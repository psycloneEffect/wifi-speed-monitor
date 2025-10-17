"""
Network adapter implementation.

Provides network statistics gathering using psutil, speedtest-cli, and ping3.
"""

import subprocess
import statistics
from datetime import datetime
from typing import Union

import psutil
import speedtest
from ping3 import ping

from project.core.constants import (
    DEFAULT_PING_COUNT,
    DEFAULT_PING_HOST,
    FALLBACK_PING_HOSTS,
    MAX_SPEEDTEST_RETRY,
    NETWORK_TIMEOUT,
    PING_TIMEOUT,
)
from project.core.enums import MeasurementStatus
from project.core.interfaces import INetworkProvider
from project.core.models import NetworkStats


class PsutilNetworkProvider(INetworkProvider):
    """
    Network information provider using psutil.

    Gathers network statistics including speed, latency, packet loss,
    and connection information using multiple tools.
    """

    def __init__(self) -> None:
        """Initialize the network provider."""
        self._last_counters = None
        self._last_time = None
        self._ping_host = DEFAULT_PING_HOST
        self._speedtest_client: Union[speedtest.Speedtest, None] = None

    def get_current_stats(self) -> NetworkStats:
        """
        Get current network statistics.

        Returns:
            NetworkStats with current network measurements.
        """
        download_speed, upload_speed = self._get_interface_speed()
        latency, packet_loss = self._measure_latency_and_loss()
        ssid, signal_strength = self._get_wifi_info()

        return NetworkStats(
            download_speed=round(download_speed, 2),
            upload_speed=round(upload_speed, 2),
            latency=latency,
            packet_loss=packet_loss,
            timestamp=datetime.now(),
            ssid=ssid,
            signal_strength=signal_strength,
        )

    def get_connection_info(self) -> dict:
        """
        Get connection information (legacy method).

        Returns:
            Dict with ssid and signal_strength keys.
        """
        ssid, signal_strength = self._get_wifi_info()
        return {"ssid": ssid, "signal_strength": signal_strength}

    def _get_interface_speed(self) -> tuple[float, float]:
        """
        Calculate interface speed from byte counters.

        Returns:
            Tuple of (download_speed, upload_speed) in Mbps.
        """
        current_counters = psutil.net_io_counters()
        current_time = datetime.now()

        download_speed = 0.0
        upload_speed = 0.0

        if self._last_counters and self._last_time:
            time_delta = (current_time - self._last_time).total_seconds()
            if time_delta > 0:
                bytes_recv = current_counters.bytes_recv - self._last_counters.bytes_recv
                bytes_sent = current_counters.bytes_sent - self._last_counters.bytes_sent

                download_speed = (bytes_recv * 8) / (time_delta * 1_000_000)
                upload_speed = (bytes_sent * 8) / (time_delta * 1_000_000)

        self._last_counters = current_counters
        self._last_time = current_time

        return download_speed, upload_speed

    def _measure_latency_and_loss(self) -> tuple[float, float]:
        """
        Measure latency and packet loss using ping.

        Returns:
            Tuple of (latency_ms, packet_loss_percentage).
        """
        latencies = []
        failed_pings = 0

        for _ in range(DEFAULT_PING_COUNT):
            try:
                result = ping(self._ping_host, timeout=PING_TIMEOUT)
                if result is not None:
                    latencies.append(result * 1000)
                else:
                    failed_pings += 1
            except Exception:
                failed_pings += 1

        if not latencies:
            return 0.0, 100.0

        avg_latency = statistics.mean(latencies)
        packet_loss = (failed_pings / DEFAULT_PING_COUNT) * 100

        return round(avg_latency, 2), round(packet_loss, 2)

    def _get_wifi_info(self) -> tuple[Union[str, None], Union[float, None]]:
        """
        Get WiFi SSID and signal strength (Windows only).

        Returns:
            Tuple of (ssid, signal_strength_dbm).
        """
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True,
                text=True,
                timeout=NETWORK_TIMEOUT,
                check=False,
            )

            if result.returncode != 0:
                return None, None

            return self._parse_netsh_output(result.stdout)

        except Exception:
            return None, None

    def _parse_netsh_output(self, output: str) -> tuple[Union[str, None], Union[float, None]]:
        """
        Parse netsh wlan show interfaces output.

        Args:
            output: Raw netsh command output.

        Returns:
            Tuple of (ssid, signal_strength_dbm).
        """
        ssid = None
        signal = None

        for line in output.splitlines():
            line = line.strip()
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":", 1)[1].strip()
            elif "Signal" in line:
                signal_str = line.split(":", 1)[1].strip().replace("%", "")
                try:
                    signal_percent = int(signal_str)
                    signal = self._convert_signal_to_dbm(signal_percent)
                except ValueError:
                    pass

        return ssid, signal

    def _convert_signal_to_dbm(self, percentage: int) -> float:
        """
        Convert signal percentage to dBm.

        Args:
            percentage: Signal strength as percentage (0-100).

        Returns:
            Approximate signal strength in dBm.
        """
        return -100 + (percentage * 0.5)

    def measure_speed_with_speedtest(self) -> tuple[float, float, MeasurementStatus]:
        """
        Measure download and upload speed using speedtest-cli.

        This method performs an actual internet speed test, which takes
        10-30 seconds to complete. Use sparingly to avoid excessive
        network usage.

        Returns:
            Tuple of (download_mbps, upload_mbps, status).
        """
        for attempt in range(MAX_SPEEDTEST_RETRY):
            try:
                if self._speedtest_client is None:
                    self._speedtest_client = speedtest.Speedtest()

                self._speedtest_client.get_best_server()

                download_bps = self._speedtest_client.download(
                    threads=None
                )
                upload_bps = self._speedtest_client.upload(threads=None)

                download_mbps = download_bps / 1_000_000
                upload_mbps = upload_bps / 1_000_000

                return (
                    round(download_mbps, 2),
                    round(upload_mbps, 2),
                    MeasurementStatus.SUCCESS,
                )

            except speedtest.ConfigRetrievalError:
                if attempt < MAX_SPEEDTEST_RETRY - 1:
                    continue
                return 0.0, 0.0, MeasurementStatus.FAILED

            except Exception:
                if attempt < MAX_SPEEDTEST_RETRY - 1:
                    continue
                return 0.0, 0.0, MeasurementStatus.FAILED

        return 0.0, 0.0, MeasurementStatus.TIMEOUT

    def measure_latency_with_fallback(self) -> tuple[float, float]:
        """
        Measure latency with fallback hosts.

        Tries multiple ping hosts if the primary host fails.

        Returns:
            Tuple of (latency_ms, packet_loss_percentage).
        """
        for host in FALLBACK_PING_HOSTS:
            self._ping_host = host
            latency, packet_loss = self._measure_latency_and_loss()

            if packet_loss < 100.0:
                return latency, packet_loss

        return 0.0, 100.0


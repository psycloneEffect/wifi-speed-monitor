"""
Unit tests for network adapter.

Tests the PsutilNetworkProvider class functionality.
"""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from project.adapters.network_adapter import PsutilNetworkProvider
from project.core.models import NetworkStats


class TestPsutilNetworkProvider:
    """Test suite for PsutilNetworkProvider."""

    @pytest.fixture
    def provider(self) -> PsutilNetworkProvider:
        """Create a PsutilNetworkProvider instance for testing."""
        return PsutilNetworkProvider()

    def test_init(self, provider: PsutilNetworkProvider) -> None:
        """Test provider initialization."""
        assert provider._last_counters is None
        assert provider._last_time is None
        assert provider._ping_host == "8.8.8.8"

    @patch("project.adapters.network_adapter.psutil.net_io_counters")
    def test_get_interface_speed_first_call(
        self, mock_net_io: Mock, provider: PsutilNetworkProvider
    ) -> None:
        """Test interface speed on first call returns zero."""
        mock_counters = Mock()
        mock_counters.bytes_recv = 1000
        mock_counters.bytes_sent = 500
        mock_net_io.return_value = mock_counters

        download_speed, upload_speed = provider._get_interface_speed()

        assert download_speed == 0.0
        assert upload_speed == 0.0
        assert provider._last_counters is not None
        assert provider._last_time is not None

    @patch("project.adapters.network_adapter.datetime")
    @patch("project.adapters.network_adapter.psutil.net_io_counters")
    def test_get_interface_speed_subsequent_call(
        self, mock_net_io: Mock, mock_datetime: Mock, provider: PsutilNetworkProvider
    ) -> None:
        """Test interface speed calculation on subsequent calls."""
        # Setup first call
        first_counters = Mock()
        first_counters.bytes_recv = 1000
        first_counters.bytes_sent = 500
        first_time = datetime(2025, 1, 1, 12, 0, 0)

        # Setup second call (1 second later)
        second_counters = Mock()
        second_counters.bytes_recv = 1001000  # 1MB received
        second_counters.bytes_sent = 500500  # 500KB sent
        second_time = datetime(2025, 1, 1, 12, 0, 1)

        mock_net_io.side_effect = [first_counters, second_counters]
        mock_datetime.now.side_effect = [first_time, second_time]

        # First call to initialize
        provider._get_interface_speed()

        # Second call to calculate speed
        download_speed, upload_speed = provider._get_interface_speed()

        # Expected: (1000000 bytes * 8 bits) / (1 second * 1_000_000) = 8 Mbps
        assert download_speed == 8.0
        # Expected: (500000 bytes * 8 bits) / (1 second * 1_000_000) = 4 Mbps
        assert upload_speed == 4.0

    @patch("project.adapters.network_adapter.ping")
    def test_measure_latency_and_loss_all_success(
        self, mock_ping: Mock, provider: PsutilNetworkProvider
    ) -> None:
        """Test latency measurement with all successful pings."""
        # Mock 10 successful pings with 0.05s (50ms) latency
        mock_ping.return_value = 0.05

        latency, packet_loss = provider._measure_latency_and_loss()

        assert latency == 50.0  # 0.05s * 1000 = 50ms
        assert packet_loss == 0.0
        assert mock_ping.call_count == 10

    @patch("project.adapters.network_adapter.ping")
    def test_measure_latency_and_loss_partial_failure(
        self, mock_ping: Mock, provider: PsutilNetworkProvider
    ) -> None:
        """Test latency measurement with some failed pings."""
        # Mock 8 successes (50ms) and 2 failures (None)
        mock_ping.side_effect = [0.05] * 8 + [None, None]

        latency, packet_loss = provider._measure_latency_and_loss()

        assert latency == 50.0
        assert packet_loss == 20.0  # 2/10 * 100 = 20%
        assert mock_ping.call_count == 10

    @patch("project.adapters.network_adapter.ping")
    def test_measure_latency_and_loss_all_failure(
        self, mock_ping: Mock, provider: PsutilNetworkProvider
    ) -> None:
        """Test latency measurement with all failed pings."""
        mock_ping.return_value = None

        latency, packet_loss = provider._measure_latency_and_loss()

        assert latency == 0.0
        assert packet_loss == 100.0
        assert mock_ping.call_count == 10

    @patch("project.adapters.network_adapter.ping")
    def test_measure_latency_and_loss_exception(
        self, mock_ping: Mock, provider: PsutilNetworkProvider
    ) -> None:
        """Test latency measurement with exceptions."""
        mock_ping.side_effect = Exception("Network error")

        latency, packet_loss = provider._measure_latency_and_loss()

        assert latency == 0.0
        assert packet_loss == 100.0

    @patch("project.adapters.network_adapter.subprocess.run")
    def test_get_wifi_info_success(
        self, mock_subprocess: Mock, provider: PsutilNetworkProvider
    ) -> None:
        """Test WiFi info extraction from netsh output."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = """
            SSID                   : MyNetwork
            BSSID                  : aa:bb:cc:dd:ee:ff
            Signal                 : 80%
        """
        mock_subprocess.return_value = mock_result

        ssid, signal_strength = provider._get_wifi_info()

        assert ssid == "MyNetwork"
        assert signal_strength == -60.0  # -100 + (80 * 0.5)

    @patch("project.adapters.network_adapter.subprocess.run")
    def test_get_wifi_info_not_connected(
        self, mock_subprocess: Mock, provider: PsutilNetworkProvider
    ) -> None:
        """Test WiFi info when not connected."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_subprocess.return_value = mock_result

        ssid, signal_strength = provider._get_wifi_info()

        assert ssid is None
        assert signal_strength is None

    @patch("project.adapters.network_adapter.subprocess.run")
    def test_get_wifi_info_exception(
        self, mock_subprocess: Mock, provider: PsutilNetworkProvider
    ) -> None:
        """Test WiFi info with subprocess exception."""
        mock_subprocess.side_effect = Exception("Command failed")

        ssid, signal_strength = provider._get_wifi_info()

        assert ssid is None
        assert signal_strength is None

    def test_parse_netsh_output_full_info(
        self, provider: PsutilNetworkProvider
    ) -> None:
        """Test parsing complete netsh output."""
        output = """
            Name                   : Wi-Fi
            SSID                   : TestNetwork
            BSSID                  : aa:bb:cc:dd:ee:ff
            Signal                 : 90%
        """

        ssid, signal = provider._parse_netsh_output(output)

        assert ssid == "TestNetwork"
        assert signal == -55.0  # -100 + (90 * 0.5)

    def test_parse_netsh_output_missing_info(
        self, provider: PsutilNetworkProvider
    ) -> None:
        """Test parsing incomplete netsh output."""
        output = """
            Name                   : Wi-Fi
        """

        ssid, signal = provider._parse_netsh_output(output)

        assert ssid is None
        assert signal is None

    def test_parse_netsh_output_invalid_signal(
        self, provider: PsutilNetworkProvider
    ) -> None:
        """Test parsing netsh output with invalid signal."""
        output = """
            SSID                   : TestNetwork
            Signal                 : Invalid%
        """

        ssid, signal = provider._parse_netsh_output(output)

        assert ssid == "TestNetwork"
        assert signal is None

    @pytest.mark.parametrize(
        "percentage,expected_dbm",
        [
            (0, -100.0),
            (50, -75.0),
            (80, -60.0),
            (100, -50.0),
        ],
    )
    def test_convert_signal_to_dbm(
        self, provider: PsutilNetworkProvider, percentage: int, expected_dbm: float
    ) -> None:
        """Test signal percentage to dBm conversion."""
        result = provider._convert_signal_to_dbm(percentage)
        assert result == expected_dbm

    @patch.object(PsutilNetworkProvider, "_get_wifi_info")
    def test_get_connection_info(
        self, mock_get_wifi: Mock, provider: PsutilNetworkProvider
    ) -> None:
        """Test get_connection_info legacy method."""
        mock_get_wifi.return_value = ("TestSSID", -65.0)

        result = provider.get_connection_info()

        assert result == {"ssid": "TestSSID", "signal_strength": -65.0}

    @patch.object(PsutilNetworkProvider, "_get_wifi_info")
    @patch.object(PsutilNetworkProvider, "_measure_latency_and_loss")
    @patch.object(PsutilNetworkProvider, "_get_interface_speed")
    def test_get_current_stats_integration(
        self,
        mock_speed: Mock,
        mock_latency: Mock,
        mock_wifi: Mock,
        provider: PsutilNetworkProvider,
    ) -> None:
        """Test complete stats gathering integration."""
        mock_speed.return_value = (100.5, 50.25)
        mock_latency.return_value = (25.5, 0.5)
        mock_wifi.return_value = ("MyWiFi", -55.0)

        stats = provider.get_current_stats()

        assert isinstance(stats, NetworkStats)
        assert stats.download_speed == 100.5
        assert stats.upload_speed == 50.25
        assert stats.latency == 25.5
        assert stats.packet_loss == 0.5
        assert stats.ssid == "MyWiFi"
        assert stats.signal_strength == -55.0
        assert isinstance(stats.timestamp, datetime)

"""
ネットワークアダプター実装
"""
from datetime import datetime
from typing import Optional
import psutil
from project.core.interfaces import INetworkProvider
from project.core.models import NetworkStats


class PsutilNetworkProvider(INetworkProvider):
    """psutilを使用したネットワーク情報プロバイダー"""
    
    def __init__(self):
        self._last_counters = None
        self._last_time = None
    
    def get_current_stats(self) -> NetworkStats:
        """現在のネットワーク統計を取得"""
        # 実際の実装では、speedtest-cliやping3を使用して
        # より正確な速度とレイテンシを測定します
        # ここでは簡略化した例を示します
        
        current_counters = psutil.net_io_counters()
        current_time = datetime.now()
        
        download_speed = 0.0
        upload_speed = 0.0
        
        if self._last_counters and self._last_time:
            time_delta = (current_time - self._last_time).total_seconds()
            if time_delta > 0:
                bytes_recv_delta = current_counters.bytes_recv - self._last_counters.bytes_recv
                bytes_sent_delta = current_counters.bytes_sent - self._last_counters.bytes_sent
                
                # Mbpsに変換
                download_speed = (bytes_recv_delta * 8) / (time_delta * 1_000_000)
                upload_speed = (bytes_sent_delta * 8) / (time_delta * 1_000_000)
        
        self._last_counters = current_counters
        self._last_time = current_time
        
        # TODO: ping3を使用してレイテンシを測定
        latency = self._measure_latency()
        
        connection_info = self.get_connection_info()
        
        return NetworkStats(
            download_speed=round(download_speed, 2),
            upload_speed=round(upload_speed, 2),
            latency=latency,
            packet_loss=0.0,  # TODO: 実装
            timestamp=current_time,
            ssid=connection_info.get('ssid'),
            signal_strength=connection_info.get('signal_strength')
        )
    
    def get_connection_info(self) -> dict:
        """接続情報を取得"""
        # TODO: Windowsの場合はnetsh wlan show interfacesを使用
        # プラットフォーム別の実装が必要
        return {
            'ssid': None,
            'signal_strength': None
        }
    
    def _measure_latency(self) -> float:
        """レイテンシを測定（ping）"""
        # TODO: ping3ライブラリを使用して実装
        return 0.0

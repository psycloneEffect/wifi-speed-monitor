"""
ドメインモデル定義
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NetworkStats:
    """ネットワーク統計情報"""
    download_speed: float  # Mbps
    upload_speed: float    # Mbps
    latency: float         # ms
    packet_loss: float     # %
    timestamp: datetime
    ssid: Optional[str] = None  # WiFi SSID
    signal_strength: Optional[int] = None  # dBm


@dataclass
class StabilityMetrics:
    """安定性メトリクス"""
    jitter: float          # ms (レイテンシのばらつき)
    consistency_score: float  # 0-100
    connection_quality: str  # "Excellent", "Good", "Fair", "Poor"

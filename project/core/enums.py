"""
ネットワークモニタリング用の列挙型定義.

このモジュールでは、アプリケーション全体で使用される列挙型を定義します。
ネットワーク接続品質、ネットワークタイプ、測定ステータスなどを表現します。
"""

from enum import Enum, auto


class ConnectionQuality(Enum):
    """
    ネットワーク接続品質の評価.

    レイテンシ、ジッター、パケットロス、速度測定に基づいて判定されます。
    """

    EXCELLENT = auto()
    GOOD = auto()
    FAIR = auto()
    POOR = auto()
    UNKNOWN = auto()

    def __str__(self) -> str:
        """人間が読みやすい文字列表現を返します."""
        return self.name.capitalize()


class NetworkType(Enum):
    """
    ネットワーク接続のタイプ.

    物理的/論理的な接続タイプを識別するために使用されます。
    """

    WIFI = auto()
    ETHERNET = auto()
    MOBILE = auto()
    UNKNOWN = auto()

    def __str__(self) -> str:
        """人間が読みやすい文字列表現を返します."""
        return self.name.capitalize()


class SignalStrength(Enum):
    """
    WiFi信号強度の評価.

    RSSI (受信信号強度インジケーター) のdBm値に基づきます。
    - EXCELLENT: -50 dBm以上
    - GOOD: -60 dBm以上
    - FAIR: -70 dBm以上
    - POOR: -80 dBm以上
    - VERY_POOR: -80 dBm未満
    """

    EXCELLENT = auto()
    GOOD = auto()
    FAIR = auto()
    POOR = auto()
    VERY_POOR = auto()
    UNKNOWN = auto()

    def __str__(self) -> str:
        """人間が読みやすい文字列表現を返します."""
        return self.name.replace("_", " ").capitalize()


class MeasurementStatus(Enum):
    """
    ネットワーク測定操作のステータス.

    測定試行の現在の状態または結果を示します。
    """

    IDLE = auto()
    IN_PROGRESS = auto()
    SUCCESS = auto()
    FAILED = auto()
    TIMEOUT = auto()

    def __str__(self) -> str:
        """人間が読みやすい文字列表現を返します."""
        return self.name.replace("_", " ").capitalize()

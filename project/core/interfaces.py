"""
インターフェース定義（抽象基底クラス）
"""
from abc import ABC, abstractmethod
from .models import NetworkStats, StabilityMetrics


class INetworkProvider(ABC):
    """ネットワーク情報プロバイダーインターフェース"""
    
    @abstractmethod
    def get_current_stats(self) -> NetworkStats:
        """現在のネットワーク統計を取得"""
        pass
    
    @abstractmethod
    def get_connection_info(self) -> dict:
        """接続情報（SSID、信号強度等）を取得"""
        pass


class IStabilityAnalyzer(ABC):
    """安定性分析インターフェース"""
    
    @abstractmethod
    def analyze(self, stats_history: list[NetworkStats]) -> StabilityMetrics:
        """統計履歴から安定性を分析"""
        pass


class IUIPresenter(ABC):
    """UI表示インターフェース"""
    
    @abstractmethod
    def show_tooltip(self, stats: NetworkStats, metrics: StabilityMetrics) -> None:
        """ツールチップを表示"""
        pass
    
    @abstractmethod
    def update_icon(self, quality: str) -> None:
        """トレイアイコンを更新"""
        pass

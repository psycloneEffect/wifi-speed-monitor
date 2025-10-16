"""
ネットワークモニタリングサービス
"""
from typing import List
from datetime import datetime, timedelta
from project.core.interfaces import INetworkProvider, IStabilityAnalyzer
from project.core.models import NetworkStats, StabilityMetrics


class NetworkMonitorService:
    """ネットワーク監視サービス"""
    
    def __init__(
        self,
        provider: INetworkProvider,
        analyzer: IStabilityAnalyzer,
        history_size: int = 60
    ):
        self._provider = provider
        self._analyzer = analyzer
        self._history: List[NetworkStats] = []
        self._history_size = history_size
    
    def collect_stats(self) -> NetworkStats:
        """統計情報を収集して履歴に追加"""
        stats = self._provider.get_current_stats()
        self._add_to_history(stats)
        return stats
    
    def get_stability_metrics(self) -> StabilityMetrics:
        """現在の安定性メトリクスを取得"""
        if len(self._history) < 2:
            # データ不足の場合はデフォルト値
            return StabilityMetrics(
                jitter=0.0,
                consistency_score=0.0,
                connection_quality="Insufficient Data"
            )
        return self._analyzer.analyze(self._history)
    
    def _add_to_history(self, stats: NetworkStats) -> None:
        """履歴に追加（最大サイズを維持）"""
        self._history.append(stats)
        if len(self._history) > self._history_size:
            self._history.pop(0)
    
    def clear_old_history(self, max_age_minutes: int = 60) -> None:
        """古い履歴データをクリア"""
        cutoff = datetime.now() - timedelta(minutes=max_age_minutes)
        self._history = [s for s in self._history if s.timestamp > cutoff]

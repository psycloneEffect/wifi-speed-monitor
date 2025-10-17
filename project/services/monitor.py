"""
ネットワークモニタリングサービス
"""
import logging
from collections import deque
from datetime import datetime, timedelta
from typing import Deque, Union

from project.core.constants import (
    DEFAULT_HISTORY_SIZE,
    MAX_HISTORY_SIZE,
    MIN_HISTORY_SIZE,
)
from project.core.interfaces import INetworkProvider, IStabilityAnalyzer
from project.core.models import NetworkStats, StabilityMetrics

logger = logging.getLogger(__name__)


class NetworkMonitorService:
    """ネットワーク監視サービス"""
    
    def __init__(
        self,
        provider: INetworkProvider,
        analyzer: IStabilityAnalyzer,
        history_size: Union[int, None] = None,
    ):
        self._provider = provider
        self._analyzer = analyzer
        
        if history_size is None:
            history_size = DEFAULT_HISTORY_SIZE
        
        if history_size < MIN_HISTORY_SIZE:
            logger.warning(
                f"History size {history_size} is below minimum "
                f"{MIN_HISTORY_SIZE}. Using minimum."
            )
            history_size = MIN_HISTORY_SIZE
        
        if history_size > MAX_HISTORY_SIZE:
            logger.warning(
                f"History size {history_size} exceeds maximum "
                f"{MAX_HISTORY_SIZE}. Using maximum."
            )
            history_size = MAX_HISTORY_SIZE
        
        self._history_size = history_size
        self._history: Deque[NetworkStats] = deque(maxlen=history_size)
    
    def collect_stats(self) -> Union[NetworkStats, None]:
        """
        統計情報を収集して履歴に追加.

        Returns:
            収集された統計情報、エラーの場合は None.
        """
        try:
            stats = self._provider.get_current_stats()
            self._add_to_history(stats)
            logger.debug(
                f"Collected stats: "
                f"Download={stats.download_speed:.2f}Mbps, "
                f"Latency={stats.latency:.2f}ms"
            )
            return stats
        except Exception as e:
            logger.error(f"Failed to collect stats: {e}")
            return None
    
    def get_stability_metrics(self) -> StabilityMetrics:
        """
        現在の安定性メトリクスを取得.

        Returns:
            分析された安定性メトリクス.
        """
        if len(self._history) < MIN_HISTORY_SIZE:
            logger.warning(
                f"Insufficient data for analysis: {len(self._history)} "
                f"samples (minimum {MIN_HISTORY_SIZE})"
            )
            return self._create_insufficient_data_metrics()
        
        try:
            return self._analyzer.analyze(list(self._history))
        except Exception as e:
            logger.error(f"Failed to analyze stability: {e}")
            return self._create_insufficient_data_metrics()
    
    def _add_to_history(self, stats: NetworkStats) -> None:
        """
        履歴に追加（最大サイズを維持）.

        Args:
            stats: 追加する統計情報.
        """
        self._history.append(stats)
    
    def clear_old_history(self, max_age_minutes: int = 60) -> None:
        """
        古い履歴データをクリア.

        Args:
            max_age_minutes: 保持する最大の経過時間（分）.
        """
        cutoff = datetime.now() - timedelta(minutes=max_age_minutes)
        initial_count = len(self._history)
        
        self._history = deque(
            (s for s in self._history if s.timestamp > cutoff),
            maxlen=self._history_size,
        )
        
        removed_count = initial_count - len(self._history)
        if removed_count > 0:
            logger.info(f"Cleared {removed_count} old history entries")
    
    def get_history_count(self) -> int:
        """
        履歴データの件数を取得.

        Returns:
            履歴に保存されているデータ数.
        """
        return len(self._history)
    
    def get_history(self) -> list[NetworkStats]:
        """
        履歴データのコピーを取得.

        Returns:
            履歴データのリスト.
        """
        return list(self._history)
    
    def clear_all_history(self) -> None:
        """すべての履歴データをクリア."""
        count = len(self._history)
        self._history.clear()
        logger.info(f"Cleared all history ({count} entries)")
    
    def _create_insufficient_data_metrics(self) -> StabilityMetrics:
        """
        データ不足時のデフォルトメトリクスを作成.

        Returns:
            デフォルトの安定性メトリクス.
        """
        return StabilityMetrics(
            jitter=0.0,
            consistency_score=0.0,
            connection_quality="Insufficient Data",
        )

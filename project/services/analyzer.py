"""
安定性分析サービス
"""
from statistics import stdev, mean

from project.core.constants import (
    JITTER_EXCELLENT,
    JITTER_FAIR,
    JITTER_GOOD,
    LATENCY_EXCELLENT,
    LATENCY_FAIR,
    LATENCY_GOOD,
    PACKET_LOSS_FAIR,
    PACKET_LOSS_GOOD,
    WEIGHT_JITTER,
    WEIGHT_LATENCY,
    WEIGHT_PACKET_LOSS,
    WEIGHT_SPEED,
)
from project.core.enums import ConnectionQuality
from project.core.interfaces import IStabilityAnalyzer
from project.core.models import NetworkStats, StabilityMetrics


class StabilityAnalyzerService(IStabilityAnalyzer):
    """ネットワーク安定性分析サービス"""

    def analyze(self, stats_history: list[NetworkStats]) -> StabilityMetrics:
        """統計履歴から安定性を分析"""
        if len(stats_history) < 2:
            return self._default_metrics()

        # レイテンシのばらつき（ジッター）を計算
        latencies = [s.latency for s in stats_history]
        jitter = stdev(latencies) if len(latencies) > 1 else 0.0

        # 速度の一貫性スコアを計算
        download_speeds = [s.download_speed for s in stats_history]
        consistency_score = self._calculate_consistency(download_speeds)

        # 総合的な接続品質を判定
        quality = self._determine_quality(
            mean(latencies),
            jitter,
            consistency_score,
            mean([s.packet_loss for s in stats_history])
        )

        return StabilityMetrics(
            jitter=round(jitter, 2),
            consistency_score=round(consistency_score, 2),
            connection_quality=quality
        )

    def _calculate_consistency(self, values: list[float]) -> float:
        """値の一貫性スコアを計算（0-100）"""
        if not values or len(values) < 2:
            return 0.0

        avg = mean(values)
        if avg == 0:
            return 0.0

        # 変動係数（CV）から一貫性を計算
        cv = (stdev(values) / avg) * 100
        # CVが低いほど一貫性が高い（100点満点に変換）
        consistency = max(0, 100 - cv)
        return min(100, consistency)

    def _determine_quality(
        self,
        avg_latency: float,
        jitter: float,
        consistency: float,
        packet_loss: float
    ) -> str:
        """接続品質を判定"""
        if packet_loss > PACKET_LOSS_FAIR:
            return ConnectionQuality.POOR.value
        if avg_latency > LATENCY_GOOD or jitter > JITTER_FAIR:
            return ConnectionQuality.FAIR.value
        if consistency > 80 and avg_latency < LATENCY_EXCELLENT:
            return ConnectionQuality.EXCELLENT.value
        if avg_latency < LATENCY_GOOD and jitter < JITTER_GOOD:
            return ConnectionQuality.GOOD.value
        return ConnectionQuality.FAIR.value

    def _default_metrics(self) -> StabilityMetrics:
        """デフォルトメトリクス"""
        return StabilityMetrics(
            jitter=0.0,
            consistency_score=0.0,
            connection_quality=ConnectionQuality.UNKNOWN.value
        )

    def calculate_quality_score(
        self,
        latency: float,
        jitter: float,
        packet_loss: float,
        speed: float,
    ) -> float:
        """
        Calculate weighted quality score (0-100).

        Args:
            latency: Average latency in ms.
            jitter: Jitter in ms.
            packet_loss: Packet loss percentage.
            speed: Download speed in Mbps.

        Returns:
            Quality score from 0 to 100.
        """
        latency_score = self._normalize_latency_score(latency)
        jitter_score = self._normalize_jitter_score(jitter)
        packet_loss_score = self._normalize_packet_loss_score(packet_loss)
        speed_score = self._normalize_speed_score(speed)

        total_score = (
            latency_score * WEIGHT_LATENCY
            + jitter_score * WEIGHT_JITTER
            + packet_loss_score * WEIGHT_PACKET_LOSS
            + speed_score * WEIGHT_SPEED
        )

        return round(total_score, 2)

    def _normalize_latency_score(self, latency: float) -> float:
        """Normalize latency to 0-100 score."""
        if latency <= LATENCY_EXCELLENT:
            return 100.0
        if latency >= LATENCY_FAIR:
            return 0.0
        ratio = (LATENCY_FAIR - latency) / (LATENCY_FAIR - LATENCY_EXCELLENT)
        return ratio * 100.0

    def _normalize_jitter_score(self, jitter: float) -> float:
        """Normalize jitter to 0-100 score."""
        if jitter <= JITTER_EXCELLENT:
            return 100.0
        if jitter >= JITTER_FAIR:
            return 0.0
        ratio = (JITTER_FAIR - jitter) / (JITTER_FAIR - JITTER_EXCELLENT)
        return ratio * 100.0

    def _normalize_packet_loss_score(self, packet_loss: float) -> float:
        """Normalize packet loss to 0-100 score."""
        if packet_loss <= PACKET_LOSS_GOOD:
            return 100.0
        if packet_loss >= PACKET_LOSS_FAIR:
            return 0.0
        ratio = (PACKET_LOSS_FAIR - packet_loss) / (
            PACKET_LOSS_FAIR - PACKET_LOSS_GOOD
        )
        return ratio * 100.0

    def _normalize_speed_score(self, speed: float) -> float:
        """Normalize speed to 0-100 score."""
        if speed >= 100.0:
            return 100.0
        if speed <= 10.0:
            return 0.0
        return (speed - 10.0) / 0.9

"""
安定性分析サービス
"""
from statistics import stdev, mean
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
        if packet_loss > 5.0:
            return "Poor"
        if avg_latency > 100 or jitter > 50:
            return "Fair"
        if consistency > 80 and avg_latency < 50:
            return "Excellent"
        return "Good"
    
    def _default_metrics(self) -> StabilityMetrics:
        """デフォルトメトリクス"""
        return StabilityMetrics(
            jitter=0.0,
            consistency_score=0.0,
            connection_quality="Unknown"
        )

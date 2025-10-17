"""
Unit tests for stability analyzer service.

Tests the StabilityAnalyzerService class functionality.
"""

from datetime import datetime

import pytest

from project.core.constants import (
    JITTER_EXCELLENT,
    JITTER_FAIR,
    LATENCY_EXCELLENT,
    LATENCY_FAIR,
    PACKET_LOSS_FAIR,
)
from project.core.enums import ConnectionQuality
from project.core.models import NetworkStats, StabilityMetrics
from project.services.analyzer import StabilityAnalyzerService


class TestStabilityAnalyzerService:
    """Test suite for StabilityAnalyzerService."""

    @pytest.fixture
    def analyzer(self) -> StabilityAnalyzerService:
        """Create a StabilityAnalyzerService instance for testing."""
        return StabilityAnalyzerService()

    @pytest.fixture
    def sample_stats(self) -> list[NetworkStats]:
        """Create sample network statistics for testing."""
        return [
            NetworkStats(
                download_speed=100.0,
                upload_speed=50.0,
                latency=25.0,
                packet_loss=0.0,
                timestamp=datetime.now(),
                ssid="TestNetwork",
                signal_strength=-60.0,
            ),
            NetworkStats(
                download_speed=105.0,
                upload_speed=48.0,
                latency=30.0,
                packet_loss=0.0,
                timestamp=datetime.now(),
                ssid="TestNetwork",
                signal_strength=-60.0,
            ),
            NetworkStats(
                download_speed=98.0,
                upload_speed=52.0,
                latency=28.0,
                packet_loss=0.5,
                timestamp=datetime.now(),
                ssid="TestNetwork",
                signal_strength=-62.0,
            ),
        ]

    def test_analyze_insufficient_data(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test analysis with insufficient data."""
        stats = [
            NetworkStats(
                download_speed=100.0,
                upload_speed=50.0,
                latency=25.0,
                packet_loss=0.0,
                timestamp=datetime.now(),
                ssid=None,
                signal_strength=None,
            )
        ]

        metrics = analyzer.analyze(stats)

        assert isinstance(metrics, StabilityMetrics)
        assert metrics.jitter == 0.0
        assert metrics.consistency_score == 0.0
        assert metrics.connection_quality == ConnectionQuality.UNKNOWN.value

    def test_analyze_good_connection(
        self, analyzer: StabilityAnalyzerService, sample_stats: list[NetworkStats]
    ) -> None:
        """Test analysis with good connection quality."""
        metrics = analyzer.analyze(sample_stats)

        assert isinstance(metrics, StabilityMetrics)
        assert metrics.jitter > 0.0
        assert metrics.consistency_score > 0.0
        assert metrics.connection_quality in [
            ConnectionQuality.EXCELLENT.value,
            ConnectionQuality.GOOD.value,
        ]

    def test_analyze_poor_connection_high_packet_loss(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test analysis with high packet loss."""
        stats = [
            NetworkStats(
                download_speed=50.0,
                upload_speed=25.0,
                latency=100.0,
                packet_loss=10.0,
                timestamp=datetime.now(),
                ssid=None,
                signal_strength=None,
            ),
            NetworkStats(
                download_speed=48.0,
                upload_speed=23.0,
                latency=105.0,
                packet_loss=12.0,
                timestamp=datetime.now(),
                ssid=None,
                signal_strength=None,
            ),
        ]

        metrics = analyzer.analyze(stats)

        assert metrics.connection_quality == ConnectionQuality.POOR.value

    def test_calculate_consistency_empty_values(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test consistency calculation with empty values."""
        consistency = analyzer._calculate_consistency([])

        assert consistency == 0.0

    def test_calculate_consistency_single_value(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test consistency calculation with single value."""
        consistency = analyzer._calculate_consistency([100.0])

        assert consistency == 0.0

    def test_calculate_consistency_consistent_values(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test consistency calculation with consistent values."""
        values = [100.0, 101.0, 99.0, 100.5, 99.5]
        consistency = analyzer._calculate_consistency(values)

        assert consistency > 90.0

    def test_calculate_consistency_inconsistent_values(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test consistency calculation with inconsistent values."""
        values = [100.0, 50.0, 150.0, 75.0, 125.0]
        consistency = analyzer._calculate_consistency(values)

        assert consistency < 70.0

    def test_determine_quality_excellent(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test quality determination for excellent connection."""
        quality = analyzer._determine_quality(
            avg_latency=LATENCY_EXCELLENT - 10,
            jitter=JITTER_EXCELLENT - 5,
            consistency=90.0,
            packet_loss=0.0,
        )

        assert quality == ConnectionQuality.EXCELLENT.value

    def test_determine_quality_good(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test quality determination for good connection."""
        quality = analyzer._determine_quality(
            avg_latency=LATENCY_EXCELLENT + 20,
            jitter=JITTER_EXCELLENT + 10,
            consistency=70.0,
            packet_loss=1.0,
        )

        assert quality == ConnectionQuality.GOOD.value

    def test_determine_quality_fair(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test quality determination for fair connection."""
        quality = analyzer._determine_quality(
            avg_latency=LATENCY_FAIR - 50,
            jitter=JITTER_FAIR,
            consistency=60.0,
            packet_loss=2.0,
        )

        assert quality == ConnectionQuality.FAIR.value

    def test_determine_quality_poor(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test quality determination for poor connection."""
        quality = analyzer._determine_quality(
            avg_latency=LATENCY_FAIR + 100,
            jitter=JITTER_FAIR + 50,
            consistency=40.0,
            packet_loss=PACKET_LOSS_FAIR + 5,
        )

        assert quality == ConnectionQuality.POOR.value

    def test_calculate_quality_score_excellent(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test quality score calculation for excellent metrics."""
        score = analyzer.calculate_quality_score(
            latency=LATENCY_EXCELLENT - 10,
            jitter=JITTER_EXCELLENT - 5,
            packet_loss=0.0,
            speed=150.0,
        )

        assert score > 80.0

    def test_calculate_quality_score_poor(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test quality score calculation for poor metrics."""
        score = analyzer.calculate_quality_score(
            latency=LATENCY_FAIR + 100,
            jitter=JITTER_FAIR + 50,
            packet_loss=PACKET_LOSS_FAIR + 5,
            speed=5.0,
        )

        assert score < 20.0

    def test_normalize_latency_score_excellent(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test latency normalization for excellent values."""
        score = analyzer._normalize_latency_score(LATENCY_EXCELLENT - 10)

        assert score == 100.0

    def test_normalize_latency_score_poor(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test latency normalization for poor values."""
        score = analyzer._normalize_latency_score(LATENCY_FAIR + 100)

        assert score == 0.0

    def test_normalize_jitter_score_excellent(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test jitter normalization for excellent values."""
        score = analyzer._normalize_jitter_score(JITTER_EXCELLENT - 5)

        assert score == 100.0

    def test_normalize_jitter_score_poor(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test jitter normalization for poor values."""
        score = analyzer._normalize_jitter_score(JITTER_FAIR + 50)

        assert score == 0.0

    def test_normalize_packet_loss_score_excellent(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test packet loss normalization for excellent values."""
        from project.core.constants import PACKET_LOSS_GOOD

        score = analyzer._normalize_packet_loss_score(PACKET_LOSS_GOOD - 0.5)

        assert score == 100.0

    def test_normalize_packet_loss_score_poor(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test packet loss normalization for poor values."""
        score = analyzer._normalize_packet_loss_score(PACKET_LOSS_FAIR + 5)

        assert score == 0.0

    def test_normalize_speed_score_excellent(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test speed normalization for excellent values."""
        score = analyzer._normalize_speed_score(150.0)

        assert score == 100.0

    def test_normalize_speed_score_poor(
        self, analyzer: StabilityAnalyzerService
    ) -> None:
        """Test speed normalization for poor values."""
        score = analyzer._normalize_speed_score(5.0)

        assert score == 0.0

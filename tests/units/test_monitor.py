"""
Unit tests for network monitor service.

Tests the NetworkMonitorService class functionality.
"""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from project.core.constants import (
    DEFAULT_HISTORY_SIZE,
    MAX_HISTORY_SIZE,
    MIN_HISTORY_SIZE,
)
from project.core.models import NetworkStats, StabilityMetrics
from project.services.monitor import NetworkMonitorService


class TestNetworkMonitorService:
    """Test suite for NetworkMonitorService."""

    @pytest.fixture
    def mock_provider(self) -> Mock:
        """Create a mock network provider."""
        provider = Mock()
        provider.get_current_stats.return_value = NetworkStats(
            download_speed=100.0,
            upload_speed=50.0,
            latency=25.0,
            packet_loss=0.0,
            timestamp=datetime.now(),
            ssid="TestNetwork",
            signal_strength=-60.0,
        )
        return provider

    @pytest.fixture
    def mock_analyzer(self) -> Mock:
        """Create a mock stability analyzer."""
        analyzer = Mock()
        analyzer.analyze.return_value = StabilityMetrics(
            jitter=5.0,
            consistency_score=90.0,
            connection_quality="Excellent",
        )
        return analyzer

    @pytest.fixture
    def monitor(
        self, mock_provider: Mock, mock_analyzer: Mock
    ) -> NetworkMonitorService:
        """Create a NetworkMonitorService instance for testing."""
        return NetworkMonitorService(
            provider=mock_provider, analyzer=mock_analyzer
        )

    def test_init_default_history_size(
        self, mock_provider: Mock, mock_analyzer: Mock
    ) -> None:
        """Test initialization with default history size."""
        monitor = NetworkMonitorService(
            provider=mock_provider, analyzer=mock_analyzer
        )

        assert monitor._history_size == DEFAULT_HISTORY_SIZE
        assert len(monitor._history) == 0

    def test_init_custom_history_size(
        self, mock_provider: Mock, mock_analyzer: Mock
    ) -> None:
        """Test initialization with custom history size."""
        custom_size = 100
        monitor = NetworkMonitorService(
            provider=mock_provider, analyzer=mock_analyzer, history_size=custom_size
        )

        assert monitor._history_size == custom_size

    def test_init_below_minimum_history_size(
        self, mock_provider: Mock, mock_analyzer: Mock
    ) -> None:
        """Test initialization with below minimum history size."""
        monitor = NetworkMonitorService(
            provider=mock_provider,
            analyzer=mock_analyzer,
            history_size=MIN_HISTORY_SIZE - 1,
        )

        assert monitor._history_size == MIN_HISTORY_SIZE

    def test_init_above_maximum_history_size(
        self, mock_provider: Mock, mock_analyzer: Mock
    ) -> None:
        """Test initialization with above maximum history size."""
        monitor = NetworkMonitorService(
            provider=mock_provider,
            analyzer=mock_analyzer,
            history_size=MAX_HISTORY_SIZE + 1,
        )

        assert monitor._history_size == MAX_HISTORY_SIZE

    def test_collect_stats_success(self, monitor: NetworkMonitorService) -> None:
        """Test successful stats collection."""
        stats = monitor.collect_stats()

        assert stats is not None
        assert isinstance(stats, NetworkStats)
        assert len(monitor._history) == 1

    def test_collect_stats_multiple_times(
        self, monitor: NetworkMonitorService
    ) -> None:
        """Test collecting stats multiple times."""
        for _ in range(5):
            monitor.collect_stats()

        assert len(monitor._history) == 5

    def test_collect_stats_exceeds_max_size(
        self, mock_provider: Mock, mock_analyzer: Mock
    ) -> None:
        """Test that history doesn't exceed maximum size."""
        monitor = NetworkMonitorService(
            provider=mock_provider, analyzer=mock_analyzer, history_size=15
        )

        for _ in range(20):
            monitor.collect_stats()

        assert len(monitor._history) == 15

    def test_collect_stats_error_handling(
        self, mock_provider: Mock, mock_analyzer: Mock
    ) -> None:
        """Test error handling during stats collection."""
        mock_provider.get_current_stats.side_effect = Exception("Network error")
        monitor = NetworkMonitorService(
            provider=mock_provider, analyzer=mock_analyzer
        )

        stats = monitor.collect_stats()

        assert stats is None
        assert len(monitor._history) == 0

    def test_get_stability_metrics_insufficient_data(
        self, monitor: NetworkMonitorService
    ) -> None:
        """Test getting stability metrics with insufficient data."""
        metrics = monitor.get_stability_metrics()

        assert isinstance(metrics, StabilityMetrics)
        assert metrics.connection_quality == "Insufficient Data"

    def test_get_stability_metrics_success(
        self, monitor: NetworkMonitorService, mock_analyzer: Mock
    ) -> None:
        """Test getting stability metrics with sufficient data."""
        for _ in range(MIN_HISTORY_SIZE):
            monitor.collect_stats()

        metrics = monitor.get_stability_metrics()

        assert isinstance(metrics, StabilityMetrics)
        mock_analyzer.analyze.assert_called_once()

    def test_get_stability_metrics_error_handling(
        self, monitor: NetworkMonitorService, mock_analyzer: Mock
    ) -> None:
        """Test error handling when analyzing metrics."""
        for _ in range(MIN_HISTORY_SIZE):
            monitor.collect_stats()

        mock_analyzer.analyze.side_effect = Exception("Analysis error")

        metrics = monitor.get_stability_metrics()

        assert isinstance(metrics, StabilityMetrics)
        assert metrics.connection_quality == "Insufficient Data"

    def test_clear_old_history(
        self, mock_provider: Mock, mock_analyzer: Mock
    ) -> None:
        """Test clearing old history data."""
        monitor = NetworkMonitorService(
            provider=mock_provider, analyzer=mock_analyzer
        )

        now = datetime.now()
        old_stats = NetworkStats(
            download_speed=100.0,
            upload_speed=50.0,
            latency=25.0,
            packet_loss=0.0,
            timestamp=now - timedelta(hours=2),
            ssid=None,
            signal_strength=None,
        )
        recent_stats = NetworkStats(
            download_speed=100.0,
            upload_speed=50.0,
            latency=25.0,
            packet_loss=0.0,
            timestamp=now,
            ssid=None,
            signal_strength=None,
        )

        monitor._history.append(old_stats)
        monitor._history.append(recent_stats)

        monitor.clear_old_history(max_age_minutes=60)

        assert len(monitor._history) == 1
        assert monitor._history[0].timestamp == recent_stats.timestamp

    def test_get_history_count(self, monitor: NetworkMonitorService) -> None:
        """Test getting history count."""
        assert monitor.get_history_count() == 0

        for _ in range(5):
            monitor.collect_stats()

        assert monitor.get_history_count() == 5

    def test_get_history(self, monitor: NetworkMonitorService) -> None:
        """Test getting history copy."""
        for _ in range(3):
            monitor.collect_stats()

        history = monitor.get_history()

        assert len(history) == 3
        assert isinstance(history, list)
        assert all(isinstance(s, NetworkStats) for s in history)

    def test_get_history_is_copy(self, monitor: NetworkMonitorService) -> None:
        """Test that get_history returns a copy."""
        monitor.collect_stats()

        history1 = monitor.get_history()
        history2 = monitor.get_history()

        assert history1 is not history2
        assert len(history1) == len(history2)

    def test_clear_all_history(self, monitor: NetworkMonitorService) -> None:
        """Test clearing all history."""
        for _ in range(5):
            monitor.collect_stats()

        assert monitor.get_history_count() == 5

        monitor.clear_all_history()

        assert monitor.get_history_count() == 0

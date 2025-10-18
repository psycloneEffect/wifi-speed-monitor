"""
UIアダプターのユニットテスト
"""
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from PyQt6.QtWidgets import QApplication

from project.adapters.ui_adapter import TrayUIAdapter
from project.core.enums import ConnectionQuality
from project.core.models import NetworkStats, StabilityMetrics


@pytest.fixture
def qapp():
    """QApplicationフィクスチャ"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # クリーンアップは不要（Qtのイベントループは自動管理）


@pytest.fixture
def mock_tray_icon():
    """モックされたQSystemTrayIconフィクスチャ"""
    with patch("project.adapters.ui_adapter.QSystemTrayIcon") as mock:
        instance = Mock()
        mock.return_value = instance
        yield instance


@pytest.fixture
def sample_stats():
    """サンプルのNetworkStatsフィクスチャ"""
    return NetworkStats(
        download_speed=100.5,
        upload_speed=50.2,
        latency=25.3,
        packet_loss=0.1,
        timestamp=datetime.now(),
        ssid="TestNetwork",
        signal_strength=-45,
    )


@pytest.fixture
def sample_metrics():
    """サンプルのStabilityMetricsフィクスチャ"""
    return StabilityMetrics(
        jitter=5.2,
        consistency_score=95.5,
        connection_quality="Excellent",
    )


class TestTrayUIAdapter:
    """TrayUIAdapterクラスのテスト"""

    def test_init_creates_tray_icon(self, qapp, mock_tray_icon):
        """初期化時にシステムトレイアイコンが作成されることをテスト"""
        _ = TrayUIAdapter(qapp)

        # QSystemTrayIconが作成されたことを確認
        assert mock_tray_icon.show.called

    def test_show_tooltip_sets_tooltip_text(
        self, qapp, mock_tray_icon, sample_stats, sample_metrics
    ):
        """show_tooltipがツールチップテキストを設定することをテスト"""
        adapter = TrayUIAdapter(qapp)

        adapter.show_tooltip(sample_stats, sample_metrics)

        # setToolTipが呼ばれたことを確認
        mock_tray_icon.setToolTip.assert_called_once()
        tooltip_text = mock_tray_icon.setToolTip.call_args[0][0]

        # ツールチップに主要な情報が含まれていることを確認
        assert "TestNetwork" in tooltip_text
        assert "100.5" in tooltip_text
        assert "50.2" in tooltip_text
        assert "25" in tooltip_text
        assert "Excellent" in tooltip_text

    def test_update_icon_changes_icon(self, qapp, mock_tray_icon):
        """update_iconがアイコンを変更することをテスト"""
        adapter = TrayUIAdapter(qapp)

        # 初期状態からExcellentに変更
        adapter.update_icon(ConnectionQuality.EXCELLENT.value)

        # setIconが呼ばれたことを確認
        assert mock_tray_icon.setIcon.called

    def test_update_icon_only_changes_on_quality_change(self, qapp, mock_tray_icon):
        """品質が変わった時のみアイコンが変更されることをテスト"""
        adapter = TrayUIAdapter(qapp)
        mock_tray_icon.setIcon.reset_mock()

        # 同じ品質で2回呼び出し
        adapter.update_icon(ConnectionQuality.GOOD.value)
        first_call_count = mock_tray_icon.setIcon.call_count

        adapter.update_icon(ConnectionQuality.GOOD.value)
        second_call_count = mock_tray_icon.setIcon.call_count

        # 2回目の呼び出しではsetIconが呼ばれないことを確認
        assert second_call_count == first_call_count

    def test_format_tooltip_includes_all_metrics(self, qapp, sample_stats, sample_metrics):
        """_format_tooltipがすべてのメトリクスを含むことをテスト"""
        with patch("project.adapters.ui_adapter.QSystemTrayIcon"):
            adapter = TrayUIAdapter(qapp)

            tooltip = adapter._format_tooltip(sample_stats, sample_metrics)

            # すべての主要情報が含まれていることを確認
            assert "TestNetwork" in tooltip
            assert "100.5" in tooltip
            assert "50.2" in tooltip
            assert str(int(sample_stats.latency)) in tooltip
            assert sample_metrics.connection_quality in tooltip
            # consistency_scoreは四捨五入されて表示される
            assert "96%" in tooltip or "95%" in tooltip
            assert str(sample_metrics.jitter) in tooltip

    def test_format_tooltip_handles_none_ssid(self, qapp, sample_metrics):
        """_format_tooltipがSSIDがNoneの場合を適切に処理することをテスト"""
        with patch("project.adapters.ui_adapter.QSystemTrayIcon"):
            adapter = TrayUIAdapter(qapp)

            stats_no_ssid = NetworkStats(
                download_speed=50.0,
                upload_speed=25.0,
                latency=30.0,
                packet_loss=1.0,
                timestamp=datetime.now(),
                ssid=None,
                signal_strength=None,
            )

            tooltip = adapter._format_tooltip(stats_no_ssid, sample_metrics)

            # "Unknown Network"が表示されることを確認
            assert "Unknown Network" in tooltip

    def test_quit_app_hides_tray_and_quits(self, qapp, mock_tray_icon):
        """_quit_appがトレイアイコンを非表示にしてアプリを終了することをテスト"""
        with patch.object(qapp, "quit") as mock_quit:
            adapter = TrayUIAdapter(qapp)

            adapter._quit_app()

            # hideとquitが呼ばれたことを確認
            mock_tray_icon.hide.assert_called_once()
            mock_quit.assert_called_once()

    def test_show_details_displays_message(self, qapp, mock_tray_icon):
        """_show_detailsがメッセージを表示することをテスト"""
        adapter = TrayUIAdapter(qapp)

        adapter._show_details()

        # showMessageが呼ばれたことを確認
        mock_tray_icon.showMessage.assert_called_once()

    def test_show_settings_displays_message(self, qapp, mock_tray_icon):
        """_show_settingsがメッセージを表示することをテスト"""
        adapter = TrayUIAdapter(qapp)

        adapter._show_settings()

        # showMessageが呼ばれたことを確認
        mock_tray_icon.showMessage.assert_called_once()

    def test_all_quality_levels_have_icons(self, qapp):
        """すべての品質レベルにアイコンが存在することをテスト"""
        with patch("project.adapters.ui_adapter.QSystemTrayIcon"):
            adapter = TrayUIAdapter(qapp)

            # すべての品質レベルをテスト
            quality_levels = [
                ConnectionQuality.EXCELLENT.value,
                ConnectionQuality.GOOD.value,
                ConnectionQuality.FAIR.value,
                ConnectionQuality.POOR.value,
                ConnectionQuality.UNKNOWN.value,
            ]

            for quality in quality_levels:
                # 各品質レベルのアイコンが存在することを確認
                assert quality in adapter._icons

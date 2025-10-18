"""
UIアダプター実装（PyQt6）
"""
import sys
from pathlib import Path
from typing import Optional

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from project.core.enums import ConnectionQuality
from project.core.interfaces import IUIPresenter
from project.core.models import NetworkStats, StabilityMetrics


class TrayUIAdapter(IUIPresenter):
    """システムトレイUI実装"""

    def __init__(self, app: Optional[QApplication] = None) -> None:
        """
        システムトレイUIを初期化します。

        Args:
            app: QApplicationインスタンス（Noneの場合は新規作成）
        """
        # QApplicationの初期化
        if app is None:
            self._app = QApplication.instance()
            if self._app is None:
                self._app = QApplication(sys.argv)
        else:
            self._app = app

        # システムトレイアイコンの初期化
        self._tray_icon = QSystemTrayIcon(self._app)
        self._current_quality = ConnectionQuality.UNKNOWN.value

        # デフォルトアイコンの設定
        self._setup_icons()

        # コンテキストメニューの設定
        self._setup_menu()

        # トレイアイコンを表示
        self._tray_icon.show()

    def _setup_icons(self) -> None:
        """アイコンリソースをセットアップします。"""
        self._icons = {}
        icons_dir = Path(__file__).parent.parent.parent / "resources" / "icons"

        # アイコンファイルのマッピング
        icon_files = {
            ConnectionQuality.EXCELLENT.value: "excellent.png",
            ConnectionQuality.GOOD.value: "good.png",
            ConnectionQuality.FAIR.value: "fair.png",
            ConnectionQuality.POOR.value: "poor.png",
            ConnectionQuality.UNKNOWN.value: "unknown.png",
        }

        # アイコンをロード（ファイルが存在しない場合はデフォルトを使用）
        for quality, filename in icon_files.items():
            icon_path = icons_dir / filename
            if icon_path.exists():
                self._icons[quality] = QIcon(str(icon_path))
            else:
                # フォールバック: 空のアイコン
                self._icons[quality] = QIcon()

        # 初期アイコンを設定
        self.update_icon(ConnectionQuality.UNKNOWN.value)

    def _setup_menu(self) -> None:
        """コンテキストメニューをセットアップします。"""
        menu = QMenu()

        # 詳細情報アクション
        detail_action = QAction("詳細情報", self._app)
        detail_action.triggered.connect(self._show_details)
        menu.addAction(detail_action)

        # 設定アクション
        settings_action = QAction("設定", self._app)
        settings_action.triggered.connect(self._show_settings)
        menu.addAction(settings_action)

        menu.addSeparator()

        # 終了アクション
        quit_action = QAction("終了", self._app)
        quit_action.triggered.connect(self._quit_app)
        menu.addAction(quit_action)

        self._tray_icon.setContextMenu(menu)

    def show_tooltip(self, stats: NetworkStats, metrics: StabilityMetrics) -> None:
        """
        ツールチップを表示します。

        Args:
            stats: ネットワーク統計情報
            metrics: 安定性メトリクス
        """
        tooltip_text = self._format_tooltip(stats, metrics)
        self._tray_icon.setToolTip(tooltip_text)

    def update_icon(self, quality: str) -> None:
        """
        トレイアイコンを品質に応じて更新します。

        Args:
            quality: 接続品質（Excellent/Good/Fair/Poor/Unknown）
        """
        if quality != self._current_quality:
            self._current_quality = quality
            icon = self._icons.get(quality, self._icons[ConnectionQuality.UNKNOWN.value])
            self._tray_icon.setIcon(icon)

    def _format_tooltip(self, stats: NetworkStats, metrics: StabilityMetrics) -> str:
        """
        ツールチップのテキストをフォーマットします。

        Args:
            stats: ネットワーク統計情報
            metrics: 安定性メトリクス

        Returns:
            フォーマットされたツールチップテキスト
        """
        return f"""WiFi Speed Monitor
━━━━━━━━━━━━━━━━
📡 {stats.ssid or 'Unknown Network'}
⬇️ {stats.download_speed:.1f} Mbps
⬆️ {stats.upload_speed:.1f} Mbps
⏱️ {stats.latency:.0f} ms
📊 {metrics.connection_quality}
━━━━━━━━━━━━━━━━
Stability: {metrics.consistency_score:.0f}%
Jitter: {metrics.jitter:.1f} ms""".strip()

    def _show_details(self) -> None:
        """詳細情報ウィンドウを表示します（将来実装）。"""
        self._tray_icon.showMessage(
            "WiFi Speed Monitor",
            "詳細情報機能は今後実装予定です",
            QSystemTrayIcon.MessageIcon.Information,
            2000,
        )

    def _show_settings(self) -> None:
        """設定ウィンドウを表示します（将来実装）。"""
        self._tray_icon.showMessage(
            "WiFi Speed Monitor",
            "設定機能は今後実装予定です",
            QSystemTrayIcon.MessageIcon.Information,
            2000,
        )

    def _quit_app(self) -> None:
        """アプリケーションを終了します。"""
        self._tray_icon.hide()
        self._app.quit()

    def exec(self) -> int:
        """
        アプリケーションのイベントループを開始します。

        Returns:
            アプリケーションの終了コード
        """
        return self._app.exec()

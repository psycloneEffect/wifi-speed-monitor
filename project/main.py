"""
Speed Finder - WiFi速度モニタリングアプリ
エントリーポイント
"""
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from project.adapters.network_adapter import PsutilNetworkProvider
from project.adapters.ui_adapter import TrayUIAdapter
from project.core.constants import DEFAULT_MONITOR_INTERVAL
from project.services.analyzer import StabilityAnalyzerService
from project.services.monitor import NetworkMonitorService


def main() -> int:
    """
    アプリケーションのメインエントリーポイント。

    Returns:
        アプリケーションの終了コード
    """
    # PyQt6アプリケーションの初期化
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # ウィンドウがなくても実行を継続

    # 依存性注入によるオニオンアーキテクチャの構築
    # 外側から内側へ組み立てる

    # Infrastructure Layer
    network_provider = PsutilNetworkProvider()
    ui_presenter = TrayUIAdapter(app)

    # Application Layer
    analyzer = StabilityAnalyzerService()
    monitor = NetworkMonitorService(
        provider=network_provider,
        analyzer=analyzer,
        history_size=60,  # 60データポイントの履歴
    )

    def update_ui() -> None:
        """UIを定期的に更新する処理"""
        # 統計情報を収集
        stats = monitor.collect_stats()

        if stats is not None:
            # 安定性メトリクスを取得
            metrics = monitor.get_stability_metrics()

            # UIを更新
            ui_presenter.show_tooltip(stats, metrics)
            ui_presenter.update_icon(metrics.connection_quality)

    # 定期的にUIを更新するタイマーを設定
    timer = QTimer()
    timer.timeout.connect(update_ui)
    timer.start(DEFAULT_MONITOR_INTERVAL * 1000)  # ミリ秒に変換

    # 初回更新
    update_ui()

    print("Speed Finder started...")
    print("System tray icon should be visible.")
    print("Right-click the icon for options.")

    # PyQt6のイベントループを開始
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

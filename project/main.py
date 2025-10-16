"""
Speed Finder - WiFi速度モニタリングアプリ
エントリーポイント
"""
import time
from adapters.network_adapter import PsutilNetworkProvider
from adapters.ui_adapter import TrayUIAdapter
from services.monitor import NetworkMonitorService
from services.analyzer import StabilityAnalyzerService


def main():
    """アプリケーションのメインエントリーポイント"""
    # 依存性注入によるオニオンアーキテクチャの構築
    # 外側から内側へ組み立てる
    
    # Infrastructure Layer
    network_provider = PsutilNetworkProvider()
    ui_presenter = TrayUIAdapter()
    
    # Application Layer
    analyzer = StabilityAnalyzerService()
    monitor = NetworkMonitorService(
        provider=network_provider,
        analyzer=analyzer,
        history_size=60  # 60データポイントの履歴
    )
    
    print("Speed Finder started...")
    print("Monitoring network... (Press Ctrl+C to stop)")
    
    try:
        # メインループ（TODO: PyQt6のイベントループに置き換え）
        while True:
            # 統計情報を収集
            stats = monitor.collect_stats()
            
            # 安定性メトリクスを取得
            metrics = monitor.get_stability_metrics()
            
            # UIを更新
            ui_presenter.show_tooltip(stats, metrics)
            ui_presenter.update_icon(metrics.connection_quality)
            
            # 10秒待機
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\nSpeed Finder stopped.")


if __name__ == "__main__":
    main()

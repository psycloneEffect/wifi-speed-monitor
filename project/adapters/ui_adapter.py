"""
UIアダプター実装（PyQt6）
"""
# TODO: PyQt6実装
# from PyQt6.QtWidgets import QSystemTrayIcon, QApplication
# from PyQt6.QtCore import QTimer
from core.interfaces import IUIPresenter
from core.models import NetworkStats, StabilityMetrics


class TrayUIAdapter(IUIPresenter):
    """システムトレイUI実装"""
    
    def __init__(self):
        # TODO: QSystemTrayIconの初期化
        pass
    
    def show_tooltip(self, stats: NetworkStats, metrics: StabilityMetrics) -> None:
        """ツールチップを表示"""
        tooltip_text = self._format_tooltip(stats, metrics)
        # TODO: QSystemTrayIcon.setToolTip(tooltip_text)
        print(f"Tooltip: {tooltip_text}")
    
    def update_icon(self, quality: str) -> None:
        """トレイアイコンを更新"""
        # TODO: 品質に応じたアイコンに変更
        print(f"Icon updated: {quality}")
    
    def _format_tooltip(self, stats: NetworkStats, metrics: StabilityMetrics) -> str:
        """ツールチップのテキストをフォーマット"""
        return f"""
WiFi Monitor
━━━━━━━━━━━━━━━━
📡 {stats.ssid or 'Unknown Network'}
⬇️ {stats.download_speed:.1f} Mbps
⬆️ {stats.upload_speed:.1f} Mbps
⏱️ {stats.latency:.0f} ms
📊 {metrics.connection_quality}
━━━━━━━━━━━━━━━━
Stability: {metrics.consistency_score:.0f}%
Jitter: {metrics.jitter:.1f} ms
        """.strip()

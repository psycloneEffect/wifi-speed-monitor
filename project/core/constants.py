"""
Core constants for network monitoring.

This module defines threshold values, default settings, and configuration constants
used throughout the application for network quality assessment.
"""

# ==========================================
# Latency Thresholds (milliseconds)
# ==========================================
LATENCY_EXCELLENT = 50  # <= 50ms: Excellent
LATENCY_GOOD = 100  # <= 100ms: Good
LATENCY_FAIR = 200  # <= 200ms: Fair
# > 200ms: Poor

# ==========================================
# Jitter Thresholds (milliseconds)
# ==========================================
JITTER_EXCELLENT = 10  # <= 10ms: Excellent
JITTER_GOOD = 30  # <= 30ms: Good
JITTER_FAIR = 50  # <= 50ms: Fair
# > 50ms: Poor

# ==========================================
# Packet Loss Thresholds (percentage)
# ==========================================
PACKET_LOSS_EXCELLENT = 0.5  # <= 0.5%: Excellent
PACKET_LOSS_GOOD = 2.0  # <= 2.0%: Good
PACKET_LOSS_FAIR = 5.0  # <= 5.0%: Fair
# > 5.0%: Poor

# ==========================================
# Download Speed Thresholds (Mbps)
# ==========================================
DOWNLOAD_SPEED_EXCELLENT = 100.0  # >= 100 Mbps: Excellent
DOWNLOAD_SPEED_GOOD = 50.0  # >= 50 Mbps: Good
DOWNLOAD_SPEED_FAIR = 10.0  # >= 10 Mbps: Fair
# < 10 Mbps: Poor

# ==========================================
# Upload Speed Thresholds (Mbps)
# ==========================================
UPLOAD_SPEED_EXCELLENT = 50.0  # >= 50 Mbps: Excellent
UPLOAD_SPEED_GOOD = 20.0  # >= 20 Mbps: Good
UPLOAD_SPEED_FAIR = 5.0  # >= 5 Mbps: Fair
# < 5 Mbps: Poor

# ==========================================
# Signal Strength Thresholds (dBm for WiFi)
# ==========================================
SIGNAL_STRENGTH_EXCELLENT = -50  # >= -50 dBm: Excellent
SIGNAL_STRENGTH_GOOD = -60  # >= -60 dBm: Good
SIGNAL_STRENGTH_FAIR = -70  # >= -70 dBm: Fair
# < -70 dBm: Poor

# ==========================================
# Monitoring Settings
# ==========================================
DEFAULT_MONITOR_INTERVAL = 10  # seconds between measurements
DEFAULT_HISTORY_SIZE = 60  # number of data points to retain
DEFAULT_SPEEDTEST_INTERVAL = 300  # seconds (5 min) between speed tests
DEFAULT_PING_COUNT = 10  # number of pings per measurement

# ==========================================
# Timeout Settings
# ==========================================
NETWORK_TIMEOUT = 5  # seconds for network operations
SPEEDTEST_TIMEOUT = 30  # seconds for speed test
PING_TIMEOUT = 3  # seconds per ping

# ==========================================
# UI Update Settings
# ==========================================
UI_UPDATE_INTERVAL = 1000  # milliseconds between UI updates
TOOLTIP_DISPLAY_DURATION = 5000  # milliseconds to show tooltip

# ==========================================
# Data Retention
# ==========================================
MAX_HISTORY_SIZE = 3600  # maximum data points (10 hours at 10s interval)
MIN_HISTORY_SIZE = 10  # minimum data points for analysis

# ==========================================
# Quality Score Weights
# ==========================================
WEIGHT_LATENCY = 0.3  # latency contribution to quality score
WEIGHT_JITTER = 0.2  # jitter contribution to quality score
WEIGHT_PACKET_LOSS = 0.3  # packet loss contribution to quality score
WEIGHT_SPEED = 0.2  # speed contribution to quality score

# ==========================================
# Network Measurement Settings
# ==========================================
DEFAULT_PING_HOST = "8.8.8.8"  # Google DNS
FALLBACK_PING_HOSTS = [
    "8.8.8.8",  # Google DNS
    "1.1.1.1",  # Cloudflare DNS
    "208.67.222.222",  # OpenDNS
]
MAX_SPEEDTEST_RETRY = 3  # maximum retry attempts for speed test

# ==========================================
# Application Info
# ==========================================
APP_NAME = "Speed Finder"
APP_VERSION = "0.1.0"
MIN_PYTHON_VERSION = (3, 11)

# ==========================================
# Logging Settings
# ==========================================
DEFAULT_LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
MAX_LOG_FILE_SIZE_MB = 10
MAX_LOG_FILE_COUNT = 5

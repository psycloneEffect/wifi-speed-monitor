# Speed Finder 🍛

WiFiネットワークの速度と安定性をリアルタイムでモニタリングする常駐型アプリケーション

## 📋 概要

Speed Finderは、現在接続中のWiFiネットワークの性能を継続的に監視し、システムトレイからマウスオーバーで詳細情報を表示するPythonアプリケーションです。

### 主な機能

- ⬇️⬆️ ダウンロード/アップロード速度の測定
- ⏱️ レイテンシ（ping）の監視
- 📊 接続安定性の分析
- 🔔 システムトレイ常駐
- 💡 マウスオーバーでの情報表示

## 🏗️ アーキテクチャ

このプロジェクトは**オニオンアーキテクチャ**を採用しています。依存関係は外側から内側への一方向のみです。

```py
┌─────────────────────────────────────────────┐
│         Infrastructure Layer                │
│  (adapters/ - PyQt6, psutil, speedtest)    │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │     Application Layer                 │ │
│  │  (services/ - monitor, analyzer)      │ │
│  │                                       │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │      Domain Core                │ │ │
│  │  │  (core/ - models, interfaces)   │ │ │
│  │  │  - 純粋なPython                  │ │ │
│  │  │  - 依存関係なし                  │ │ │
│  │  └─────────────────────────────────┘ │ │
│  │                                       │ │
│  └───────────────────────────────────────┘ │
│                                             │
└─────────────────────────────────────────────┘
```

### 依存の方向

```py
Infrastructure → Application → Core
   (外側)                      (内側)
```

## 📁 プロジェクト構造

```py
speed-finder/
│
├── core/                       # ドメインコア層（依存なし）
│   ├── __init__.py
│   ├── models.py              # データモデル（NetworkStats, StabilityMetrics）
│   └── interfaces.py          # 抽象インターフェース（ABC）
│
├── services/                   # アプリケーション層（coreに依存）
│   ├── __init__.py
│   ├── monitor.py             # ネットワークモニタリングサービス
│   └── analyzer.py            # 安定性分析サービス
│
├── adapters/                   # インフラストラクチャ層（すべてに依存可）
│   ├── __init__.py
│   ├── network_adapter.py     # psutil/speedtest実装
│   └── ui_adapter.py          # PyQt6 UIトレイ実装
│
├── tests/                      # テストコード
│   └── __init__.py
│
├── main.py                     # エントリーポイント
├── requirements.txt            # 依存パッケージ
├── .gitignore
├── AGENTS.md                   # AI Agent開発ガイド
└── README.md                   # このファイル
```

## 🔧 セットアップ

### 1. Python環境の準備

```powershell
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
.\venv\Scripts\Activate.ps1

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 2. 実行

```powershell
python main.py
```

## 🧪 テスト

```powershell
# テストの実行
pytest

# カバレッジ付きテスト
pytest --cov=. --cov-report=html
```

## 📦 各レイヤーの責務

### Core Layer（中心層）

- **責務**: ドメインモデルとビジネスルールの定義
- **依存**: なし（純粋Python）
- **含まれるもの**:
  - `NetworkStats`: ネットワーク統計データモデル
  - `StabilityMetrics`: 安定性メトリクスモデル
  - `INetworkProvider`: ネットワーク情報取得インターフェース
  - `IStabilityAnalyzer`: 安定性分析インターフェース
  - `IUIPresenter`: UI表示インターフェース

### Application Layer（アプリケーション層）

- **責務**: ビジネスロジックのオーケストレーション
- **依存**: `core`のみ
- **含まれるもの**:
  - `NetworkMonitorService`: モニタリングロジック
  - `StabilityAnalyzerService`: 統計分析と品質判定

### Infrastructure Layer（インフラ層）

- **責務**: 外部ライブラリとの統合
- **依存**: `core`, `services`
- **含まれるもの**:
  - `PsutilNetworkProvider`: psutilを使ったネットワーク情報取得
  - `TrayUIAdapter`: PyQt6によるシステムトレイUI

## 🎯 依存性注入パターン

```python
# main.pyでの組み立て例
# 外側から内側へ依存を注入

# 1. Infrastructure（最外層）
network_provider = PsutilNetworkProvider()
ui_presenter = TrayUIAdapter()

# 2. Application（中間層）
analyzer = StabilityAnalyzerService()
monitor = NetworkMonitorService(
    provider=network_provider,  # 注入
    analyzer=analyzer
)

# 3. 実行
stats = monitor.collect_stats()
metrics = monitor.get_stability_metrics()
ui_presenter.show_tooltip(stats, metrics)
```

## 🌟 アーキテクチャの利点

1. **テスタビリティ**: coreレイヤーは外部依存なしでテスト可能
2. **柔軟性**: ライブラリ変更が容易（例: PyQt6 → PySide6）
3. **保守性**: 依存関係が一方向のみで理解しやすい
4. **拡張性**: 新機能追加時も既存コアに影響なし

## 🚧 TODO

- [ ] PyQt6によるシステムトレイUI実装
- [ ] speedtest-cliを使った正確な速度測定
- [ ] ping3によるレイテンシ測定
- [ ] Windows netshコマンドでのSSID/信号強度取得
- [ ] 設定ファイル対応（監視間隔など）
- [ ] ロギング実装
- [ ] パッケージング（exe化）

## 📝 ライセンス

MIT License

## 👤 作者

せんぱい 🍛✨

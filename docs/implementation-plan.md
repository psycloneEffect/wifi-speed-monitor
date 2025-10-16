# Speed Finder 実装計画

## 📋 プロジェクト概要

**プロジェクト名**: Speed Finder

**目的**: WiFiネットワークの速度と安定性をリアルタイムでモニタリングし、システムトレイから情報を表示する常駐型デスクトップアプリケーション

**アーキテクチャ**: オニオンアーキテクチャ

**対象OS**: Windows（優先）、macOS、Linux（将来対応）

**開発期間**: 2025年10月 〜 2025年12月（予定）

## 🎯 主要機能

### Phase 1: コア機能（MVP）

- [x] プロジェクト構造の構築
- [x] オニオンアーキテクチャの実装
- [ ] ネットワーク統計情報の取得
- [ ] 速度測定機能
- [ ] レイテンシ測定機能
- [ ] 基本的なシステムトレイUI
- [ ] ツールチップでの情報表示

### Phase 2: 安定性分析

- [ ] ジッター計算
- [ ] パケットロス測定
- [ ] 接続品質の判定
- [ ] 統計履歴の保存

### Phase 3: UI/UX改善

- [ ] アイコンの品質別表示
- [ ] 詳細情報ウィンドウ
- [ ] グラフ表示機能
- [ ] 設定画面

### Phase 4: 高度な機能

- [ ] 自動速度テスト
- [ ] 通知機能
- [ ] ログ記録
- [ ] データエクスポート

## 📅 タイムライン

### Week 1-2: 基盤構築 ✅

**完了項目:**

- [x] プロジェクト初期化
- [x] オニオンアーキテクチャ実装
- [x] CI/CD パイプライン構築
- [x] ドキュメント整備
- [x] 開発環境セットアップ

### Week 3-4: ネットワーク測定機能

**目標:**

- [ ] psutil を使った基本的なネットワーク統計取得
- [ ] speedtest-cli 統合
- [ ] ping3 でのレイテンシ測定
- [ ] Windows netsh による WiFi情報取得
- [ ] `core/enums.py` の追加（ConnectionQuality, NetworkType等）
- [ ] `core/constants.py` の追加（閾値定数、デフォルト設定）

**成果物:**

- `adapters/network_adapter.py` の完全実装
- `core/enums.py` と `core/constants.py` の作成
- ネットワーク測定のユニットテスト
- 測定精度の検証

### Week 5-6: 安定性分析エンジン

**目標:**

- [ ] 統計履歴の管理
- [ ] ジッター計算アルゴリズム
- [ ] 一貫性スコア算出
- [ ] 接続品質判定ロジック

**成果物:**

- `services/analyzer.py` の完全実装
- 分析アルゴリズムのテスト
- パフォーマンス最適化

### Week 7-8: システムトレイUI

**目標:**

- [ ] PyQt6 によるシステムトレイアイコン
- [ ] ツールチップの実装
- [ ] メニュー機能
- [ ] アイコンの品質別表示

**成果物:**

- `adapters/ui_adapter.py` の完全実装
- UIのモックアップとデザイン
- ユーザビリティテスト

### Week 9-10: 統合とテスト

**目標:**

- [ ] 全コンポーネントの統合
- [ ] エンドツーエンドテスト
- [ ] パフォーマンステスト
- [ ] メモリリーク検証

**成果物:**

- 統合テストスイート
- パフォーマンスレポート
- バグ修正

### Week 11-12: ポリッシュとリリース準備

**目標:**

- [ ] UI/UX改善
- [ ] エラーハンドリング強化
- [ ] ドキュメント完成
- [ ] インストーラー作成

**成果物:**

- v1.0.0 リリース
- ユーザーマニュアル
- インストールガイド

## 🏗️ プロジェクト構造とアーキテクチャ設計

### ディレクトリ構成の方針

#### オニオンアーキテクチャの層構造

```
project/
├── core/              # ドメインコア層（最内側・依存なし）
│   ├── models.py      # データモデル
│   ├── interfaces.py  # 抽象インターフェース
│   ├── enums.py       # 列挙型定義（Week 3-4で追加）
│   ├── constants.py   # 定数定義（Week 3-4で追加）
│   └── exceptions.py  # カスタム例外（必要に応じて）
│
├── services/          # アプリケーション層（coreに依存）
│   ├── monitor.py
│   ├── analyzer.py
│   └── (utils.py)     # サービス層で使うユーティリティ（最小限）
│
└── adapters/          # インフラ層（外側・すべてに依存可）
    ├── network_adapter.py
    ├── ui_adapter.py
    └── (helpers.py)   # アダプター層のヘルパー（最小限）
```

### Shared層に関する設計判断

#### ❌ 避けるべきパターン

**ルート直下のshared層は作成しない**

```
# アンチパターン
project/
├── shared/            # ❌ オニオン構造を崩す
│   ├── constants/
│   ├── enums/
│   ├── interfaces/
│   └── utils/
```

**理由:**

- オニオンの層構造が不明確になる
- 依存関係が複雑化（どこからでもアクセス可能になる）
- 「shared」は責務が曖昧で肥大化しやすい

#### ✅ 推奨パターン

**適切な層に配置する**

1. **定数・列挙型 → `core/` に配置**
   - ドメインレベルの定数
   - ビジネスルールに関する列挙型
   - すべての層から参照可能（内側なので）

2. **インターフェース → `core/interfaces.py`**
   - 既存ファイルで管理
   - 新規追加時も同ファイルに集約

3. **ユーティリティ → 使用する層に配置**
   - ネットワーク系 → `adapters/`
   - ビジネスロジック系 → `services/`
   - ドメイン系 → `core/`

### 段階的な追加計画

#### Phase 1（Week 1-2）: 最小構成 ✅ 完了

```
core/
├── models.py          # データモデル
└── interfaces.py      # インターフェース
```

#### Phase 2（Week 3-4）: 定数・列挙型追加

```python
# core/enums.py を追加
from enum import Enum

class ConnectionQuality(Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"
    UNKNOWN = "Unknown"

class NetworkType(Enum):
    WIFI = "wifi"
    ETHERNET = "ethernet"
    MOBILE = "mobile"

# core/constants.py を追加
# 品質判定の閾値
LATENCY_EXCELLENT = 50    # ms
LATENCY_GOOD = 100
LATENCY_FAIR = 200

JITTER_EXCELLENT = 10
JITTER_GOOD = 30
JITTER_FAIR = 50

# デフォルト設定
DEFAULT_MONITOR_INTERVAL = 10  # 秒
DEFAULT_HISTORY_SIZE = 60
DEFAULT_SPEEDTEST_INTERVAL = 1800  # 30分
```

**追加タイミング:**

- [ ] Week 3-4: `core/enums.py` 作成
- [ ] Week 3-4: `core/constants.py` 作成
- [ ] Week 5-6: `core/exceptions.py` 作成（必要に応じて）

#### Phase 3（Week 5-6以降）: カスタム例外

```python
# core/exceptions.py
class SpeedFinderError(Exception):
    """ベース例外"""
    pass

class NetworkError(SpeedFinderError):
    """ネットワーク関連エラー"""
    pass

class MeasurementError(SpeedFinderError):
    """測定エラー"""
    pass
```

### コーディング規約（実装時の注意事項）

#### 循環インポート回避

- **TYPE_CHECKINGを使用しない**
- **1ファイル1クラスの原則**を遵守
- ファイル名 = クラス名（小文字）

**例:**

```
core/
├── network_stats.py      # NetworkStatsクラス
├── stability_metrics.py  # StabilityMetricsクラス
└── connection_quality.py # ConnectionQualityクラス
```

#### コードの分割基準

- **PEP8準拠**
- **80行（コメント除く）を超えたら分割**
- 内部メソッドへのリファクタリング

**例:**

```python
class NetworkMonitorService:
    def collect_and_analyze(self):
        # 80行超える場合
        stats = self._collect_stats()      # 分割
        metrics = self._analyze_metrics()  # 分割
        return stats, metrics

    def _collect_stats(self):
        # 実装
        pass

    def _analyze_metrics(self):
        # 実装
        pass
```

#### 型ヒント

- **Optionalではなく、Union を優先**

```python
# ❌ 避ける
from typing import Optional
def get_ssid(self) -> Optional[str]:
    pass

# ✅ 推奨
from typing import Union
def get_ssid(self) -> Union[str, None]:
    pass
```

#### ハードコーディング禁止

- すべての定数は `core/constants.py` に集約
- マジックナンバーは使わない

```python
# ❌ 避ける
if latency < 50:
    quality = "Excellent"

# ✅ 推奨
from project.core.constants import LATENCY_EXCELLENT
if latency < LATENCY_EXCELLENT:
    quality = ConnectionQuality.EXCELLENT
```

#### 未使用インポートの削除

- pyファイル更新後、必ず確認
- CI/CDでruffとflake8が自動チェック

## 🏗️ 実装の優先順位

### P0: 最優先（MVP に必須）

1. ネットワーク統計の基本取得
2. システムトレイアイコン表示
3. ツールチップでの情報表示
4. 安定動作の確保

### P1: 重要（v1.0 に含める）

1. 速度測定機能
2. レイテンシ測定
3. 安定性分析
4. 設定機能

### P2: 改善（v1.1+ で対応）

1. グラフ表示
2. 詳細統計
3. 通知機能
4. データエクスポート

### P3: 将来検討

1. macOS/Linux対応
2. モバイルアプリ連携
3. クラウド同期
4. 高度な分析機能

## 🔧 技術的な実装詳細

### Core Layer 実装

#### `core/models.py`

```python
@dataclass
class NetworkStats:
    """ネットワーク統計情報"""
    download_speed: float
    upload_speed: float
    latency: float
    packet_loss: float
    timestamp: datetime
    ssid: Optional[str]
    signal_strength: Optional[int]
```

**実装タスク:**

- [x] データクラス定義
- [ ] バリデーション追加
- [ ] シリアライゼーション対応

#### `core/interfaces.py`

**実装タスク:**

- [x] インターフェース定義
- [ ] ドキュメント追加
- [ ] 型ヒント完全化

### Services Layer 実装

#### `services/monitor.py`

**実装タスク:**

- [x] 基本構造
- [ ] 履歴管理機能
- [ ] 定期実行ロジック
- [ ] エラーハンドリング
- [ ] パフォーマンス最適化

#### `services/analyzer.py`

**実装タスク:**

- [x] 基本構造
- [ ] ジッター計算
- [ ] 一貫性スコア算出
- [ ] 品質判定アルゴリズム
- [ ] 統計分析機能

### Adapters Layer 実装

#### `adapters/network_adapter.py`

**実装タスク:**

- [x] 基本構造
- [ ] psutil 完全統合
- [ ] speedtest-cli 統合
- [ ] ping3 統合
- [ ] Windows netsh 統合
- [ ] プラットフォーム別実装

**実装メモ:**

```python
# Windows: netsh コマンド実行
subprocess.run(['netsh', 'wlan', 'show', 'interfaces'])

# speedtest-cli 使用
import speedtest
st = speedtest.Speedtest()
st.download()
st.upload()

# ping3 使用
from ping3 import ping
ping('8.8.8.8')
```

#### `adapters/ui_adapter.py`

**実装タスク:**

- [ ] QSystemTrayIcon 実装
- [ ] ツールチップ表示
- [ ] コンテキストメニュー
- [ ] アイコン動的変更
- [ ] イベントハンドリング

**UI設計:**

```
システムトレイアイコン
├── 緑: Excellent (Latency < 50ms, 安定)
├── 黄: Good/Fair (50-100ms)
└── 赤: Poor (> 100ms または不安定)

ツールチップ:
━━━━━━━━━━━━━━━━
📡 WiFi Name
⬇️ 100.5 Mbps
⬆️ 50.2 Mbps
⏱️ 25 ms
📊 Excellent
━━━━━━━━━━━━━━━━
安定性: 95%
ジッター: 2.5ms
```

## 🧪 テスト戦略

### ユニットテスト

**カバレッジ目標**: 80% 以上

**重点テスト:**

- [ ] Core モデルのバリデーション
- [ ] Services の計算ロジック
- [ ] エラーハンドリング

### インテグレーションテスト

**テスト項目:**

- [ ] ネットワークアダプターと実際のネットワーク
- [ ] サービス層の連携
- [ ] UI とバックエンドの統合

### E2Eテスト

**シナリオ:**

1. アプリケーション起動
2. ネットワーク統計取得
3. ツールチップ表示
4. 設定変更
5. アプリケーション終了

### パフォーマンステスト

**測定項目:**

- メモリ使用量（目標: < 50MB）
- CPU使用率（目標: < 5% 平均）
- 起動時間（目標: < 3秒）
- レスポンス時間（目標: < 100ms）

## 📚 ドキュメント計画

### ユーザー向け

- [x] README.md
- [ ] インストールガイド (`docs/guide/installation.md`)
- [ ] 使い方ガイド (`docs/guide/usage.md`)
- [ ] FAQ
- [ ] トラブルシューティング

### 開発者向け

- [x] CONTRIBUTING.md
- [ ] アーキテクチャドキュメント (`docs/dev/architecture.md`)
- [ ] API リファレンス
- [ ] 開発環境セットアップ (`docs/dev/setup.md`)

### API ドキュメント

- [ ] Core API (`docs/api/core.md`)
- [ ] Services API (`docs/api/services.md`)
- [ ] Adapters API (`docs/api/adapters.md`)

## 🚀 デプロイ計画

### パッケージング

**Windows:**

```powershell
# PyInstaller で exe 化
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

**配布方法:**

- GitHub Releases
- Microsoft Store（将来）
- Chocolatey パッケージ（将来）

### インストーラー

**使用ツール:**

- Inno Setup (Windows)
- 自動起動設定
- アンインストーラー

### 更新機能

- [ ] バージョンチェック機能
- [ ] 自動更新通知
- [ ] GitHub Releases 連携

## 🔐 セキュリティ考慮事項

### 実装時の注意点

1. **WiFi情報の取り扱い**
   - SSID は機密情報として扱う
   - パスワードは絶対に取得しない
   - ログに機密情報を含めない

2. **ネットワーク通信**
   - speedtest サーバーへの接続は HTTPS
   - 外部への情報送信は行わない（完全ローカル動作）

3. **依存関係**
   - 定期的な脆弱性スキャン
   - Dependabot による自動更新

4. **権限**
   - 必要最小限の権限で動作
   - 管理者権限は不要

## 📊 成功指標

### 技術指標

- [ ] テストカバレッジ > 80%
- [ ] 全リントエラー解消
- [ ] 型チェック100%パス
- [ ] ドキュメント完成度 > 90%

### パフォーマンス指標

- [ ] メモリ使用量 < 50MB
- [ ] CPU使用率 < 5%（平均）
- [ ] 起動時間 < 3秒
- [ ] クラッシュ発生率 < 0.1%

### ユーザビリティ指標

- [ ] インストール成功率 > 95%
- [ ] 初回起動成功率 > 99%
- [ ] 使い方の理解度 > 80%

## 🐛 既知の課題と対応

### 技術的課題

1. **Windows netsh の出力パース**
   - 言語依存の問題
   - 対策: 英語ロケールで実行

2. **speedtest の実行時間**
   - 測定に時間がかかる（10-30秒）
   - 対策: バックグラウンドスレッドで実行

3. **PyQt6 のパッケージサイズ**
   - 配布ファイルが大きくなる
   - 対策: 最小限のモジュールのみバンドル

### 今後の検討事項

- [ ] macOS/Linux 対応
- [ ] 設定ファイルのフォーマット
- [ ] 多言語対応
- [ ] テーマ機能

## 🎉 マイルストーン

### v0.1.0 - MVP (2025年11月)

- 基本的なネットワーク統計表示
- システムトレイアイコン
- ツールチップ表示

### v0.2.0 - 安定性分析 (2025年11月中旬)

- ジッター計算
- 品質判定
- 履歴管理

### v0.5.0 - UI改善 (2025年12月)

- 詳細ウィンドウ
- グラフ表示
- 設定画面

### v1.0.0 - 正式リリース (2025年12月末)

- 全機能実装
- ドキュメント完成
- パッケージング完了

## 📝 次のアクション

### 今週のタスク

1. [ ] `network_adapter.py` の実装開始
   - psutil によるネットワーク統計取得
   - Windows netsh 統合

2. [ ] 基本的なテストの作成
   - モック使用したユニットテスト
   - CI での自動実行

3. [ ] ドキュメント作成
   - インストールガイド
   - アーキテクチャドキュメント

### 来週のタスク

1. [ ] speedtest-cli 統合
2. [ ] ping3 によるレイテンシ測定
3. [ ] 統合テスト作成

## 🔗 参考リンク

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [psutil Documentation](https://psutil.readthedocs.io/)
- [speedtest-cli GitHub](https://github.com/sivel/speedtest-cli)
- [ping3 GitHub](https://github.com/kyan001/ping3)
- [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)

---

### Copilotに理解してほしいこと

- TYPECHECKを使用しなくても循環インポートにならない構成で実装してください。
- 上述の循環インポートを回避するため、1ファイル1クラス、pyファイル名＝クラス名の実装を遵守してください。
- PEP8準拠のもと、80行 (コメント除く) を超えるコードは分割し、別メソッド(内部メソッド)にリファクタリングしてください。
- pyファイル更新後、未使用インポートがあったら削除してください。
- Optionalではなく、可能な限りUnionを優先的に使用してください。
- ハードコーディングは避け、

**最終更新**: 2025年10月16日

**ステータス**: Phase 1 進行中 🚀

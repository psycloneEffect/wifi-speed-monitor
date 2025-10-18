# Contributing to Speed Finder 🍛

Speed Finderへの貢献に興味を持っていただき、ありがとうございます！✨

## 📋 目次

- [行動規範](#行動規範)
- [質問がある場合](#質問がある場合)
- [貢献の方法](#貢献の方法)
- [開発環境のセットアップ](#開発環境のセットアップ)
- [コーディング規約](#コーディング規約)
- [プルリクエストの流れ](#プルリクエストの流れ)
- [コミットメッセージ規約](#コミットメッセージ規約)

## 🤝 行動規範

このプロジェクトでは、すべての参加者に対して尊重と礼儀を期待しています。

- 建設的なフィードバックを提供する
- 異なる視点や経験を尊重する
- プロジェクトとコミュニティの最善の利益を考える

## ❓ 質問がある場合

質問がある場合は、以下の方法で聞いてください：

1. [GitHub Discussions](../../discussions) で質問を投稿
2. 既存の [Issues](../../issues) を検索
3. 新しい Issue を作成（適切なテンプレートを使用）

## 🎯 貢献の方法

### バグ報告

バグを見つけた場合：

1. [既存のIssue](../../issues) を検索して重複を避ける
2. バグ報告テンプレートを使用して新しいIssueを作成
3. 再現手順、期待される動作、実際の動作を明確に記載

### 機能リクエスト

新機能を提案する場合：

1. [既存のIssue](../../issues) を検索
2. 機能リクエストテンプレートを使用
3. ユースケースと期待される効果を説明

### コード貢献

1. Issue を確認または作成
2. フォークしてブランチを作成
3. コードを書く
4. テストを追加
5. プルリクエストを作成

## 🛠️ 開発環境のセットアップ

```bash
# 1. リポジトリをフォーク & クローン
git clone https://github.com/YOUR_USERNAME/wifi-speed-monitor.git
cd wifi-speed-monitor

# 2. 仮想環境を作成
python -m venv venv

# 3. 仮想環境を有効化
# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

# 4. 依存関係をインストール
pip install -r requirements.txt

# 5. 開発用の追加パッケージをインストール
pip install -e .

# 6. pre-commitフックをセットアップ（推奨）
pip install pre-commit
pre-commit install
```

## 📝 コーディング規約

### Python スタイルガイド

- **PEP 8** に準拠
- **型ヒント** を使用（Python 3.10+）
- **Docstring** は Google スタイルで記述

```python
def calculate_speed(bytes_received: int, time_delta: float) -> float:
    """速度を計算します。

    Args:
        bytes_received: 受信したバイト数
        time_delta: 経過時間（秒）

    Returns:
        速度（Mbps）

    Raises:
        ValueError: time_deltaが0以下の場合
    """
    if time_delta <= 0:
        raise ValueError("time_delta must be positive")
    return (bytes_received * 8) / (time_delta * 1_000_000)
```

### アーキテクチャ規約

このプロジェクトは **オニオンアーキテクチャ** を採用しています：

```
Infrastructure → Application → Core
   (外側)                      (内側)
```

**依存の方向を守ること：**

- Core は外部依存を持たない
- Services は Core のみに依存
- Adapters はすべてに依存可能

### コードフォーマット

```bash
# 自動フォーマット
black project/ tests/

# リントチェック
flake8 project/ tests/
pylint project/

# 型チェック
mypy project/
```

## 🔄 プルリクエストの流れ

1. **ブランチを作成**

   ```bash
   git checkout -b feature/amazing-feature
   # または
   git checkout -b fix/bug-description
   ```

2. **変更をコミット**

   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

3. **テストを実行**

   ```bash
   pytest --cov=project
   ```

4. **プッシュ**

   ```bash
   git push origin feature/amazing-feature
   ```

5. **プルリクエストを作成**
   - PRテンプレートに従って記入
   - レビュアーを指定（自動割り当てされる場合もあり）

6. **レビューに対応**
   - フィードバックに基づいて修正
   - 追加コミットをプッシュ

7. **マージ**
   - レビュー承認後、メンテナーがマージ

## 💬 コミットメッセージ規約

[Conventional Commits](https://www.conventionalcommits.org/) に準拠：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type（必須）

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの動作に影響しない変更（フォーマット等）
- `refactor`: リファクタリング
- `perf`: パフォーマンス改善
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更

### 例

```bash
feat(core): add NetworkStats model

Closes #123

fix(adapters): resolve psutil import error

- Update import path
- Add error handling

docs(readme): update installation instructions
```

## ✅ プルリクエストのチェックリスト

- [ ] コードがフォーマットされている（`black`）
- [ ] リントエラーがない（`flake8`, `pylint`）
- [ ] 型チェックをパスする（`mypy`）
- [ ] テストを追加した
- [ ] すべてのテストがパスする
- [ ] ドキュメントを更新した
- [ ] コミットメッセージが規約に従っている
- [ ] CHANGELOG.mdを更新した（必要な場合）

## 🧪 テストの書き方

```python
# tests/test_monitor.py
import pytest
from project.services.monitor import NetworkMonitorService

class TestNetworkMonitorService:
    def test_collect_stats(self, mock_provider, mock_analyzer):
        """統計情報の収集をテスト"""
        monitor = NetworkMonitorService(
            provider=mock_provider,
            analyzer=mock_analyzer
        )
        stats = monitor.collect_stats()
        
        assert stats.download_speed > 0
        assert stats.upload_speed > 0
```

## 📚 参考資料

- [Python PEP 8 スタイルガイド](https://peps.python.org/pep-0008/)
- [Google Python スタイルガイド](https://google.github.io/styleguide/pyguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [オニオンアーキテクチャ](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)

## 🎉 貢献者

すべての貢献者に感謝します！🍛✨

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

---

質問や不明点がある場合は、遠慮なく Issue を作成してください！💫

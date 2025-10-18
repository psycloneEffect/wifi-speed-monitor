# GitHub Actions ワークフロー

このディレクトリには、Speed Finderプロジェクトの自動化ワークフローが含まれています。

## 📋 利用可能なワークフロー

### 1. 🔄 CI/CD Pipeline (`ci-cd.yml`)

**トリガー**: `main`, `develop` ブランチへのプッシュ、PR作成時、手動実行

**実行内容**:
- 🔍 **Lint & Code Quality**: flake8, pylint, black, isort
- 🔬 **Type Checking**: mypy による型チェック
- 🧪 **Tests**: 複数OS（Ubuntu, Windows, macOS）、Python 3.10-3.12でテスト実行
- 📊 **Coverage**: Codecov連携、HTML/XMLレポート生成
- 🔒 **Security Scan**: Bandit, Safety によるセキュリティチェック
- 📚 **Documentation**: MkDocsでドキュメントビルド
- 📦 **Package Build**: Wheelパッケージビルド

**使い方**:

```bash
# 手動実行
gh workflow run ci-cd.yml
```

### 2. ⚡ Pull Request Checks (`pr-check.yml`)

**トリガー**: PR作成、更新時

**実行内容**:
- ⚡ クイックバリデーション（変更ファイルのみ）
- 📊 カバレッジ閾値チェック（80%以上）
- 💬 PR自動コメント

**特徴**:
- 高速実行（変更ファイルのみチェック）
- PR作成者へのフィードバック

### 3. 🚀 Release (`release.yml`)

**トリガー**: `v*.*.*` 形式のタグプッシュ、手動実行

**実行内容**:
- 🏗️ パッケージビルド（Wheel, Source Distribution）
- 🪟 Windows実行ファイル生成（PyInstaller）
- 🎉 GitHub Release自動作成
- 📦 PyPI公開（オプション）
- 📢 リリース通知

**使い方**:

```bash
# タグを作成してプッシュ
git tag v1.0.0
git push origin v1.0.0

# または手動実行
gh workflow run release.yml -f version=v1.0.0
```

### 4. 📅 Scheduled Checks (`scheduled-checks.yml`)

**トリガー**: 毎日午前3時（UTC）、手動実行

**実行内容**:
- 🔐 依存関係の脆弱性チェック
- 📦 古い依存関係の検出
- 📊 カバレッジトレンド分析
- 🔗 ドキュメントリンク切れチェック
- 📋 日次ヘルスサマリー

**特徴**:
- 脆弱性発見時に自動Issue作成
- 定期的なプロジェクト健全性チェック

## 🔧 セットアップ

### 必要なシークレット

プロジェクト設定 → Secrets and variables → Actions で以下を設定:

#### PyPI公開用（オプション）

```
PYPI_API_TOKEN: PyPI APIトークン
```

取得方法:
1. <https://pypi.org/> でアカウント作成
2. Account settings → API tokens → Add API token
3. Token scope を「Entire account」または特定プロジェクトに設定

### Codecov連携（オプション）

1. <https://codecov.io/> でリポジトリ連携
2. 自動的にカバレッジレポートがアップロードされます

### ブランチ保護ルール

Settings → Branches → Add rule で設定推奨:

```
Branch name pattern: main
☑ Require a pull request before merging
☑ Require status checks to pass before merging
  - Quick Validation
  - Tests (Python 3.11, ubuntu-latest)
☑ Require conversation resolution before merging
```

## 📊 バッジ追加

README.mdに以下のバッジを追加できます:

```markdown
![CI/CD](https://github.com/YOUR_USERNAME/speed-finder/workflows/CI%2FCD%20Pipeline/badge.svg)
![Tests](https://github.com/YOUR_USERNAME/speed-finder/workflows/Pull%20Request%20Checks/badge.svg)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/speed-finder/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/speed-finder)
```

## 🎯 ワークフロー実行状況の確認

### GitHubウェブUI

```
リポジトリ → Actions タブ
```

### GitHub CLI

```bash
# 最新のワークフロー実行状況
gh run list

# 特定のワークフロー実行詳細
gh run view <run-id>

# ワークフローログ表示
gh run view <run-id> --log
```

## 🚨 トラブルシューティング

### ワークフローが失敗する場合

1. **Lintエラー**:

   ```bash
   # ローカルで修正
   black project/ tests/
   isort project/ tests/
   ```

2. **テスト失敗**:

   ```bash
   # ローカルでテスト実行
   pytest tests/ -v
   ```

3. **カバレッジ不足**:

   ```bash
   # カバレッジレポート確認
   pytest tests/ --cov=project --cov-report=html
   open htmlcov/index.html
   ```

### ワークフローのデバッグ

```yaml
# デバッグ用ステップを追加
- name: Debug info
  run: |
    echo "Python version: $(python --version)"
    echo "Pip version: $(pip --version)"
    pip list
```

## 📚 参考リンク

- [GitHub Actions ドキュメント](https://docs.github.com/en/actions)
- [Python CI/CD ベストプラクティス](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

## 🆕 更新履歴

- **2025-10-18**: 初期ワークフロー作成
  - CI/CD Pipeline
  - PR Checks
  - Release Automation
  - Scheduled Health Checks

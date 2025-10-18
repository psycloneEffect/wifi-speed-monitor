# GitHub Actions CI/CD セットアップ完了 🎉

## 📦 作成されたワークフロー

### 1. 🔄 **CI/CD Pipeline** (`ci-cd.yml`)
本格的な継続的インテグレーション/デプロイメントパイプライン

**7つのジョブ**:
- ✅ Lint & Code Quality (flake8, pylint, black, isort)
- ✅ Type Checking (mypy)
- ✅ Tests (Ubuntu/Windows/macOS × Python 3.10/3.11/3.12)
- ✅ Security Scan (Bandit, Safety)
- ✅ Documentation Build (MkDocs)
- ✅ Package Build (Wheel)
- ✅ Summary Report

**トリガー**: main/developブランチへのプッシュ、PR作成

---

### 2. ⚡ **Pull Request Checks** (`pr-check.yml`)
高速なPRバリデーション

**機能**:
- 変更ファイルのみをチェック（高速化）
- カバレッジ80%閾値チェック
- PR自動コメント機能

**トリガー**: PR作成・更新時

---

### 3. 🚀 **Release** (`release.yml`)
自動リリース管理

**機能**:
- GitHub Releaseの自動作成
- CHANGELOGからリリースノート抽出
- Windows実行ファイル生成（PyInstaller）
- PyPI公開対応（オプション）

**トリガー**: `v*.*.*` タグプッシュ

---

### 4. 📅 **Scheduled Checks** (`scheduled-checks.yml`)
定期的なプロジェクト健全性チェック

**機能**:
- 依存関係の脆弱性スキャン
- 古いパッケージの検出
- カバレッジトレンド分析
- ドキュメントリンク切れチェック
- 脆弱性発見時の自動Issue作成

**トリガー**: 毎日午前3時（UTC）

---

## 🚀 次のステップ

### 1. GitHubリポジトリの初期化（まだの場合）

```bash
# リポジトリを初期化
git init
git add .
git commit -m "Initial commit with CI/CD setup"

# GitHubにリモートリポジトリを作成して設定
git remote add origin https://github.com/YOUR_USERNAME/speed-finder.git
git branch -M main
git push -u origin main
```

### 2. オプション設定

#### PyPI公開用（リリース時にPyPIに公開したい場合）

1. PyPIアカウント作成: <https://pypi.org/>
2. API Token取得: Account settings → API tokens
3. GitHubのSecrets設定:

   ```
   Settings → Secrets and variables → Actions → New repository secret
   Name: PYPI_API_TOKEN
   Secret: <your-token>
   ```

4. `release.yml`の該当箇所を編集:

   ```yaml
   - name: 📦 Publish to PyPI
     if: true  # false から true に変更
   ```

#### Codecov連携（カバレッジレポート可視化）

1. <https://codecov.io/> でGitHubアカウントでログイン
2. リポジトリを追加
3. 自動的にワークフローから連携されます

### 3. ブランチ保護ルール設定（推奨）

```
Settings → Branches → Add branch protection rule

Branch name pattern: main

☑ Require a pull request before merging
  ☑ Require approvals: 1
☑ Require status checks to pass before merging
  検索: Quick Validation, Tests
☑ Require conversation resolution before merging
```

### 4. README.mdのバッジ更新

`YOUR_USERNAME` を実際のGitHubユーザー名に置き換えてください:

```markdown
[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/speed-finder/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/YOUR_USERNAME/speed-finder/actions)
```

↓

```markdown
[![CI/CD Pipeline](https://github.com/actual-username/speed-finder/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/actual-username/speed-finder/actions)
```

---

## 🎯 ワークフローの使い方

### ローカルでの事前チェック

```bash
# コード整形
black project/ tests/
isort project/ tests/

# Lint
flake8 project/ tests/

# 型チェック
mypy project/

# テスト実行
pytest tests/ -v --cov=project

# カバレッジ確認
pytest tests/ --cov=project --cov-report=html
```

### 手動ワークフロー実行

```bash
# GitHub CLI使用
gh workflow run ci-cd.yml
gh workflow run scheduled-checks.yml

# または GitHubウェブUI
# Actions → 該当ワークフロー → Run workflow
```

### リリース作成

```bash
# タグを作成
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 自動的にリリースワークフローが実行されます
```

---

## 📊 期待される効果

### ✅ コード品質向上
- 自動Lintによる統一されたコードスタイル
- 型チェックによる型安全性の向上
- セキュリティスキャンによる脆弱性の早期発見

### ✅ 信頼性向上
- 複数環境でのテスト実行
- 高いテストカバレッジ（93%+）維持
- リグレッションの早期発見

### ✅ 開発効率向上
- PR時の自動フィードバック
- リリース作業の自動化
- 定期的な健全性チェック

### ✅ ドキュメント品質
- 自動ドキュメント生成
- リンク切れの定期チェック

---

## 🔧 トラブルシューティング

### ワークフローが実行されない

1. `.github/workflows/` ディレクトリがmainブランチにあることを確認
2. YAMLファイルの構文エラーをチェック（GitHub Actionsタブで確認可能）

### テストが失敗する

```bash
# ローカルで同じ環境を再現
python -m pytest tests/ -v

# デバッグモード
python -m pytest tests/ -v --pdb
```

### カバレッジが閾値を下回る

```bash
# カバレッジレポート確認
pytest tests/ --cov=project --cov-report=html
open htmlcov/index.html

# 不足箇所を特定して追加テスト作成
```

---

## 📚 参考リソース

- [GitHub Actions ドキュメント](https://docs.github.com/en/actions)
- [Python CI/CD ベストプラクティス](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [詳細なワークフロー説明](.github/workflows/README.md)

---

## 🎊 完成

これで、プロフェッショナルなCI/CDパイプラインが構築されました！

**自動化される内容**:
- ✅ コード品質チェック
- ✅ テスト実行
- ✅ セキュリティスキャン
- ✅ ドキュメント生成
- ✅ リリース管理
- ✅ 定期的な健全性チェック

次のコミットから、これらすべてが自動実行されます 🚀✨

# GitHubリモートリポジトリ作成ガイド

## 🎯 目的
ローカルの `speed-finder` プロジェクトをGitHub（`psycloneEffect`アカウント）にプッシュする

---

## 📋 前提条件チェック

- [x] ローカルリポジトリ作成済み
- [x] GitHub Actions ワークフロー設定完了
- [ ] GitHubアカウント `psycloneEffect` でログイン可能
- [ ] Gitの初期設定完了

---

## 🚀 手順（ウェブUI使用）

### Step 1: GitHubでリポジトリ作成

1. <https://github.com/> にアクセスしてログイン
2. 右上の「+」ボタン → 「New repository」
3. 以下を入力:
   - **Owner**: `psycloneEffect`
   - **Repository name**: `speed-finder`
   - **Description**: `WiFiネットワークの速度と安定性をリアルタイムでモニタリングする常駐型アプリケーション`
   - **Visibility**: Public または Private（お好みで）
   - **Initialize**: すべてチェックを外す（ローカルに既存ファイルがあるため）
4. 「Create repository」をクリック

### Step 2: ローカルGit設定確認

ターミナルで以下を実行して確認:

```powershell
# Git設定確認
git config user.name
git config user.email

# 未設定の場合は設定
git config --global user.name "psycloneEffect"
git config --global user.email "your-email@example.com"
```

### Step 3: ローカルリポジトリ初期化

```powershell
# プロジェクトディレクトリに移動（既に居る場合はスキップ）
cd C:\Users\onoma\OneDrive\07_CodeBase\71_Python\speed-finder

# Gitリポジトリ初期化（まだの場合）
git init

# 現在のブランチをmainに変更（masterの場合）
git branch -M main

# ファイルをステージング
git add .

# 初回コミット
git commit -m "feat: Initial commit with comprehensive CI/CD setup

- Complete onion architecture implementation
- Network monitoring with psutil, speedtest-cli, ping3
- Stability analysis service
- PyQt6 system tray UI
- 72 unit tests with 93.29% coverage
- GitHub Actions CI/CD pipeline (4 workflows)
- Comprehensive documentation"
```

### Step 4: リモートリポジトリ接続

GitHubで作成したリポジトリのURLを使用:

```powershell
# HTTPSの場合
git remote add origin https://github.com/psycloneEffect/speed-finder.git

# または SSHの場合（SSH鍵設定済みなら）
git remote add origin git@github.com:psycloneEffect/speed-finder.git

# リモート確認
git remote -v
```

### Step 5: プッシュ

```powershell
# mainブランチをプッシュ
git push -u origin main
```

**初回プッシュ時の認証**:
- **HTTPS**: GitHubのユーザー名とPersonal Access Token（パスワードは使えません）
- **SSH**: SSH鍵のパスフレーズ

---

## 🔑 Personal Access Token (PAT) の作成（HTTPS使用時）

パスワード認証は廃止されたため、PATが必要です:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 「Generate new token (classic)」
3. 設定:
   - **Note**: `speed-finder local development`
   - **Expiration**: 90 days（推奨）
   - **Select scopes**:
     - ☑ `repo` (フルコントロール)
     - ☑ `workflow` (GitHub Actions)
4. 「Generate token」をクリック
5. **トークンをコピーして安全に保存**（再表示不可）

プッシュ時にパスワードの代わりにこのトークンを使用します。

---

## 🔐 SSH鍵の設定（SSH使用時・推奨）

### SSH鍵がない場合

```powershell
# SSH鍵生成
ssh-keygen -t ed25519 -C "your-email@example.com"

# 生成場所: C:\Users\onoma\.ssh\id_ed25519
# パスフレーズ設定（推奨）

# 公開鍵の内容をコピー
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

### GitHubにSSH鍵を登録

1. GitHub → Settings → SSH and GPG keys
2. 「New SSH key」
3. Title: `Windows PC - speed-finder`
4. Key: コピーした公開鍵を貼り付け
5. 「Add SSH key」

### 接続テスト

```powershell
ssh -T git@github.com
# 成功メッセージが表示されればOK
```

---

## ✅ プッシュ後の確認

### GitHub Actionsの実行確認

1. GitHubリポジトリ → 「Actions」タブ
2. 「CI/CD Pipeline」ワークフローが自動実行されているか確認
3. すべてのジョブが成功（緑チェック）することを確認

### README バッジの更新

`README.md` の以下の部分を更新:

```markdown
# 変更前
[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/speed-finder/workflows/...

# 変更後
[![CI/CD Pipeline](https://github.com/psycloneEffect/speed-finder/workflows/...
```

すべての `YOUR_USERNAME` を `psycloneEffect` に置換してコミット・プッシュ。

---

## 🎊 完了

これでGitHub上にリポジトリが作成され、CI/CDパイプラインが動作します！

### 次にできること

✅ リポジトリ設定のカスタマイズ
- Settings → General で説明・トピック設定
- Settings → Branches でブランチ保護ルール
- Settings → Secrets で PyPI token 設定（リリース時）

✅ 開発の継続
- ブランチを切ってPR作成
- Pull Request Checksが自動実行
- レビュー後マージ

✅ リリース準備
- タグを打つだけで自動リリース
- Windows実行ファイルも自動生成

---

## 🔧 トラブルシューティング

### エラー: `fatal: remote origin already exists`

```powershell
# 既存のリモートを削除
git remote remove origin

# 再度追加
git remote add origin https://github.com/psycloneEffect/speed-finder.git
```

### エラー: 認証失敗

- HTTPS: Personal Access Tokenを使用（パスワード不可）
- SSH: SSH鍵が正しく登録されているか確認

### エラー: `rejected` (non-fast-forward)

```powershell
# リモートの状態を確認
git fetch origin

# 必要に応じて強制プッシュ（初回のみ推奨）
git push -u origin main --force
```

---

**作成日**: 2025-10-18  
**所要時間**: 約10-15分  
**次のステップ**: `.github/CICD_SETUP.md` 参照

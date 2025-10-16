# インストールガイド

Speed Finder のインストール方法を説明します。

## 📋 システム要件

### 最小要件

- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **Python**: 3.10 以上
- **メモリ**: 2GB 以上
- **ディスク**: 100MB 以上の空き容量

### 推奨要件

- **OS**: Windows 11
- **Python**: 3.11 以上
- **メモリ**: 4GB 以上
- **ディスク**: 500MB 以上の空き容量

## 🚀 インストール方法

### Method 1: pip でインストール（推奨）

```bash
# PyPI からインストール（将来）
pip install speed-finder

# または、開発版をインストール
pip install git+https://github.com/onoma/speed-finder.git
```

### Method 2: ソースからインストール

```bash
# リポジトリをクローン
git clone https://github.com/onoma/speed-finder.git
cd speed-finder

# 仮想環境を作成
python -m venv .venv

# 仮想環境を有効化
# Windows
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt

# アプリケーションを実行
python -m project.main
```

### Method 3: 実行ファイル（Windows）

**※ 現在準備中**

1. [Releases](https://github.com/onoma/speed-finder/releases) から最新版をダウンロード
2. `SpeedFinder-Setup.exe` を実行
3. インストールウィザードに従う
4. スタートメニューから起動

## 🔧 依存パッケージ

Speed Finder は以下のパッケージに依存しています：

### 必須パッケージ

```txt
psutil>=5.9.0          # システム・ネットワーク統計
PyQt6>=6.6.0           # システムトレイUI
speedtest-cli>=2.1.3   # 速度測定
ping3>=4.0.4           # レイテンシ測定
```

### オプションパッケージ

```txt
numpy>=1.24.0          # 高度な統計分析
loguru>=0.7.0          # 構造化ログ
pyyaml>=6.0.0          # 設定ファイル
```

## 🐍 Python のインストール

### Windows

1. [Python 公式サイト](https://www.python.org/downloads/)から Python 3.11 以上をダウンロード
2. インストーラーを実行
3. **"Add Python to PATH"** にチェックを入れる
4. "Install Now" をクリック

### macOS

```bash
# Homebrew を使用
brew install python@3.11
```

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

## ✅ インストールの確認

```bash
# Python バージョン確認
python --version
# または
python3 --version

# Speed Finder のバージョン確認
speed-finder --version

# 動作確認
speed-finder --help
```

## 🔄 アップデート

### pip でインストールした場合

```bash
pip install --upgrade speed-finder
```

### ソースからインストールした場合

```bash
cd speed-finder
git pull origin main
pip install -r requirements.txt
```

## 🗑️ アンインストール

### pip でインストールした場合

```bash
pip uninstall speed-finder
```

### ソースからインストールした場合

```bash
# プロジェクトフォルダを削除
rm -rf speed-finder
```

### 実行ファイルでインストールした場合

**Windows:**

1. 設定 → アプリ → Speed Finder
2. アンインストールをクリック

## 🐛 トラブルシューティング

### Python が見つからない

**症状**: `python: command not found`

**解決策**:

- Windows: Python インストーラーで "Add to PATH" を有効にして再インストール
- macOS/Linux: `python3` コマンドを使用

### pip が見つからない

**症状**: `pip: command not found`

**解決策**:

```bash
# pip をインストール
python -m ensurepip --upgrade
```

### 依存パッケージのインストールエラー

**症状**: `error: Microsoft Visual C++ 14.0 is required`

**解決策** (Windows):

1. [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) をインストール
2. "Desktop development with C++" を選択

### 権限エラー

**症状**: `Permission denied`

**解決策**:

```bash
# --user オプションを使用
pip install --user speed-finder

# または仮想環境を使用（推奨）
python -m venv .venv
```

### PyQt6 のインポートエラー

**症状**: `ModuleNotFoundError: No module named 'PyQt6'`

**解決策**:

```bash
# PyQt6 を手動インストール
pip install PyQt6>=6.6.0
```

### ネットワーク測定が動作しない

**症状**: 速度測定やping測定ができない

**解決策**:

1. ファイアウォール設定を確認
2. 管理者権限で実行（Windowsの場合）
3. アンチウイルスソフトの除外設定

## 📞 サポート

問題が解決しない場合：

1. [FAQ](../README.md#faq)を確認
2. [既存のIssue](https://github.com/onoma/speed-finder/issues)を検索
3. 新しい[Issue](https://github.com/onoma/speed-finder/issues/new)を作成

## 🎉 次のステップ

インストールが完了したら：

1. [使い方ガイド](usage.md)で基本機能を学ぶ
2. [設定ガイド](configuration.md)でカスタマイズ
3. 問題があれば[トラブルシューティング](troubleshooting.md)を参照

---

**最終更新**: 2025年10月16日

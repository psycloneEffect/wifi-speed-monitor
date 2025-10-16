# Speed Finder MCP Configuration Guide

## 🎯 MCP (Model Context Protocol) とは

MCPは、AIアシスタント（GitHub Copilot等）がプロジェクトのコンテキストをより深く理解するためのプロトコルです。

## 📋 設定ファイル: `.vscode/mcp.json`

このファイルは、VS CodeとMCPサーバーの統合を設定します。

## 🔧 利用可能なMCPサーバー

### 1. Filesystem Server
プロジェクトのファイルシステムへのアクセスを提供

```json
"filesystem": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "c:\\Users\\onoma\\OneDrive\\07_CodeBase\\71_Python\\speed-finder"
  ]
}
```

### 2. GitHub Server
GitHubリポジトリとの統合

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
  }
}
```

### 3. Memory Server
セッション間でのコンテキスト保持

```json
"memory": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-memory"]
}
```

## 🚀 セットアップ手順

### 前提条件

- Node.js がインストールされていること
- GitHub Personal Access Token（GitHub Server使用時）

### 1. Node.js のインストール確認

```powershell
node --version
npm --version
```

### 2. GitHub Token の設定（オプション）

1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token (classic)"
3. `repo` スコープを選択
4. トークンをコピー

**環境変数に設定:**

```powershell
# PowerShell
$env:GITHUB_TOKEN = "your_token_here"

# または .env ファイルに追加
GITHUB_TOKEN=your_token_here
```

### 3. MCP サーバーのテスト

```powershell
# Filesystem serverのテスト
npx -y @modelcontextprotocol/server-filesystem "C:\Users\onoma\OneDrive\07_CodeBase\71_Python\speed-finder"

# Memory serverのテスト
npx -y @modelcontextprotocol/server-memory
```

## 💡 使用例

### プロジェクト構造の理解

MCPが有効な場合、Copilotは以下をより正確に理解します：

- ファイル構造とオニオンアーキテクチャ
- 依存関係
- コーディング規約
- プロジェクトの実装計画

### コンテキスト保持

Memory Serverにより、以下が保持されます：

- 以前の会話のコンテキスト
- プロジェクト固有の決定事項
- コーディングパターン

## 🔒 セキュリティ注意事項

1. **GitHub Tokenの管理**
   - `.env` ファイルに保存（`.gitignore`に追加済み）
   - 環境変数として設定
   - ハードコーディング禁止

2. **ファイルシステムアクセス**
   - プロジェクトディレクトリのみに制限
   - 機密ファイルへのアクセスに注意

## 🐛 トラブルシューティング

### MCPサーバーが起動しない

**症状**: エラーメッセージが表示される

**解決策**:

```powershell
# Nodeキャッシュをクリア
npm cache clean --force

# パッケージを再インストール
npx -y @modelcontextprotocol/server-filesystem --help
```

### GitHub認証エラー

**症状**: `GITHUB_PERSONAL_ACCESS_TOKEN` エラー

**解決策**:

1. トークンの有効期限を確認
2. 環境変数が正しく設定されているか確認
3. VS Codeを再起動

### パスエラー（Windows）

**症状**: パスが認識されない

**解決策**:

- バックスラッシュをエスケープ: `\\`
- または、フォワードスラッシュ使用: `/`

```json
"c:/Users/onoma/OneDrive/07_CodeBase/71_Python/speed-finder"
```

## 📚 参考資料

- [Model Context Protocol 公式ドキュメント](https://modelcontextprotocol.io/)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)

## 🎉 効率的な開発のために

MCPを活用することで：

- ✅ コンテキストを保持した会話
- ✅ プロジェクト構造の正確な理解
- ✅ コーディング規約の自動適用
- ✅ より的確なコード提案

---

**最終更新**: 2025年10月16日

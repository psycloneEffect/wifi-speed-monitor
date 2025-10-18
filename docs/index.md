# WiFi Speed Monitor ドキュメント

Welcome to WiFi Speed Monitor documentation! 🍛

## 📚 ドキュメント構成

### ユーザーガイド

- [インストールガイド](guide/installation.md) - WiFi Speed Monitor のインストール方法
- [使い方](guide/usage.md) - 基本的な使い方と機能説明
- [設定](guide/configuration.md) - 詳細な設定方法

### 開発者ガイド

- [アーキテクチャ](dev/architecture.md) - オニオンアーキテクチャの詳細
- [開発環境セットアップ](dev/setup.md) - 開発環境の構築方法
- [コントリビューション](dev/contributing.md) - プロジェクトへの貢献方法
- [実装計画](implementation-plan.md) - プロジェクトの実装計画とロードマップ

### API リファレンス

- [Core API](api/core.md) - ドメインモデルとインターフェース
- [Services API](api/services.md) - ビジネスロジック
- [Adapters API](api/adapters.md) - インフラストラクチャ実装

## 🚀 クイックスタート

```bash
# インストール
pip install wifi-speed-monitor

# 実行
wifi-speed-monitor
```

詳細は[インストールガイド](guide/installation.md)を参照してください。

## 🏗️ プロジェクト概要

WiFi Speed Monitor は、WiFiネットワークの速度と安定性をリアルタイムでモニタリングする常駐型デスクトップアプリケーションです。

### 主な機能

- 📊 リアルタイムネットワーク統計
- ⬇️⬆️ ダウンロード/アップロード速度測定
- ⏱️ レイテンシ（ping）監視
- 📈 接続安定性分析
- 🔔 システムトレイ常駐
- 💡 マウスオーバー情報表示

### アーキテクチャ

WiFi Speed Monitor は**オニオンアーキテクチャ**を採用しています。

```
Infrastructure → Application → Core
   (外側)                      (内側)
```

詳細は[アーキテクチャドキュメント](dev/architecture.md)を参照してください。

## 📖 ドキュメントをローカルで表示

```bash
# MkDocs をインストール
pip install mkdocs mkdocs-material

# ドキュメントをサーブ
mkdocs serve

# ブラウザで http://127.0.0.1:8000 にアクセス
```

## 🤝 コントリビューション

プロジェクトへの貢献を歓迎します！

1. [コントリビューションガイド](../CONTRIBUTING.md)を読む
2. Issue を作成またはコメント
3. Fork & Pull Request

## 📝 ライセンス

MIT License - 詳細は[LICENSE](../LICENSE)を参照してください。

## 🔗 リンク

- [GitHub Repository](https://github.com/psycloneEffect/wifi-speed-monitor)
- [Issue Tracker](https://github.com/psycloneEffect/wifi-speed-monitor/issues)
- [Changelog](../CHANGELOG.md)

---

**最終更新**: 2025年10月16日

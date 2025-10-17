# テストカバレッジレポート 📊

このディレクトリには、タイムスタンプ付きのテストカバレッジレポートが保存されます。

## ディレクトリ構造

```plain
tests/coverage/
├── 20251018_082420/    # タイムスタンプ付きレポート
│   └── index.html      # カバレッジレポート
├── 20251018_082441/    # 別の実行のレポート
│   └── index.html
└── latest/             # 最新レポートへのリンク ✨
    └── index.html
```

## 使い方

### テスト実行

```powershell
# タイムスタンプ付きカバレッジレポートを生成
python run_tests.py
```

### レポートの確認

```powershell
# 最新のレポートを開く
start tests/coverage/latest/index.html

# 特定のタイムスタンプのレポートを開く
start tests/coverage/20251018_082420/index.html
```

## 機能

- ✅ **タイムスタンプ付き保存**: 毎回のテスト実行が履歴として残ります
- ✅ **latest リンク**: 常に最新のレポートに簡単アクセス
- ✅ **自動クリーンアップ**: 古いレポートを手動で削除可能

## レポートの内容

各タイムスタンプフォルダには以下が含まれます:

- `index.html`: メインのカバレッジレポート
- `class_index.html`: クラスごとのカバレッジ
- `function_index.html`: 関数ごとのカバレッジ
- 各モジュールの詳細HTMLファイル

## 古いレポートの削除

必要に応じて、古いタイムスタンプフォルダを手動で削除できます:

```powershell
# 7日以上前のレポートを削除 (例)
Get-ChildItem -Directory | Where-Object {
    $_.Name -match '^\d{8}_\d{6}$' -and 
    $_.CreationTime -lt (Get-Date).AddDays(-7)
} | Remove-Item -Recurse -Force
```

---

**総合カバレッジ目標**: 80% 以上  
**現在の達成率**: 91.61% 🎉

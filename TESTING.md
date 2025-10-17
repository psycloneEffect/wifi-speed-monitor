# Speed Finder - テスト実行ガイド 🧪

## クイックスタート

```powershell
# タイムスタンプ付きカバレッジレポートを生成
python run_tests.py
```

## テストコマンド比較

### 推奨: run_tests.py 🌟

```powershell
python run_tests.py
```

**メリット:**
- ✅ タイムスタンプ付きでレポートを保存
- ✅ 履歴が自動で残る
- ✅ `latest/` リンクで最新レポートに簡単アクセス
- ✅ 上書きされない

**レポート保存先:**

```plain
tests/coverage/
├── 20251018_082420/   # 1回目
├── 20251018_082441/   # 2回目
└── latest/            # 最新へのリンク ✨
```

### 従来の pytest

```powershell
# 基本
pytest

# カバレッジ付き
pytest --cov=project --cov-report=html

# 詳細表示
pytest -v --cov=project --cov-report=term-missing
```

**注意:**
- ⚠️ 毎回レポートが上書きされる
- ⚠️ 履歴が残らない

## レポートの確認

### 最新レポートを開く

```powershell
# Windows
start tests\coverage\latest\index.html

# または直接指定
start tests\coverage\20251018_082420\index.html
```

### コマンドラインで確認

```powershell
# 簡易表示（pytest実行時に自動表示）
pytest --cov=project --cov-report=term-missing
```

## 特定のテストのみ実行

### ファイル指定

```powershell
# network_adapter のテストのみ
pytest tests/units/test_network_adapter.py -v

# analyzer のテストのみ
pytest tests/units/test_analyzer.py -v

# カバレッジ付き
pytest tests/units/test_network_adapter.py --cov=project.adapters.network_adapter
```

### テストクラス/メソッド指定

```powershell
# 特定のテストクラス
pytest tests/units/test_network_adapter.py::TestPsutilNetworkProvider -v

# 特定のテストメソッド
pytest tests/units/test_network_adapter.py::TestPsutilNetworkProvider::test_init -v
```

### マーカーで選択

```powershell
# 遅いテストをスキップ
pytest -m "not slow"

# ユニットテストのみ
pytest -m "unit"

# 統合テストのみ
pytest -m "integration"
```

## カバレッジレポートの管理

### 古いレポートの削除

```powershell
# 7日以上前のレポートを削除
cd tests\coverage
Get-ChildItem -Directory | Where-Object {
    $_.Name -match '^\d{8}_\d{6}$' -and 
    $_.CreationTime -lt (Get-Date).AddDays(-7)
} | Remove-Item -Recurse -Force
```

### すべてのレポートを削除

```powershell
cd tests\coverage
Get-ChildItem -Directory | Where-Object {
    $_.Name -match '^\d{8}_\d{6}$'
} | Remove-Item -Recurse -Force
Remove-Item latest -Force
```

## CI/CD での実行

### GitHub Actions

```yaml
- name: Run tests with coverage
  run: |
    python run_tests.py
    
- name: Upload coverage report
  uses: actions/upload-artifact@v3
  with:
    name: coverage-report
    path: tests/coverage/latest/
```

### ローカルでの継続的テスト

```powershell
# pytest-watch をインストール
pip install pytest-watch

# ファイル変更時に自動実行
ptw -- --cov=project --cov-report=term-missing
```

## トラブルシューティング

### カバレッジが 0% になる

```powershell
# .coverage ファイルを削除して再実行
Remove-Item .coverage -Force
python run_tests.py
```

### latest リンクが機能しない

```powershell
# 手動で再作成
cd tests\coverage
Remove-Item latest -Force
mklink /J latest 20251018_082420  # 最新のタイムスタンプに置き換え
```

### テストが遅い

```powershell
# 並列実行（pytest-xdist をインストール）
pip install pytest-xdist
pytest -n auto  # CPUコア数に応じて並列実行
```

## 目標とベンチマーク

- **カバレッジ目標**: 80% 以上
- **現在の達成率**: 91.61% 🎉
- **総テスト数**: 62テスト
- **テスト実行時間**: 約1.5秒

---

詳細は [tests/coverage/README.md](tests/coverage/README.md) を参照してください ✨

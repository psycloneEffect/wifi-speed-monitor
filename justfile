# WiFi Speed Monitor - Justfile
# Modern alternative to Makefile
# Install just: https://github.com/casey/just

# デフォルトレシピを表示
default:
    @just --list

# ==========================================
# Setup & Installation
# ==========================================

# 本番環境の依存関係をインストール
install:
    pip install -e .

# 開発環境の依存関係をインストール
install-dev:
    pip install -e ".[dev,docs,analysis,logging,config]"
    pre-commit install

# 開発環境を初期セットアップ
setup: install-dev
    @echo "✅ Development environment is ready!"
    @echo "Run 'just test' to verify everything works."

# ==========================================
# Testing
# ==========================================

# すべてのテストを実行（カバレッジ付き）
test:
    pytest --cov=project --cov-report=term-missing --cov-report=html

# 詳細モードでテスト実行
test-verbose:
    pytest -vv --cov=project --cov-report=term-missing

# ユニットテストのみ実行
test-unit:
    pytest -m unit

# インテグレーションテストのみ実行
test-integration:
    pytest -m integration

# 特定のテストファイルを実行
test-file FILE:
    pytest {{FILE}} -vv

# ==========================================
# Code Quality
# ==========================================

# すべてのリンターを実行
lint:
    flake8 project/ tests/
    pylint project/
    ruff check project/ tests/

# リントエラーを自動修正
lint-fix:
    ruff check --fix project/ tests/

# コードをフォーマット
format:
    black project/ tests/
    isort project/ tests/

# フォーマットチェック（CI用）
format-check:
    black --check project/ tests/
    isort --check-only project/ tests/

# 型チェック
type-check:
    mypy project/

# セキュリティチェック
security:
    bandit -r project/ -c pyproject.toml
    pip-audit

# すべての品質チェックを実行
check: format-check lint type-check test
    @echo "✅ All checks passed!"

# ==========================================
# Documentation
# ==========================================

# ドキュメントをビルド
docs:
    mkdocs build --strict

# ドキュメントをローカルでサーブ
serve:
    mkdocs serve

# ドキュメントをGitHub Pagesにデプロイ
docs-deploy:
    mkdocs gh-deploy

# ==========================================
# Build & Release
# ==========================================

# 配布パッケージをビルド
build: clean
    python -m build

# ビルド成果物をクリーンアップ
clean:
    rm -rf build/ dist/ *.egg-info
    rm -rf .pytest_cache .mypy_cache .ruff_cache
    rm -rf htmlcov/ .coverage coverage.xml
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# バージョンを表示
version:
    @python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"

# ==========================================
# Development
# ==========================================

# アプリケーションを実行
run:
    python -m project.main

# pre-commitフックをインストール
pre-commit-install:
    pre-commit install

# すべてのファイルにpre-commitを実行
pre-commit-run:
    pre-commit run --all-files

# 依存関係を更新
upgrade:
    pip install --upgrade pip
    pip install --upgrade -r requirements.txt

# 仮想環境を再作成
recreate-venv:
    rm -rf .venv
    python -m venv .venv
    @echo "Virtual environment recreated. Activate it and run 'just install-dev'"

# ==========================================
# CI/CD
# ==========================================

# CI環境でのテストを実行
ci-test:
    pytest --cov=project --cov-report=xml --cov-report=term

# CI環境でのリントを実行
ci-lint:
    black --check project/ tests/
    flake8 project/ tests/
    pylint project/
    mypy project/

# ==========================================
# Utilities
# ==========================================

# プロジェクト情報を表示
info:
    @echo "📦 WiFi Speed Monitor"
    @echo "Version: $(just version)"
    @echo "Python: $(python --version)"
    @echo "Location: $(pwd)"

# 依存関係ツリーを表示
deps:
    pip list
    @echo ""
    @echo "Dependency tree:"
    pipdeptree

# コードの統計情報を表示
stats:
    @echo "📊 Code Statistics"
    @echo "=================="
    @cloc project/ --exclude-dir=__pycache__

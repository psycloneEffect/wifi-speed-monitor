# Makefile for Speed Finder development
# Windows環境でも動作するように配慮

.PHONY: help install install-dev test lint format type-check clean docs serve build

# デフォルトターゲット
help:
	@echo "Speed Finder - Development Commands"
	@echo "===================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install production dependencies"
	@echo "  make install-dev    - Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test           - Run tests with coverage"
	@echo "  make lint           - Run all linters"
	@echo "  make format         - Format code with black and isort"
	@echo "  make type-check     - Run type checking with mypy"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs           - Build documentation"
	@echo "  make serve          - Serve documentation locally"
	@echo ""
	@echo "Build & Release:"
	@echo "  make build          - Build distribution packages"
	@echo "  make clean          - Clean build artifacts"
	@echo ""
	@echo "Quality:"
	@echo "  make check          - Run all quality checks"
	@echo "  make pre-commit     - Install pre-commit hooks"

# 依存関係のインストール
install:
	pip install -e .

install-dev:
	pip install -e ".[dev,docs,analysis,logging,config]"
	pre-commit install

# テスト
test:
	pytest --cov=project --cov-report=term-missing --cov-report=html

test-verbose:
	pytest -vv --cov=project --cov-report=term-missing

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

# リント
lint:
	flake8 project/ tests/
	pylint project/
	ruff check project/ tests/

lint-fix:
	ruff check --fix project/ tests/

# フォーマット
format:
	black project/ tests/
	isort project/ tests/

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

# すべてのチェックを実行
check: format-check lint type-check test

# ドキュメント
docs:
	mkdocs build --strict

serve:
	mkdocs serve

# ビルド
build: clean
	python -m build

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov/ .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# pre-commit
pre-commit:
	pre-commit install
	pre-commit run --all-files

# 開発環境のセットアップ（初回）
setup: install-dev pre-commit
	@echo "Development environment is ready! 🚀"
	@echo "Run 'make test' to verify everything works."

# アプリケーションの実行
run:
	python -m project.main

# バージョン情報
version:
	@python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])"

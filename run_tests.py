"""
テスト実行スクリプト with タイムスタンプ付きカバレッジレポート.

タイムスタンプ付きのフォルダにカバレッジレポートを保存し、
最新のレポートへのシンボリックリンクも作成します。
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_tests_with_timestamped_coverage() -> int:
    """
    タイムスタンプ付きカバレッジレポートでテストを実行.

    Returns:
        テストの終了コード (0: 成功, 非0: 失敗).
    """
    # タイムスタンプ付きフォルダ名を生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    coverage_dir = Path("tests") / "coverage" / timestamp

    # カバレッジディレクトリを作成
    coverage_dir.mkdir(parents=True, exist_ok=True)

    print("🚀 Running tests with coverage...")
    print(f"📊 Coverage report will be saved to: {coverage_dir}")
    print("-" * 60)

    # pytestコマンドを実行
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "-v",
        "--cov=project",
        f"--cov-report=html:{coverage_dir}",
        "--cov-report=term-missing",
        "--cov-report=xml:coverage.xml",
    ]

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("-" * 60)
        print(f"✅ Tests passed! Coverage report: {coverage_dir / 'index.html'}")

        # 最新のレポートへのショートカット作成 (Windows)
        latest_link = Path("tests") / "coverage" / "latest"
        if latest_link.exists():
            if latest_link.is_dir():
                import shutil
                shutil.rmtree(latest_link)
            else:
                latest_link.unlink()

        # Windowsではシンボリックリンクの代わりにディレクトリジャンクションを使用
        try:
            import os
            os.system(f'mklink /J "{latest_link}" "{coverage_dir.name}"')
            print(f"🔗 Latest coverage report: {latest_link / 'index.html'}")
        except Exception as e:
            print(f"⚠️ Could not create 'latest' link: {e}")
    else:
        print("-" * 60)
        print("❌ Tests failed! See details above.")

    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests_with_timestamped_coverage())

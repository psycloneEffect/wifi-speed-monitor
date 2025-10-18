"""
プレースホルダーアイコン生成スクリプト

シンプルな円形のアイコンを各品質レベルに応じて生成します。
本番環境では、プロフェッショナルなアイコンに置き換えることを推奨します。
"""
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("PIL (Pillow) がインストールされていません。")
    print("以下のコマンドでインストールしてください:")
    print("  pip install Pillow")
    exit(1)


def create_icon(color: tuple, output_path: Path, size: int = 48) -> None:
    """
    シンプルな円形アイコンを作成します。

    Args:
        color: RGB色タプル
        output_path: 出力ファイルパス
        size: アイコンサイズ（ピクセル）
    """
    # 透明背景の画像を作成
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 円を描画（中心に配置、少し余白を残す）
    margin = 4
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=color + (255,),  # RGB + Alpha
        outline=(255, 255, 255, 200),  # 白い縁
        width=2,
    )

    # 内側の小さな円（Wi-Fi信号のイメージ）
    inner_margin = size // 3
    draw.ellipse(
        [inner_margin, inner_margin, size - inner_margin, size - inner_margin],
        fill=(255, 255, 255, 150),
    )

    # 保存
    img.save(output_path, "PNG")
    print(f"✓ 作成: {output_path.name}")


def main() -> None:
    """メイン処理"""
    # アイコンディレクトリ
    icons_dir = Path(__file__).parent

    # 各品質レベルの色定義（RGB）
    icon_colors = {
        "excellent.png": (34, 139, 34),  # 緑
        "good.png": (70, 130, 180),  # 青
        "fair.png": (255, 165, 0),  # オレンジ
        "poor.png": (220, 20, 60),  # 赤
        "unknown.png": (128, 128, 128),  # 灰色
    }

    print("プレースホルダーアイコンを生成中...")
    print()

    # 各アイコンを生成
    for filename, color in icon_colors.items():
        output_path = icons_dir / filename
        create_icon(color, output_path)

    print()
    print("すべてのアイコンが生成されました！")
    print()
    print("注意: これらはプレースホルダーアイコンです。")
    print("本番環境では、プロフェッショナルなデザインのアイコンに")
    print("置き換えることを推奨します。")


if __name__ == "__main__":
    main()

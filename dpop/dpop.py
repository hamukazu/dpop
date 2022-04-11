import argparse
import math
import os
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont

from dpop import __version__


class DpopFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def check_font_path(path: str) -> str:
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"Font file {repr(path)} is not found.")


def get_os_font() -> str:
    platform = sys.platform
    # if platform.startswith("aix"):
    #     return ""
    # if platform.startswith("cygwin"):
    #     return ""
    if platform.startswith("darwin"):
        return check_font_path("/System/Library/Fonts/Apple Color Emoji.ttc")
    # if platform.startswith("freebsd"):
    #     return ""
    elif platform.startswith("linux"):
        return check_font_path(
            "/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf"
        )
    elif platform.startswith("win32"):
        return check_font_path(r"C:\Windows\Fonts\Seguiemj.ttf")
    else:
        print(f"Unsupported platform: {repr(platform)}", file=sys.stderr)
        exit(1)


def run(size: int, radius: int, shrinking: bool, outfile: str, fontfile: str) -> None:
    images = []
    fontsize = 40
    font = ImageFont.truetype(fontfile, fontsize)

    for i in range(72):
        im = Image.new("RGB", (size, size))
        draw = ImageDraw.Draw(im)
        for j in range(6):
            t = (i * 5 + j * 60) * math.pi / 180
            if shrinking:
                r = radius * (1 - abs(i - 36) / 72)
            else:
                r = radius
            draw.text(
                (
                    int(size / 2 + r * math.cos(t) - fontsize / 2),
                    int(size / 2 + r * math.sin(t) - fontsize / 2),
                ),
                text="💩",
                font=font,
                embedded_color=True,
            )
        images.append(im)

    images[0].save(
        outfile,
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=80,
        loop=0,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="dpop",
        formatter_class=(
            lambda prog: DpopFormatter(
                prog,
                **{
                    "width": shutil.get_terminal_size(fallback=(120, 50)).columns,
                    "max_help_position": 50,
                },
            )
        ),
        description="Dancing Pile-Of-Poo Gif Generator",
    )
    parser.add_argument(
        "--size", type=int, default=300, help="generated image size (<size>x<size>)"
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=100,
        help="radius of the wheel around which poops spin",
    )
    parser.add_argument("--shrinking", action="store_true", help="shrinking mode")
    parser.add_argument(
        "-o", "--output", type=str, default="dpop.gif", help="output file"
    )
    parser.add_argument(
        "--font", type=check_font_path, default=get_os_font(), help="font file"
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(args.size, args.radius, args.shrinking, args.output, args.font)


if __name__ == "__main__":
    main()

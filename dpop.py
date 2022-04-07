from PIL import Image, ImageDraw, ImageFont
import math
import sys
import argparse


def run(size, radius, shrinking, outfile):

    images = []
    fontsize = 40
    if sys.platform == "darwin":
        font = ImageFont.truetype(
            "/System/Library/Fonts/Apple Color Emoji.ttc", fontsize
        )
    else:
        print("Unsupported platform")
        sys.exit(1)

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=300)
    parser.add_argument("--radius", type=int, default=100)
    parser.add_argument("--shrinking", action="store_true", help="shrinking mode")
    parser.add_argument(
        "-o", "--output", type=str, default="dpop.gif", help="output file"
    )
    args = parser.parse_args(sys.argv[1:])
    run(args.size, args.radius, args.shrinking, args.output)


if __name__ == "__main__":
    main()

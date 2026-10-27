#!/usr/bin/env python3
"""Create a GitHub-ready square organization avatar using the ACTUAL brand logo.

Usage: python scripts/prepare_avatar.py /path/to/real-fincraft-logo.png
       python scripts/prepare_avatar.py /path/to/real-fincraft-logo.svg -o avatar.png

Recommended input: transparent PNG or SVG, preferably an icon/mark rather than a
long horizontal wordmark. No Fincraft logo has been bundled or reconstructed.
"""
import argparse
from io import BytesIO
from pathlib import Path
from PIL import Image

def open_logo(path):
    if path.suffix.lower() == '.svg':
        try:
            import cairosvg
        except ImportError:
            raise SystemExit('To use an SVG input, install CairoSVG: pip install cairosvg')
        data = cairosvg.svg2png(url=str(path), output_width=2000)
        return Image.open(BytesIO(data)).convert('RGBA')
    return Image.open(path).convert('RGBA')

def main():
    p = argparse.ArgumentParser(description='Fincraft profile avatar from actual logo')
    p.add_argument('logo', type=Path, help='Path to actual Fincraft logo PNG/SVG/JPG/WEBP')
    p.add_argument('-o', '--output', type=Path, default=Path('fincraft-github-avatar.png'))
    p.add_argument('--size', type=int, default=1024)
    p.add_argument('--background', default='#0d1117')
    a = p.parse_args()
    if not a.logo.is_file(): p.error('Logo file does not exist')
    img = open_logo(a.logo)
    if img.getextrema()[3][1] == 0: p.error('Logo is fully transparent')
    # Crop only fully transparent pixels; never auto-remove an opaque background.
    alpha_bbox = img.getchannel('A').getbbox()
    img = img.crop(alpha_bbox)
    side = a.size
    # Keep ample space because GitHub crops organization images to a circle.
    max_side = round(side * .65)
    img.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    bg = Image.new('RGBA',(side,side),a.background)
    bg.alpha_composite(img, ((side-img.width)//2,(side-img.height)//2))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    bg.convert('RGB').save(a.output, optimize=True)
    print('Saved',a.output, f'({side}x{side}); source:', a.logo)

if __name__=='__main__': main()

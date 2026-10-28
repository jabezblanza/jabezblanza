"""Render an animated terminal GIF with the current Philippine time.

GitHub does not execute JavaScript in profile READMEs. The image animates
locally (blinking cursor); GitHub Actions periodically refreshes its clock.
"""
from datetime import datetime
from io import BytesIO
from pathlib import Path
import re
from zoneinfo import ZoneInfo

import cairosvg
from PIL import Image

root = Path(__file__).resolve().parents[1]
assets = root / "assets"
template = (assets / "aboutme.template.svg").read_text(encoding="utf-8")

clock = datetime.now(ZoneInfo("Asia/Manila"))
stamp = clock.strftime("%Y%m%d%H%M")
text = template.replace("__PHT_TIME__", clock.strftime("%H:%M"))

# SVG is only an internal editable source: the README displays an animated GIF.
cursor_pattern = r'<tspan fill="#f4f4f4">▌<animate[^>]*/></tspan>'
on, count = re.subn(cursor_pattern, '<tspan fill="#f4f4f4">▌</tspan>', text)
if count != 1:
    raise RuntimeError("Expected animated cursor was not found in SVG template")
off = on.replace('<tspan fill="#f4f4f4">▌</tspan>', '<tspan fill="#f4f4f4"> </tspan>', 1)

frames = []
for svg in (on, off):
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=1200)
    with Image.open(BytesIO(png)) as image:
        frames.append(image.convert("RGB"))

out = assets / "aboutme.gif"
frames[0].save(
    out, format="GIF", save_all=True, append_images=[frames[1]],
    duration=[650, 450], loop=0, optimize=True, disposal=2,
)

readme_path = root / "README.md"
readme = readme_path.read_text(encoding="utf-8")
updated, count = re.subn(
    r'!\[About Me\]\(\./assets/aboutme\.gif(?:\?v=\d+)?\)',
    f'![About Me](./assets/aboutme.gif?v={stamp})', readme,
)
if count != 1:
    raise RuntimeError("Expected About Me GIF reference was not found")
if updated != readme:
    readme_path.write_text(updated, encoding="utf-8")
print(f"Animated GIF and README updated for {clock:%Y-%m-%d %H:%M} PHT")

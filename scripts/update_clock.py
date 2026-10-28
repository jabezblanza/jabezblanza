from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

root = Path(__file__).resolve().parents[1]
template = (root / "assets" / "aboutme.template.svg").read_text(encoding="utf-8")
clock = datetime.now(ZoneInfo("Asia/Manila")).strftime("%H:%M")
(root / "assets" / "aboutme.svg").write_text(template.replace("__PHT_TIME__", clock), encoding="utf-8")
print(f"Updated profile clock to {clock} PHT")

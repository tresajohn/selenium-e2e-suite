import re
from datetime import datetime
from pathlib import Path


def take_screenshot(driver, name: str) -> Path:
    safe_name = re.sub(r"[^\w\-]", "_", name)[:80]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshots_dir = Path("logs/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    path = screenshots_dir / f"{timestamp}_{safe_name}.png"
    driver.save_screenshot(str(path))
    return path

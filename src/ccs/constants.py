from pathlib import Path
import re

SIMPLIFIED_PATTERN = re.compile(r'[\u4e00-\u9fff]')

PROJECT_ROOT = Path(__file__).parent.parent.parent

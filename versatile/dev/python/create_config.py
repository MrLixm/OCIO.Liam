"""

"""
import os
import sys
from pathlib import Path

mck_dir = Path(__file__).parent
sys.path.append(str(mck_dir))

import makeconfig


# os.environ["MKC_LOG_LVL"] = "INFO"

makeconfig.cook()
from pathlib import Path
import os
import sys

current_path = Path(os.getcwd())
parent_path = current_path.parent
sys.path.append(str(parent_path))

from bacnet_database import Bacnet_Database

bacnet = Bacnet_Database()
bacnet.run_full_scan()



import pytest
import sys
import os
import io
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.VendingMachine import VendingMachine, isinteger_insert
from src.main import main, MENU_PROMPT

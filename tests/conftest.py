# Ensure both packages' src paths are available to Python without PYTHONPATH
import os
import sys

ROOT = os.path.dirname(__file__)
WS = os.path.abspath(os.path.join(ROOT))
EL_SRC = os.path.join(WS, "packages", "elementals", "src")
CFG_SRC = os.path.join(WS, "packages", "configfuncs", "src")
for p in (EL_SRC, CFG_SRC):
    if p not in sys.path:
        sys.path.insert(0, p)

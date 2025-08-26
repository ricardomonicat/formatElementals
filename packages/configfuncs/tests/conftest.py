# Ensure the configfuncs and elementals src paths are on sys.path for imports during tests
import os
import sys

HERE = os.path.dirname(__file__)
CFG_SRC = os.path.abspath(os.path.join(HERE, "..", "src"))
EL_SRC = os.path.abspath(os.path.join(HERE, "..", "..", "elementals", "src"))
for p in (CFG_SRC, EL_SRC):
    if p not in sys.path:
        sys.path.insert(0, p)

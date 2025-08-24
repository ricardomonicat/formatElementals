# Ensure the elementals src path is on sys.path for imports during tests
import os
import sys

HERE = os.path.dirname(__file__)
EL_SRC = os.path.abspath(os.path.join(HERE, "..", "src"))
CFG_SRC = os.path.abspath(os.path.join(HERE, "..", "..", "configfuncs", "src"))
for p in (EL_SRC, CFG_SRC):
    if p not in sys.path:
        sys.path.insert(0, p)

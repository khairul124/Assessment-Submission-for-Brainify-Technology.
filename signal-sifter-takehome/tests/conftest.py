# conftest.py – makes the parent package importable from the tests/ sub-folder
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

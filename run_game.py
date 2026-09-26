import os
import sys

# Ensure both project root and src are available in sys.path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(1, ROOT_DIR)

from main import main

if __name__ == "__main__":
    main()

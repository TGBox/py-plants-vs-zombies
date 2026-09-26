import os
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(1, ROOT_DIR)

import pygame
from main import main

# Post a QUIT event after 1.5 seconds so main loop exits cleanly
pygame.init()
pygame.time.set_timer(pygame.QUIT, 1500)
try:
    main()
except SystemExit:
    print("Main loop exited cleanly via SystemExit!")

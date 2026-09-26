import os
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from main import main

# Post a QUIT event after 1.5 seconds so main loop exits cleanly
pygame.init()
pygame.time.set_timer(pygame.QUIT, 1500)
try:
    main()
except SystemExit:
    print("Main loop exited cleanly via SystemExit!")

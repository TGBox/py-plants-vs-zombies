"""
Lawn mower defense entity.
Acts as the last line of defense in each row, mowing down all zombies when triggered.
"""

import pygame
from assets import AssetManager
from config import CELL_HEIGHT, GRID_START_X, GRID_START_Y, VIRTUAL_WIDTH


class LawnMower:
    def __init__(self, row: int):
        self.row = row
        self.x = float(GRID_START_X - 60)
        self.y = float(GRID_START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2)
        self.image = AssetManager.get_instance().get_image("projectiles/lawn_mower")
        self.is_active = False
        self.is_alive = True
        self.speed = 520.0  # px per second
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def activate(self):
        if not self.is_active:
            self.is_active = True

    def get_hitbox(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y - self.height // 2), self.width, self.height)

    def update(self, dt: float):
        if self.is_active:
            self.x += self.speed * dt
            if self.x > VIRTUAL_WIDTH + 100:
                self.is_alive = False

    def render(self, surface: pygame.Surface):
        rect = self.image.get_rect(center=(int(self.x + self.width // 2), int(self.y)))
        surface.blit(self.image, rect)

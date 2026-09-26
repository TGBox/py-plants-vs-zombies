"""
Projectile classes for peas, frozen peas, and bowling nuts.
"""

import math
import pygame
from assets import AssetManager
from config import CELL_HEIGHT, GRID_ROWS, GRID_START_Y, VIRTUAL_WIDTH


class Projectile:
    def __init__(self, x: float, y: float, row: int, damage: float = 20.0):
        self.x = x
        self.y = y
        self.row = row
        self.damage = damage
        self.speed = 360.0  # px per second
        self.is_alive = True
        self.radius = 12

    def update(self, dt: float):
        self.x += self.speed * dt
        if self.x > VIRTUAL_WIDTH + 50:
            self.is_alive = False

    def get_hitbox(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def render(self, surface: pygame.Surface):
        pass


class Pea(Projectile):
    def __init__(self, x: float, y: float, row: int):
        super().__init__(x, y, row, damage=20.0)
        self.image = AssetManager.get_instance().get_image("projectiles/pea")

    def render(self, surface: pygame.Surface):
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(self.image, rect)


class SnowPea(Projectile):
    def __init__(self, x: float, y: float, row: int):
        super().__init__(x, y, row, damage=20.0)
        self.image = AssetManager.get_instance().get_image("projectiles/snow_pea_proj")
        self.slow_duration = 4.0

    def render(self, surface: pygame.Surface):
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(self.image, rect)


class BowlingNut:
    """
    Wall-nut bowling projectile.
    Rolls down the lane, inflicts massive damage upon hitting a zombie,
    and ricochets/bounces diagonally to an adjacent row!
    """

    def __init__(self, x: float, y: float, row: int):
        self.x = x
        self.y = y
        self.row = row
        self.damage = 400.0
        self.speed_x = 380.0
        self.speed_y = 0.0
        self.target_y = y
        self.is_alive = True
        self.radius = 32
        self.rotation = 0.0
        self.image = AssetManager.get_instance().get_image("projectiles/bowling_nut")
        self.hit_cooldown_zombies: set = set()

    def get_hitbox(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def on_hit_zombie(self):
        # Ricochet: pick an adjacent row (up or down)
        possible_rows = []
        if self.row > 0:
            possible_rows.append(self.row - 1)
        if self.row < GRID_ROWS - 1:
            possible_rows.append(self.row + 1)

        if possible_rows:
            import random
            new_row = random.choice(possible_rows)
            self.row = new_row
            self.target_y = GRID_START_Y + self.row * CELL_HEIGHT + CELL_HEIGHT // 2
            # Move smoothly towards target_y
            direction = 1 if self.target_y > self.y else -1
            self.speed_y = direction * 220.0

    def update(self, dt: float):
        self.x += self.speed_x * dt
        self.rotation = (self.rotation + 420.0 * dt) % 360.0

        if self.speed_y != 0.0:
            self.y += self.speed_y * dt
            if (self.speed_y > 0 and self.y >= self.target_y) or (self.speed_y < 0 and self.y <= self.target_y):
                self.y = self.target_y
                self.speed_y = 0.0

        if self.x > VIRTUAL_WIDTH + 60:
            self.is_alive = False

    def render(self, surface: pygame.Surface):
        rotated = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)

"""
Sun entity class for collectible sun resources.
Supports falling from the sky, popping out of sunflowers, and flying to the HUD.
"""

import math
import random
import pygame
from assets import AssetManager


class Sun:
    VALUE = 25

    def __init__(
        self,
        x: float,
        y: float,
        target_y: float | None = None,
        is_from_plant: bool = False,
    ):
        self.x = x
        self.y = y
        self.is_from_plant = is_from_plant
        self.image = AssetManager.get_instance().get_image("projectiles/sun")
        self.radius = 32

        if is_from_plant:
            # Arching jump from sunflower
            self.vx = random.uniform(-40, 40)
            self.vy = -160.0
            self.target_y = y + random.uniform(10, 40)
            self.gravity = 350.0
            self.resting = False
        else:
            # Falling from sky
            self.vx = 0.0
            self.vy = 85.0
            self.target_y = target_y if target_y is not None else random.uniform(220, 620)
            self.gravity = 0.0
            self.resting = False

        self.rotation = 0.0
        self.lifetime = 12.0  # seconds before disappearing if ignored
        self.is_alive = True
        self.is_collected = False

        # Flight to UI Sun Counter
        self.target_ui_x = 85.0
        self.target_ui_y = 45.0
        self.collect_speed = 750.0

    def collect(self):
        if not self.is_collected:
            self.is_collected = True
            self.resting = False

    def is_clicked(self, mouse_x: float, mouse_y: float) -> bool:
        if self.is_collected:
            return False
        dist = math.hypot(self.x - mouse_x, self.y - mouse_y)
        return dist <= (self.radius + 14)  # generous hit radius

    def update(self, dt: float) -> bool:
        """Returns True if the sun just reached the HUD counter and gave points."""
        self.rotation = (self.rotation + 45.0 * dt) % 360.0

        if self.is_collected:
            dx = self.target_ui_x - self.x
            dy = self.target_ui_y - self.y
            dist = math.hypot(dx, dy)
            step = self.collect_speed * dt

            if dist <= step or dist < 12.0:
                self.is_alive = False
                return True  # Awarded!

            self.x += (dx / dist) * step
            self.y += (dy / dist) * step
            return False

        if not self.resting:
            if self.is_from_plant:
                self.vy += self.gravity * dt
                self.x += self.vx * dt
                self.y += self.vy * dt
                if self.vy > 0 and self.y >= self.target_y:
                    self.y = self.target_y
                    self.resting = True
            else:
                self.y += self.vy * dt
                if self.y >= self.target_y:
                    self.y = self.target_y
                    self.resting = True
        else:
            self.lifetime -= dt
            if self.lifetime <= 0:
                self.is_alive = False

        return False

    def render(self, surface: pygame.Surface):
        # Pulsing scale effect
        pulse = 1.0 + 0.06 * math.sin(pygame.time.get_ticks() * 0.006)
        scaled_size = int(self.image.get_width() * pulse)
        scaled_img = pygame.transform.smoothscale(self.image, (scaled_size, scaled_size))
        rotated = pygame.transform.rotate(scaled_img, self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)

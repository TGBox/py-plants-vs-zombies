"""
Projectile classes for peas, frozen peas, fume spores, jalapeno fire, and bowling nut variants.
"""

import math
import random
from typing import TYPE_CHECKING
import pygame
from assets import AssetManager
from config import CELL_HEIGHT, GRID_ROWS, GRID_START_Y, VIRTUAL_WIDTH

if TYPE_CHECKING:
    from entities.zombie import Zombie
    from systems.particle import ParticleSystem


class Projectile:
    def __init__(self, x: float, y: float, row: int, damage: float = 20.0):
        self.x = x
        self.y = y
        self.row = row
        self.damage = damage
        self.speed = 380.0  # px per second
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


class FumeSpore(Projectile):
    """
    Piercing fume puff that passes through multiple zombies in its lane,
    bypassing Screen Door shield protection!
    """

    def __init__(self, x: float, y: float, row: int):
        super().__init__(x, y, row, damage=20.0)
        self.image = AssetManager.get_instance().get_image("projectiles/fume_spore")
        self.speed = 280.0
        self.radius = 18
        self.max_distance = 360.0  # Fume cloud reaches about 3-4 tiles ahead
        self.traveled = 0.0
        self.hit_zombies: set = set()

    def update(self, dt: float):
        step = self.speed * dt
        self.x += step
        self.traveled += step
        if self.traveled >= self.max_distance or self.x > VIRTUAL_WIDTH + 50:
            self.is_alive = False

    def render(self, surface: pygame.Surface):
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(self.image, rect)


class JalapenoFlame:
    """
    Fiery inferno that blazes along an entire row, incinerating all zombies.
    """

    def __init__(self, row: int):
        self.row = row
        self.y = float(GRID_START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2)
        self.duration = 1.0
        self.elapsed = 0.0
        self.damage = 1800.0
        self.is_alive = True
        self.image = AssetManager.get_instance().get_image("projectiles/jalapeno_fire")
        self.hit_zombies: set = set()

    def update(self, dt: float):
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.is_alive = False

    def render(self, surface: pygame.Surface):
        # Render tiled fire wall along the lane
        for x in range(224, VIRTUAL_WIDTH, 104):
            surface.blit(self.image, (x, int(self.y - 48)))


# -------------------------------------------------------------
# BOWLING NUT VARIANTS
# -------------------------------------------------------------
class BaseBowlingNut:
    def __init__(self, x: float, y: float, row: int, damage: float, speed_x: float = 380.0):
        self.x = x
        self.y = y
        self.row = row
        self.damage = damage
        self.speed_x = speed_x
        self.speed_y = 0.0
        self.target_y = y
        self.is_alive = True
        self.radius = 32
        self.rotation = 0.0
        self.hit_cooldown_zombies: set = set()

    def get_hitbox(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def on_hit_zombie(self, zombie: "Zombie", particle_sys: "ParticleSystem", all_zombies: list["Zombie"]) -> int:
        """Called when colliding with a zombie. Returns points earned."""
        return 100

    def update(self, dt: float):
        self.x += self.speed_x * dt
        self.rotation = (self.rotation + 450.0 * dt) % 360.0

        if self.speed_y != 0.0:
            self.y += self.speed_y * dt
            if (self.speed_y > 0 and self.y >= self.target_y) or (self.speed_y < 0 and self.y <= self.target_y):
                self.y = self.target_y
                self.speed_y = 0.0

        if self.x > VIRTUAL_WIDTH + 80:
            self.is_alive = False

    def render(self, surface: pygame.Surface):
        pass


class BowlingNut(BaseBowlingNut):
    """
    Standard Wall-nut: deals 400 damage on hit and ricochets/bounces diagonally!
    """

    def __init__(self, x: float, y: float, row: int):
        super().__init__(x, y, row, damage=400.0, speed_x=380.0)
        self.image = AssetManager.get_instance().get_image("projectiles/bowling_nut")

    def on_hit_zombie(self, zombie: "Zombie", particle_sys: "ParticleSystem", all_zombies: list["Zombie"]) -> int:
        zombie.take_damage(self.damage)
        self.hit_cooldown_zombies.add(id(zombie))
        particle_sys.spawn_splat(zombie.x, zombie.y)

        # Ricochet bounce to an adjacent row (up or down)
        possible_rows = []
        if self.row > 0:
            possible_rows.append(self.row - 1)
        if self.row < GRID_ROWS - 1:
            possible_rows.append(self.row + 1)

        if possible_rows:
            new_row = random.choice(possible_rows)
            self.row = new_row
            self.target_y = GRID_START_Y + self.row * CELL_HEIGHT + CELL_HEIGHT // 2
            direction = 1 if self.target_y > self.y else -1
            self.speed_y = direction * 240.0

        return 100

    def render(self, surface: pygame.Surface):
        rotated = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)


class BowlingCherryNut(BaseBowlingNut):
    """
    Explosive Cherry Bomb Nut: IMMEDIATELY DETONATES on first contact,
    inflicting 1800 damage in a 3x3 radius and obliterating all nearby zombies!
    """

    def __init__(self, x: float, y: float, row: int):
        super().__init__(x, y, row, damage=1800.0, speed_x=420.0)
        self.image = AssetManager.get_instance().get_image("plants/cherry_bomb")

    def on_hit_zombie(self, zombie: "Zombie", particle_sys: "ParticleSystem", all_zombies: list["Zombie"]) -> int:
        # Massive 3x3 Detonation
        self.is_alive = False
        particle_sys.spawn_explosion(self.x, self.y)
        particle_sys.add_floating_text(
            "KABOOM!",
            self.x,
            self.y - 35,
            (255, 60, 40),
            AssetManager.get_instance().get_font("title"),
        )

        kills = 0
        # Deal 1800 damage to all zombies within 1 row above/below and +/- 120 px
        for z in all_zombies:
            if z.is_alive and abs(z.row - self.row) <= 1 and abs(z.x - self.x) <= 130.0:
                z.take_damage(self.damage)
                particle_sys.spawn_splat(z.x, z.y)
                kills += 1

        return 200 + kills * 150

    def render(self, surface: pygame.Surface):
        # Pulsing shaking animation
        scale = 1.0 + 0.15 * math.sin(pygame.time.get_ticks() * 0.02)
        scaled_w = int(self.image.get_width() * scale)
        scaled_h = int(self.image.get_height() * scale)
        scaled = pygame.transform.smoothscale(self.image, (scaled_w, scaled_h))
        rect = scaled.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(scaled, rect)


class BowlingGiantNut(BaseBowlingNut):
    """
    Giant Wall-nut: Heavy colossus that rolls straight forward without bouncing,
    crushing EVERY zombie in the lane to dust!
    """

    def __init__(self, x: float, y: float, row: int):
        super().__init__(x, y, row, damage=9999.0, speed_x=340.0)
        self.radius = 45
        self.image = AssetManager.get_instance().get_image("projectiles/bowling_giant_nut")

    def on_hit_zombie(self, zombie: "Zombie", particle_sys: "ParticleSystem", all_zombies: list["Zombie"]) -> int:
        # Flatten zombie and keep rolling straight
        zombie.take_damage(self.damage)
        self.hit_cooldown_zombies.add(id(zombie))
        particle_sys.spawn_splat(zombie.x, zombie.y)
        particle_sys.add_floating_text(
            "PLATSCH!",
            zombie.x,
            zombie.y - 30,
            (255, 180, 40),
            AssetManager.get_instance().get_font("medium"),
        )
        return 150

    def render(self, surface: pygame.Surface):
        rotated = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)


class BowlingIceNut(BaseBowlingNut):
    """
    Ice Nut: Freezes and slows all zombies in the area on impact!
    """

    def __init__(self, x: float, y: float, row: int):
        super().__init__(x, y, row, damage=350.0, speed_x=390.0)
        self.image = AssetManager.get_instance().get_image("projectiles/bowling_ice_nut")

    def on_hit_zombie(self, zombie: "Zombie", particle_sys: "ParticleSystem", all_zombies: list["Zombie"]) -> int:
        self.is_alive = False
        particle_sys.spawn_splat(self.x, self.y, is_ice=True)
        particle_sys.add_floating_text(
            "EIS-STOSS!",
            self.x,
            self.y - 30,
            (100, 220, 255),
            AssetManager.get_instance().get_font("large"),
        )

        for z in all_zombies:
            if z.is_alive and abs(z.row - self.row) <= 1 and abs(z.x - self.x) <= 160.0:
                z.take_damage(self.damage)
                z.apply_freeze(6.0)
                particle_sys.spawn_splat(z.x, z.y, is_ice=True)

        return 175

    def render(self, surface: pygame.Surface):
        rotated = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)

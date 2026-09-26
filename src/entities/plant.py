"""
Plant base class and specialized plant types.
Includes Sunflower, Peashooter, SnowPea, Wallnut, CherryBomb, and PotatoMine.
"""

import math
from typing import TYPE_CHECKING
import pygame
from assets import AssetManager
from config import CELL_HEIGHT, CELL_WIDTH, GRID_START_X, GRID_START_Y, PLANT_SPECS
from entities.projectile import Pea, SnowPea
from entities.sun import Sun

if TYPE_CHECKING:
    from entities.zombie import Zombie
    from systems.particle import ParticleSystem


class Plant:
    def __init__(self, plant_type: str, row: int, col: int):
        self.plant_type = plant_type
        self.row = row
        self.col = col
        self.x = float(GRID_START_X + col * CELL_WIDTH + CELL_WIDTH // 2)
        self.y = float(GRID_START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2)

        spec = PLANT_SPECS[plant_type]
        self.hp = float(spec["hp"])
        self.max_hp = float(spec["hp"])
        self.is_alive = True

        self.anim_timer = 0.0
        self.flash_timer = 0.0  # Damage flash
        self.image = AssetManager.get_instance().get_image(f"plants/{plant_type}")
        self.width = 96
        self.height = 96

    def take_damage(self, amount: float):
        self.hp -= amount
        self.flash_timer = 0.15
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def get_hitbox(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.x - CELL_WIDTH // 2 + 10),
            int(self.y - CELL_HEIGHT // 2 + 10),
            CELL_WIDTH - 20,
            CELL_HEIGHT - 20,
        )

    def update(
        self,
        dt: float,
        zombies_in_row: list["Zombie"],
        projectiles_list: list,
        suns_list: list,
        particle_sys: "ParticleSystem",
    ):
        self.anim_timer += dt
        if self.flash_timer > 0:
            self.flash_timer -= dt

    def render(self, surface: pygame.Surface):
        # Subtle idle squash and stretch breathing animation
        squash = 1.0 + 0.04 * math.sin(self.anim_timer * 3.5)
        stretch = 1.0 / squash
        scaled_w = int(self.image.get_width() * squash)
        scaled_h = int(self.image.get_height() * stretch)
        scaled_img = pygame.transform.smoothscale(self.image, (scaled_w, scaled_h))

        if self.flash_timer > 0:
            # Flashing white / red overlay on damage
            tinted = scaled_img.copy()
            tinted.fill((255, 100, 100, 140), special_flags=pygame.BLEND_RGBA_ADD)
            rect = tinted.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(tinted, rect)
        else:
            rect = scaled_img.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(scaled_img, rect)


class Sunflower(Plant):
    def __init__(self, row: int, col: int):
        super().__init__("sunflower", row, col)
        self.production_interval = 24.0
        # First sun spawns faster (~7 seconds) so player gets going
        self.production_timer = 17.0
        self.is_glowing = False

    def update(
        self,
        dt: float,
        zombies_in_row: list["Zombie"],
        projectiles_list: list,
        suns_list: list,
        particle_sys: "ParticleSystem",
    ):
        super().update(dt, zombies_in_row, projectiles_list, suns_list, particle_sys)
        self.production_timer += dt

        # Glow in the final second before producing sun
        self.is_glowing = (self.production_interval - self.production_timer) <= 1.2

        if self.production_timer >= self.production_interval:
            self.production_timer = 0.0
            self.is_glowing = False
            # Spawn Sun jumping out of Sunflower
            new_sun = Sun(self.x, self.y - 10, is_from_plant=True)
            suns_list.append(new_sun)
            particle_sys.spawn_sun_sparkles(self.x, self.y - 20)

    def render(self, surface: pygame.Surface):
        super().render(surface)
        if self.is_glowing:
            # Draw bright yellow aura
            glow_surf = pygame.Surface((110, 110), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 240, 100, 90), (55, 55), 50)
            surface.blit(glow_surf, (int(self.x - 55), int(self.y - 55)), special_flags=pygame.BLEND_RGBA_ADD)


class Peashooter(Plant):
    def __init__(self, row: int, col: int):
        super().__init__("peashooter", row, col)
        self.shoot_interval = 1.45
        self.shoot_timer = 1.0  # shoots soon after planting
        self.recoil_offset = 0.0

    def update(
        self,
        dt: float,
        zombies_in_row: list["Zombie"],
        projectiles_list: list,
        suns_list: list,
        particle_sys: "ParticleSystem",
    ):
        super().update(dt, zombies_in_row, projectiles_list, suns_list, particle_sys)
        self.shoot_timer += dt

        if self.recoil_offset > 0:
            self.recoil_offset = max(0.0, self.recoil_offset - 30.0 * dt)

        # Check if there is any alive zombie in this row ahead of the peashooter
        has_target = any(z.is_alive and z.x > self.x for z in zombies_in_row)

        if has_target and self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            self.recoil_offset = 6.0
            # Spawn Pea at the snout
            pea = Pea(self.x + 36, self.y - 4, self.row)
            projectiles_list.append(pea)


class SnowPea(Plant):
    def __init__(self, row: int, col: int):
        super().__init__("snow_pea", row, col)
        self.shoot_interval = 1.45
        self.shoot_timer = 1.0
        self.recoil_offset = 0.0

    def update(
        self,
        dt: float,
        zombies_in_row: list["Zombie"],
        projectiles_list: list,
        suns_list: list,
        particle_sys: "ParticleSystem",
    ):
        super().update(dt, zombies_in_row, projectiles_list, suns_list, particle_sys)
        self.shoot_timer += dt

        if self.recoil_offset > 0:
            self.recoil_offset = max(0.0, self.recoil_offset - 30.0 * dt)

        has_target = any(z.is_alive and z.x > self.x for z in zombies_in_row)

        if has_target and self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            self.recoil_offset = 6.0
            snow_pea = SnowPea(self.x + 36, self.y - 4, self.row)
            projectiles_list.append(snow_pea)


class Wallnut(Plant):
    def __init__(self, row: int, col: int):
        super().__init__("wallnut", row, col)
        self.assets = AssetManager.get_instance()
        self.img_healthy = self.assets.get_image("plants/wallnut")
        self.img_cracked1 = self.assets.get_image("plants/wallnut_cracked1")
        self.img_cracked2 = self.assets.get_image("plants/wallnut_cracked2")

    def update(
        self,
        dt: float,
        zombies_in_row: list["Zombie"],
        projectiles_list: list,
        suns_list: list,
        particle_sys: "ParticleSystem",
    ):
        super().update(dt, zombies_in_row, projectiles_list, suns_list, particle_sys)

        # Update sprite based on damage stages
        if self.hp <= self.max_hp * 0.33:
            self.image = self.img_cracked2
        elif self.hp <= self.max_hp * 0.66:
            self.image = self.img_cracked1
        else:
            self.image = self.img_healthy


class CherryBomb(Plant):
    def __init__(self, row: int, col: int):
        super().__init__("cherry_bomb", row, col)
        self.fuse_time = 1.15
        self.elapsed = 0.0
        self.damage = 1800.0

    def update(
        self,
        dt: float,
        zombies_in_row: list["Zombie"],
        projectiles_list: list,
        suns_list: list,
        particle_sys: "ParticleSystem",
    ):
        self.anim_timer += dt
        self.elapsed += dt

        if self.elapsed >= self.fuse_time:
            self.explode(particle_sys)

    def explode(self, particle_sys: "ParticleSystem"):
        self.is_alive = False
        particle_sys.spawn_explosion(self.x, self.y)
        particle_sys.add_floating_text("BOOM!", self.x, self.y - 30, (255, 60, 40), AssetManager.get_instance().get_font("title"))

    def render(self, surface: pygame.Surface):
        # Swelling and shaking during fuse
        progress = self.elapsed / self.fuse_time
        scale = 1.0 + 0.35 * progress
        shake_x = math.sin(self.anim_timer * 35.0) * 4.0 * progress
        shake_y = math.cos(self.anim_timer * 35.0) * 4.0 * progress

        scaled_w = int(self.image.get_width() * scale)
        scaled_h = int(self.image.get_height() * scale)
        scaled_img = pygame.transform.smoothscale(self.image, (scaled_w, scaled_h))

        rect = scaled_img.get_rect(center=(int(self.x + shake_x), int(self.y + shake_y)))
        surface.blit(scaled_img, rect)


class PotatoMine(Plant):
    def __init__(self, row: int, col: int):
        super().__init__("potato_mine", row, col)
        self.assets = AssetManager.get_instance()
        self.img_unarmed = self.assets.get_image("plants/potato_mine_unarmed")
        self.img_armed = self.assets.get_image("plants/potato_mine_armed")
        self.image = self.img_unarmed

        self.arm_duration = 14.0  # seconds until armed
        self.arm_timer = 0.0
        self.is_armed = False
        self.damage = 1800.0

    def update(
        self,
        dt: float,
        zombies_in_row: list["Zombie"],
        projectiles_list: list,
        suns_list: list,
        particle_sys: "ParticleSystem",
    ):
        super().update(dt, zombies_in_row, projectiles_list, suns_list, particle_sys)

        if not self.is_armed:
            self.arm_timer += dt
            if self.arm_timer >= self.arm_duration:
                self.is_armed = True
                self.image = self.img_armed
                particle_sys.spawn_splat(self.x, self.y)
        else:
            # Check contact with any zombie in same row
            for z in zombies_in_row:
                if z.is_alive and abs(z.x - self.x) <= 38.0:
                    self.explode_on(z, particle_sys)
                    break

    def explode_on(self, zombie: "Zombie", particle_sys: "ParticleSystem"):
        self.is_alive = False
        zombie.take_damage(self.damage)
        particle_sys.spawn_explosion(self.x, self.y)
        particle_sys.add_floating_text("SPUDOW!", self.x, self.y - 25, (255, 120, 20), AssetManager.get_instance().get_font("large"))

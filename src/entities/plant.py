"""
Plant base class and all specialized plant types.
Includes Sunflower, Peashooter, SnowPea, Wallnut, CherryBomb, PotatoMine,
Repeater, Chomper, Jalapeno, Squash, PuffShroom, and FumeShroom.
"""

import math
from typing import TYPE_CHECKING
import pygame
from assets import AssetManager, apply_tint
from config import CELL_HEIGHT, CELL_WIDTH, GRID_START_X, GRID_START_Y, PLANT_SPECS
from entities.projectile import FumeSpore, JalapenoFlame, Pea, SnowPea
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
            # Preserves alpha cleanly so no square rectangle appears!
            tinted = apply_tint(scaled_img, (160, 60, 60), blend_mode=pygame.BLEND_RGB_ADD)
            rect = tinted.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(tinted, rect)
        else:
            rect = scaled_img.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(scaled_img, rect)


class Sunflower(Plant):
    def __init__(self, row: int, col: int):
        super().__init__("sunflower", row, col)
        self.production_interval = 24.0
        self.production_timer = 18.0  # First sun spawns early to kickstart defense
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

        self.is_glowing = (self.production_interval - self.production_timer) <= 1.2

        if self.production_timer >= self.production_interval:
            self.production_timer = 0.0
            self.is_glowing = False
            new_sun = Sun(self.x, self.y - 10, is_from_plant=True)
            suns_list.append(new_sun)
            particle_sys.spawn_sun_sparkles(self.x, self.y - 20)

    def render(self, surface: pygame.Surface):
        super().render(surface)
        if self.is_glowing:
            glow_surf = pygame.Surface((110, 110), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 240, 100, 90), (55, 55), 50)
            surface.blit(glow_surf, (int(self.x - 55), int(self.y - 55)), special_flags=pygame.BLEND_RGB_ADD)


class Peashooter(Plant):
    def __init__(self, row: int, col: int):
        super().__init__("peashooter", row, col)
        self.shoot_interval = 1.45
        self.shoot_timer = 1.0

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

        has_target = any(z.is_alive and z.x > self.x for z in zombies_in_row)

        if has_target and self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            pea = Pea(self.x + 36, self.y - 4, self.row)
            projectiles_list.append(pea)


class Repeater(Plant):
    """Fires two peas in rapid succession!"""

    def __init__(self, row: int, col: int):
        super().__init__("repeater", row, col)
        self.shoot_interval = 1.45
        self.shoot_timer = 1.0
        self.second_shot_timer = -1.0

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

        has_target = any(z.is_alive and z.x > self.x for z in zombies_in_row)

        if has_target and self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            # First pea
            projectiles_list.append(Pea(self.x + 36, self.y - 4, self.row))
            # Schedule second pea 0.18s later
            self.second_shot_timer = 0.18

        if self.second_shot_timer > 0:
            self.second_shot_timer -= dt
            if self.second_shot_timer <= 0:
                projectiles_list.append(Pea(self.x + 36, self.y - 4, self.row))
                self.second_shot_timer = -1.0


class SnowPea(Plant):
    def __init__(self, row: int, col: int):
        super().__init__("snow_pea", row, col)
        self.shoot_interval = 1.45
        self.shoot_timer = 1.0

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

        has_target = any(z.is_alive and z.x > self.x for z in zombies_in_row)

        if has_target and self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            projectiles_list.append(SnowPea(self.x + 36, self.y - 4, self.row))


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
        particle_sys.add_floating_text(
            "BOOM!",
            self.x,
            self.y - 30,
            (255, 60, 40),
            AssetManager.get_instance().get_font("title"),
        )

    def render(self, surface: pygame.Surface):
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

        self.arm_duration = 14.0
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
            for z in zombies_in_row:
                if z.is_alive and abs(z.x - self.x) <= 38.0:
                    self.explode_on(z, particle_sys)
                    break

    def explode_on(self, zombie: "Zombie", particle_sys: "ParticleSystem"):
        self.is_alive = False
        zombie.take_damage(self.damage)
        particle_sys.spawn_explosion(self.x, self.y)
        particle_sys.add_floating_text(
            "SPUDOW!",
            self.x,
            self.y - 25,
            (255, 120, 20),
            AssetManager.get_instance().get_font("large"),
        )


class Chomper(Plant):
    """
    Devours a zombie whole!
    Takes 22 seconds to chew, during which it is vulnerable.
    """

    def __init__(self, row: int, col: int):
        super().__init__("chomper", row, col)
        self.chew_duration = 22.0
        self.chew_timer = 0.0
        self.is_chewing = False

    def update(
        self,
        dt: float,
        zombies_in_row: list["Zombie"],
        projectiles_list: list,
        suns_list: list,
        particle_sys: "ParticleSystem",
    ):
        super().update(dt, zombies_in_row, projectiles_list, suns_list, particle_sys)

        if self.is_chewing:
            self.chew_timer -= dt
            if self.chew_timer <= 0:
                self.is_chewing = False
                particle_sys.add_floating_text(
                    "BURP!",
                    self.x,
                    self.y - 30,
                    (180, 240, 80),
                    AssetManager.get_instance().get_font("normal"),
                )
        else:
            # Check for any zombie in front within reach (up to 120 px)
            for z in zombies_in_row:
                if z.is_alive and 0 < (z.x - self.x) <= 125.0:
                    # Chomp!
                    self.is_chewing = True
                    self.chew_timer = self.chew_duration
                    z.take_damage(9999.0)  # Swallow whole
                    particle_sys.spawn_splat(self.x + 30, self.y)
                    particle_sys.add_floating_text(
                        "CHOMP!",
                        self.x + 30,
                        self.y - 30,
                        (190, 40, 220),
                        AssetManager.get_instance().get_font("large"),
                    )
                    break

    def render(self, surface: pygame.Surface):
        super().render(surface)
        if self.is_chewing:
            # Display chewing bubbles/munching badge
            badge = AssetManager.get_instance().get_font("tiny").render("KAUT...", True, (240, 240, 220))
            surface.blit(badge, (int(self.x - badge.get_width() // 2), int(self.y + 35)))


class Jalapeno(Plant):
    """
    Ignites a blazing column of flame across the entire row, incinerating all zombies!
    """

    def __init__(self, row: int, col: int):
        super().__init__("jalapeno", row, col)
        self.fuse_time = 0.75
        self.elapsed = 0.0

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
            self.is_alive = False
            # Spawn row inferno
            projectiles_list.append(JalapenoFlame(self.row))
            particle_sys.spawn_explosion(self.x, self.y)
            particle_sys.add_floating_text(
                "FEUER!",
                self.x,
                self.y - 35,
                (255, 80, 20),
                AssetManager.get_instance().get_font("title"),
            )
            # Damage all zombies currently in row
            for z in zombies_in_row:
                z.take_damage(1800.0)

    def render(self, surface: pygame.Surface):
        # Shake and glow bright red
        progress = self.elapsed / self.fuse_time
        shake = math.sin(self.anim_timer * 40.0) * 5.0 * progress
        scaled = pygame.transform.smoothscale(self.image, (int(96 * (1.0 + 0.3 * progress)), 96))
        rect = scaled.get_rect(center=(int(self.x + shake), int(self.y)))
        surface.blit(scaled, rect)


class Squash(Plant):
    """
    Leaps high into the air and squashes an approaching zombie flat!
    """

    def __init__(self, row: int, col: int):
        super().__init__("squash", row, col)
        self.is_jumping = False
        self.jump_timer = 0.0
        self.jump_duration = 0.65
        self.target_x = self.x
        self.start_x = self.x
        self.target_zombie: "Zombie | None" = None

    def update(
        self,
        dt: float,
        zombies_in_row: list["Zombie"],
        projectiles_list: list,
        suns_list: list,
        particle_sys: "ParticleSystem",
    ):
        super().update(dt, zombies_in_row, projectiles_list, suns_list, particle_sys)

        if self.is_jumping:
            self.jump_timer += dt
            t = min(1.0, self.jump_timer / self.jump_duration)
            self.x = self.start_x + (self.target_x - self.start_x) * t
            # Arc jump
            self.y = (GRID_START_Y + self.row * CELL_HEIGHT + CELL_HEIGHT // 2) - math.sin(t * math.pi) * 80.0

            if t >= 1.0:
                self.is_alive = False
                particle_sys.spawn_explosion(self.x, self.y)
                particle_sys.add_floating_text(
                    "PLATSCH!",
                    self.x,
                    self.y - 30,
                    (140, 220, 40),
                    AssetManager.get_instance().get_font("large"),
                )
                if self.target_zombie and self.target_zombie.is_alive:
                    self.target_zombie.take_damage(1800.0)
                # Area damage
                for z in zombies_in_row:
                    if z.is_alive and abs(z.x - self.x) <= 60.0:
                        z.take_damage(1800.0)
            return

        # Scan for zombie within 1 tile ahead or behind
        for z in zombies_in_row:
            if z.is_alive and abs(z.x - self.x) <= 95.0:
                self.is_jumping = True
                self.target_zombie = z
                self.start_x = self.x
                self.target_x = z.x
                particle_sys.add_floating_text(
                    "HMMPH!",
                    self.x,
                    self.y - 30,
                    (255, 230, 40),
                    AssetManager.get_instance().get_font("normal"),
                )
                break


class PuffShroom(Plant):
    """
    Free night mushroom (0 sun).
    Shoots spores at zombies within 3 tiles (320 px).
    """

    def __init__(self, row: int, col: int):
        super().__init__("puff_shroom", row, col)
        self.shoot_interval = 1.45
        self.shoot_timer = 1.0
        self.range = 320.0

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

        has_target = any(z.is_alive and 0 < (z.x - self.x) <= self.range for z in zombies_in_row)

        if has_target and self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            projectiles_list.append(Pea(self.x + 28, self.y - 4, self.row))


class FumeShroom(Plant):
    """
    Shoots piercing fume cloud that hits all zombies in range and ignores shields!
    """

    def __init__(self, row: int, col: int):
        super().__init__("fume_shroom", row, col)
        self.shoot_interval = 1.6
        self.shoot_timer = 1.0
        self.range = 380.0

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

        has_target = any(z.is_alive and 0 < (z.x - self.x) <= self.range for z in zombies_in_row)

        if has_target and self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            projectiles_list.append(FumeSpore(self.x + 36, self.y - 4, self.row))

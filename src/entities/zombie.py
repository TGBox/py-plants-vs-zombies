"""
Zombie base class and all specialized zombie variants.
Includes Normal, Conehead, Buckethead, Flag, PoleVaulter, Newspaper,
Football, ScreenDoor, Disco, Backup, and Gargantuar.
"""

import math
from typing import TYPE_CHECKING
import pygame
from assets import AssetManager, apply_tint
from config import CELL_HEIGHT, GRID_ROWS, GRID_START_Y, ZOMBIE_SPECS

if TYPE_CHECKING:
    from entities.plant import Plant
    from systems.particle import ParticleSystem


class Zombie:
    def __init__(self, zombie_type: str, row: int, start_x: float = 1280.0):
        self.zombie_type = zombie_type
        self.row = row
        self.x = start_x
        self.y = float(GRID_START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2 - 8)

        spec = ZOMBIE_SPECS[zombie_type]
        self.hp = float(spec["hp"])
        self.max_hp = float(spec["hp"])
        self.base_speed = float(spec["speed"])
        self.speed = self.base_speed
        self.bite_dps = float(spec.get("bite_dps", 100.0))

        self.is_alive = True
        self.is_eating = False
        self.target_plant: "Plant | None" = None

        self.freeze_timer = 0.0
        self.flash_timer = 0.0
        self.walk_anim_timer = 0.0
        self.bite_anim_timer = 0.0

        self.assets = AssetManager.get_instance()
        self.image = self.assets.get_image(f"zombies/zombie_{zombie_type}")
        self.width = 96
        self.height = 128

    def take_damage(self, amount: float):
        self.hp -= amount
        self.flash_timer = 0.12
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def apply_freeze(self, duration: float = 4.0):
        self.freeze_timer = max(self.freeze_timer, duration)

    def get_hitbox(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - 30), int(self.y - 50), 60, 105)

    def update(
        self,
        dt: float,
        plants_in_row: list["Plant"],
        particle_sys: "ParticleSystem",
        spawned_zombies_list: list["Zombie"] | None = None,
    ):
        self.walk_anim_timer += dt
        if self.flash_timer > 0:
            self.flash_timer -= dt

        is_frozen = self.freeze_timer > 0
        if is_frozen:
            self.freeze_timer -= dt

        speed_mult = 0.5 if is_frozen else 1.0

        self.is_eating = False
        self.target_plant = None

        z_hitbox = self.get_hitbox()
        for plant in plants_in_row:
            if plant.is_alive and z_hitbox.colliderect(plant.get_hitbox()):
                if plant.x <= self.x + 15:
                    self.is_eating = True
                    self.target_plant = plant
                    break

        if self.is_eating and self.target_plant:
            self.bite_anim_timer += dt * speed_mult
            chew_amount = self.bite_dps * dt * speed_mult
            self.target_plant.take_damage(chew_amount)
            if not self.target_plant.is_alive:
                self.is_eating = False
                self.target_plant = None
        else:
            self.x -= self.speed * speed_mult * dt

    def render(self, surface: pygame.Surface):
        if self.is_eating:
            chomp = math.sin(self.bite_anim_timer * 12.0) * 3.0
            draw_x = self.x - chomp
            draw_y = self.y
        else:
            bob = math.sin(self.walk_anim_timer * 4.0) * 2.5
            draw_x = self.x
            draw_y = self.y + bob

        rendered_img = self.image

        # Freeze blue overlay (preserves alpha completely!)
        if self.freeze_timer > 0:
            rendered_img = apply_tint(rendered_img, (110, 185, 255), blend_mode=pygame.BLEND_RGB_MULT)

        # Hit flash white/red (preserves alpha completely!)
        if self.flash_timer > 0:
            rendered_img = apply_tint(rendered_img, (180, 180, 180), blend_mode=pygame.BLEND_RGB_ADD)

        rect = rendered_img.get_rect(center=(int(draw_x), int(draw_y)))
        surface.blit(rendered_img, rect)


class NormalZombie(Zombie):
    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("normal", row, start_x)


class ConeheadZombie(Zombie):
    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("conehead", row, start_x)
        self.img_normal = self.assets.get_image("zombies/zombie_normal")

    def update(
        self,
        dt: float,
        plants_in_row: list["Plant"],
        particle_sys: "ParticleSystem",
        spawned_zombies_list: list["Zombie"] | None = None,
    ):
        super().update(dt, plants_in_row, particle_sys, spawned_zombies_list)
        if self.hp <= 200.0:
            self.image = self.img_normal


class BucketheadZombie(Zombie):
    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("buckethead", row, start_x)
        self.img_normal = self.assets.get_image("zombies/zombie_normal")

    def update(
        self,
        dt: float,
        plants_in_row: list["Plant"],
        particle_sys: "ParticleSystem",
        spawned_zombies_list: list["Zombie"] | None = None,
    ):
        super().update(dt, plants_in_row, particle_sys, spawned_zombies_list)
        if self.hp <= 200.0:
            self.image = self.img_normal


class FlagZombie(Zombie):
    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("flag", row, start_x)


class PoleVaulterZombie(Zombie):
    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("polevaulter", row, start_x)
        self.has_vaulted = False
        self.is_vaulting = False
        self.vault_timer = 0.0
        self.vault_duration = 0.8
        self.vault_start_x = 0.0
        self.vault_target_x = 0.0
        self.img_normal = self.assets.get_image("zombies/zombie_normal")

    def update(
        self,
        dt: float,
        plants_in_row: list["Plant"],
        particle_sys: "ParticleSystem",
        spawned_zombies_list: list["Zombie"] | None = None,
    ):
        if self.is_vaulting:
            self.vault_timer += dt
            t = min(1.0, self.vault_timer / self.vault_duration)
            self.x = self.vault_start_x + (self.vault_target_x - self.vault_start_x) * t
            jump_h = math.sin(t * math.pi) * 60.0
            self.y = (GRID_START_Y + self.row * CELL_HEIGHT + CELL_HEIGHT // 2 - 8) - jump_h

            if t >= 1.0:
                self.is_vaulting = False
                self.has_vaulted = True
                self.speed = 22.0
                self.image = self.img_normal
                self.y = float(GRID_START_Y + self.row * CELL_HEIGHT + CELL_HEIGHT // 2 - 8)
                particle_sys.spawn_splat(self.x, self.y + 20)
            return

        if not self.has_vaulted:
            for plant in plants_in_row:
                if plant.is_alive and (plant.x < self.x) and (self.x - plant.x < 75.0):
                    self.is_vaulting = True
                    self.vault_timer = 0.0
                    self.vault_start_x = self.x
                    self.vault_target_x = plant.x - 55.0
                    particle_sys.add_floating_text(
                        "HOPP!",
                        self.x,
                        self.y - 40,
                        (255, 230, 40),
                        AssetManager.get_instance().get_font("normal"),
                    )
                    return

        super().update(dt, plants_in_row, particle_sys, spawned_zombies_list)


class NewspaperZombie(Zombie):
    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("newspaper", row, start_x)
        self.has_newspaper = True
        self.img_angry = self.assets.get_image("zombies/zombie_newspaper_angry")

    def update(
        self,
        dt: float,
        plants_in_row: list["Plant"],
        particle_sys: "ParticleSystem",
        spawned_zombies_list: list["Zombie"] | None = None,
    ):
        if self.has_newspaper and self.hp <= 200.0:
            self.has_newspaper = False
            self.speed = float(ZOMBIE_SPECS["newspaper"]["enraged_speed"])
            self.image = self.img_angry
            particle_sys.spawn_splat(self.x, self.y)
            particle_sys.add_floating_text(
                "GRRRR!",
                self.x,
                self.y - 35,
                (255, 30, 30),
                AssetManager.get_instance().get_font("large"),
            )

        super().update(dt, plants_in_row, particle_sys, spawned_zombies_list)


class FootballZombie(Zombie):
    """Heavy armor and fast sprinter."""

    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("football", row, start_x)
        self.img_normal = self.assets.get_image("zombies/zombie_normal")

    def update(
        self,
        dt: float,
        plants_in_row: list["Plant"],
        particle_sys: "ParticleSystem",
        spawned_zombies_list: list["Zombie"] | None = None,
    ):
        super().update(dt, plants_in_row, particle_sys, spawned_zombies_list)
        # When helmet is lost (HP <= 200), reverts to normal sprite and speed
        if self.hp <= 200.0:
            self.image = self.img_normal
            self.speed = 22.0


class ScreenDoorZombie(Zombie):
    """Holds a screen door that blocks front attacks."""

    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("screendoor", row, start_x)
        self.img_normal = self.assets.get_image("zombies/zombie_normal")

    def update(
        self,
        dt: float,
        plants_in_row: list["Plant"],
        particle_sys: "ParticleSystem",
        spawned_zombies_list: list["Zombie"] | None = None,
    ):
        super().update(dt, plants_in_row, particle_sys, spawned_zombies_list)
        if self.hp <= 200.0:
            self.image = self.img_normal


class DiscoZombie(Zombie):
    """Periodically dances and summons 4 Backup Dancers!"""

    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("disco", row, start_x)
        self.summon_interval = 14.0
        self.summon_timer = 5.0  # first summon after 5s

    def update(
        self,
        dt: float,
        plants_in_row: list["Plant"],
        particle_sys: "ParticleSystem",
        spawned_zombies_list: list["Zombie"] | None = None,
    ):
        super().update(dt, plants_in_row, particle_sys, spawned_zombies_list)
        self.summon_timer += dt

        if self.summon_timer >= self.summon_interval and spawned_zombies_list is not None:
            self.summon_timer = 0.0
            particle_sys.add_floating_text(
                "BOOGIE!",
                self.x,
                self.y - 45,
                (255, 60, 200),
                AssetManager.get_instance().get_font("large"),
            )
            # Summon backup dancers: top row, bottom row, ahead, behind
            offsets = [
                (self.row - 1, self.x),
                (self.row + 1, self.x),
                (self.row, self.x - 70.0),
                (self.row, self.x + 70.0),
            ]
            for r, zx in offsets:
                if 0 <= r < GRID_ROWS:
                    dancer = BackupZombie(r, zx)
                    spawned_zombies_list.append(dancer)
                    particle_sys.spawn_splat(zx, dancer.y)


class BackupZombie(Zombie):
    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("backup", row, start_x)


class Gargantuar(Zombie):
    """Massive boss zombie with 3000 HP. Smashes plants instantly!"""

    def __init__(self, row: int, start_x: float = 1280.0):
        super().__init__("gargantuar", row, start_x)
        self.width = 112
        self.height = 144
        self.smash_timer = 0.0

    def get_hitbox(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - 45), int(self.y - 65), 90, 130)

    def update(
        self,
        dt: float,
        plants_in_row: list["Plant"],
        particle_sys: "ParticleSystem",
        spawned_zombies_list: list["Zombie"] | None = None,
    ):
        self.walk_anim_timer += dt
        if self.flash_timer > 0:
            self.flash_timer -= dt

        is_frozen = self.freeze_timer > 0
        if is_frozen:
            self.freeze_timer -= dt

        speed_mult = 0.5 if is_frozen else 1.0

        # Check plant in range to smash!
        target_plant = None
        for plant in plants_in_row:
            if plant.is_alive and 0 <= (self.x - plant.x) <= 65.0:
                target_plant = plant
                break

        if target_plant:
            self.smash_timer += dt * speed_mult
            if self.smash_timer >= 0.8:
                self.smash_timer = 0.0
                target_plant.take_damage(9999.0)  # SMASH!
                particle_sys.spawn_explosion(target_plant.x, target_plant.y)
                particle_sys.add_floating_text(
                    "BASH!",
                    self.x,
                    self.y - 40,
                    (255, 40, 20),
                    AssetManager.get_instance().get_font("title"),
                )
        else:
            self.smash_timer = 0.0
            self.x -= self.speed * speed_mult * dt

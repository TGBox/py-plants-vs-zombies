"""
Wave management system.
Controls zombie spawning cadence, wave progression, huge wave warnings, and level completion.
"""

import random
from typing import TYPE_CHECKING
import pygame
from assets import AssetManager
from config import VIRTUAL_HEIGHT, VIRTUAL_WIDTH
from entities.zombie import (
    BucketheadZombie,
    ConeheadZombie,
    FlagZombie,
    NewspaperZombie,
    NormalZombie,
    PoleVaulterZombie,
    Zombie,
)

if TYPE_CHECKING:
    from systems.particle import ParticleSystem


class WaveManager:
    def __init__(
        self,
        total_waves: int,
        active_rows: list[int],
        allowed_zombie_types: list[str],
        is_endless: bool = False,
    ):
        self.total_waves = total_waves
        self.active_rows = active_rows
        self.allowed_zombie_types = allowed_zombie_types
        self.is_endless = is_endless

        self.current_wave = 0
        self.wave_timer = 0.0
        self.wave_delay = 14.0  # seconds before first wave
        self.is_wave_active = False

        self.huge_wave_banner_timer = 0.0
        self.huge_wave_active = False

        self.zombies_killed_total = 0
        self.font_huge = AssetManager.get_instance().get_font("huge")
        self.font_medium = AssetManager.get_instance().get_font("medium")

    def get_progress(self) -> float:
        """Returns progress ratio between 0.0 and 1.0 for HUD progress bar."""
        if self.is_endless:
            return min(1.0, (self.current_wave % 10) / 10.0)
        return min(1.0, self.current_wave / max(1, self.total_waves))

    def is_huge_wave(self, wave_index: int) -> bool:
        if self.is_endless:
            return wave_index % 5 == 0 and wave_index > 0
        return wave_index == self.total_waves or (self.total_waves >= 8 and wave_index == self.total_waves // 2)

    def trigger_huge_wave_warning(self):
        self.huge_wave_banner_timer = 3.5
        self.huge_wave_active = True

    def spawn_zombie(self, zombie_type: str, row: int, offset_x: float = 0.0) -> Zombie:
        start_x = VIRTUAL_WIDTH + 40.0 + offset_x
        if zombie_type == "conehead":
            return ConeheadZombie(row, start_x)
        elif zombie_type == "buckethead":
            return BucketheadZombie(row, start_x)
        elif zombie_type == "flag":
            return FlagZombie(row, start_x)
        elif zombie_type == "polevaulter":
            return PoleVaulterZombie(row, start_x)
        elif zombie_type == "newspaper":
            return NewspaperZombie(row, start_x)
        else:
            return NormalZombie(row, start_x)

    def generate_wave(self) -> list[Zombie]:
        self.current_wave += 1
        zombies: list[Zombie] = []

        is_huge = self.is_huge_wave(self.current_wave)
        if is_huge:
            self.trigger_huge_wave_warning()

        # Count of zombies scales with wave progression
        if self.is_endless:
            count = 3 + self.current_wave * 2
        else:
            progress_ratio = self.current_wave / self.total_waves
            count = int(2 + progress_ratio * 7)

        if is_huge:
            count += len(self.active_rows) * 2

        # In a huge wave, include a FlagZombie leading the charge
        if is_huge:
            flag_row = random.choice(self.active_rows)
            zombies.append(self.spawn_zombie("flag", flag_row, offset_x=0.0))

        # Weight zombie types: normal is common, special types appear more later
        types_pool = []
        for z_type in self.allowed_zombie_types:
            if z_type == "normal":
                types_pool.extend(["normal"] * 6)
            elif z_type == "conehead":
                types_pool.extend(["conehead"] * 4)
            elif z_type == "buckethead":
                types_pool.extend(["buckethead"] * 2)
            elif z_type in ("polevaulter", "newspaper"):
                types_pool.extend([z_type] * 3)

        if not types_pool:
            types_pool = ["normal"]

        for i in range(count):
            row = random.choice(self.active_rows)
            z_type = random.choice(types_pool)
            offset_x = random.uniform(10.0, 180.0) + (i * 20.0)
            zombies.append(self.spawn_zombie(z_type, row, offset_x))

        return zombies

    def update(self, dt: float, active_zombies: list[Zombie]) -> list[Zombie]:
        new_zombies = []

        if self.huge_wave_banner_timer > 0:
            self.huge_wave_banner_timer -= dt
            if self.huge_wave_banner_timer <= 0:
                self.huge_wave_active = False

        self.wave_timer += dt

        # Spawn next wave if timer is up or all zombies are defeated
        should_spawn = False
        if not self.is_endless and self.current_wave >= self.total_waves:
            # All waves already spawned
            pass
        else:
            if self.current_wave == 0:
                if self.wave_timer >= self.wave_delay:
                    should_spawn = True
            else:
                if len(active_zombies) == 0 and self.wave_timer >= 6.0:
                    should_spawn = True
                elif self.wave_timer >= 28.0:
                    should_spawn = True

        if should_spawn:
            self.wave_timer = 0.0
            new_zombies = self.generate_wave()

        return new_zombies

    def is_level_completed(self, active_zombies: list[Zombie]) -> bool:
        if self.is_endless:
            return False
        return self.current_wave >= self.total_waves and len(active_zombies) == 0

    def render_overlay(self, surface: pygame.Surface):
        if self.huge_wave_banner_timer > 0:
            # Flashing red and black warning banner
            flash = (pygame.time.get_ticks() // 200) % 2 == 0
            banner_surf = pygame.Surface((VIRTUAL_WIDTH, 90), pygame.SRCALPHA)
            bg_color = (180, 20, 20, 220) if flash else (120, 10, 10, 220)
            banner_surf.fill(bg_color)
            pygame.draw.line(banner_surf, (255, 230, 40), (0, 0), (VIRTUAL_WIDTH, 0), 4)
            pygame.draw.line(banner_surf, (255, 230, 40), (0, 86), (VIRTUAL_WIDTH, 86), 4)

            text_str = "EINE RIESIGE WELLE NÄHERT SICH!"
            text_surf = self.font_large = AssetManager.get_instance().get_font("large").render(text_str, True, (255, 245, 60))
            shadow_surf = AssetManager.get_instance().get_font("large").render(text_str, True, (30, 0, 0))

            bx = (VIRTUAL_WIDTH - text_surf.get_width()) // 2
            by = 22

            banner_surf.blit(shadow_surf, (bx + 3, by + 3))
            banner_surf.blit(text_surf, (bx, by))

            surface.blit(banner_surf, (0, VIRTUAL_HEIGHT // 2 - 45))

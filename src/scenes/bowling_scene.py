"""
Wall-nut Bowling minigame scene.
Conveyor belt dispenses rolling nuts. Player places nuts behind the red foul line.
Nuts roll down lanes, crush zombies, and ricochet diagonally to other rows!
"""

import random
import pygame
from assets import AssetManager
from config import (
    BOWLING_LINE_X,
    CELL_HEIGHT,
    CELL_WIDTH,
    GRID_ROWS,
    GRID_START_X,
    GRID_START_Y,
    VIRTUAL_HEIGHT,
    VIRTUAL_WIDTH,
)
from entities.lawn_mower import LawnMower
from entities.projectile import BowlingNut
from entities.zombie import (
    BucketheadZombie,
    ConeheadZombie,
    FlagZombie,
    NewspaperZombie,
    NormalZombie,
    PoleVaulterZombie,
    Zombie,
)
from scenes.scene_manager import Scene, SceneManager
from systems.particle import ParticleSystem
from ui.button import Button
from ui.dialogs import GameOverDialog, PauseDialog


class ConveyorNut:
    def __init__(self, nut_type: str, x: float, y: float):
        self.nut_type = nut_type  # "regular" or "explosive"
        self.x = x
        self.y = y
        self.rect = pygame.Rect(int(x), int(y), 70, 70)
        self.target_x = x

    def update(self, dt: float, target_x: float):
        self.target_x = target_x
        if self.x > self.target_x:
            self.x = max(self.target_x, self.x - 120.0 * dt)
        self.rect.x = int(self.x)


class BowlingScene(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager)
        self.assets = AssetManager.get_instance()
        self.bg_img = self.assets.get_image("backgrounds/lawn_bowling")
        self.font_score = self.assets.get_font("large")
        self.font_title = self.assets.get_font("medium")
        self.font_desc = self.assets.get_font("small")

        self.particle_sys = ParticleSystem()
        self.zombies: list[Zombie] = []
        self.rolling_nuts: list[BowlingNut] = []
        self.lawn_mowers: list[LawnMower] = []

        # Conveyor belt state
        self.conveyor_nuts: list[ConveyorNut] = []
        self.conveyor_spawn_timer = 0.0
        self.conveyor_interval = 3.2
        self.selected_nut_type: str | None = None

        # Zombie wave state
        self.spawn_timer = 0.0
        self.score = 0
        self.zombies_killed = 0

        # UI & Buttons
        self.btn_pause = Button((VIRTUAL_WIDTH - 210, 15, 95, 42), "Pause", self.toggle_pause, "small", "wood")
        self.btn_fs = Button((VIRTUAL_WIDTH - 105, 15, 95, 42), "Vollbild", self.manager.toggle_fullscreen, "tiny", "gray")

        self.is_paused = False
        self.is_game_over = False

        self.pause_dialog = PauseDialog(
            on_resume=self.toggle_pause,
            on_restart=self.restart_game,
            on_fullscreen=self.manager.toggle_fullscreen,
            on_menu=self.return_to_menu,
        )
        self.game_over_dialog = GameOverDialog(
            on_retry=self.restart_game,
            on_menu=self.return_to_menu,
        )

        self.nut_img = pygame.transform.smoothscale(self.assets.get_image("plants/wallnut"), (60, 60))
        self.cherry_img = pygame.transform.smoothscale(self.assets.get_image("plants/cherry_bomb"), (60, 60))

    def on_enter(self, **kwargs):
        self.is_paused = False
        self.is_game_over = False
        self.score = 0
        self.zombies_killed = 0
        self.conveyor_spawn_timer = 2.0
        self.spawn_timer = 0.0

        self.zombies.clear()
        self.rolling_nuts.clear()
        self.conveyor_nuts.clear()
        self.lawn_mowers.clear()
        self.particle_sys = ParticleSystem()

        # Place lawn mowers on all 5 rows
        for r in range(GRID_ROWS):
            self.lawn_mowers.append(LawnMower(r))

        # Give 2 initial nuts on conveyor
        self.conveyor_nuts.append(ConveyorNut("regular", 500, 30))
        self.conveyor_nuts.append(ConveyorNut("regular", 580, 30))

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def restart_game(self):
        self.on_enter()

    def return_to_menu(self):
        self.manager.switch_to("menu")

    def spawn_zombie(self):
        row = random.randint(0, GRID_ROWS - 1)
        r = random.random()
        start_x = VIRTUAL_WIDTH + random.uniform(20, 60)

        if r < 0.40:
            z = NormalZombie(row, start_x)
        elif r < 0.65:
            z = ConeheadZombie(row, start_x)
        elif r < 0.80:
            z = NewspaperZombie(row, start_x)
        elif r < 0.92:
            z = PoleVaulterZombie(row, start_x)
        else:
            z = BucketheadZombie(row, start_x)

        self.zombies.append(z)

    def handle_event(self, event: pygame.event.Event, mouse_pos: tuple[int, int]):
        if self.is_game_over:
            self.game_over_dialog.handle_event(event, mouse_pos)
            return

        if self.is_paused:
            self.pause_dialog.handle_event(event, mouse_pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.toggle_pause()
            return

        if self.btn_pause.handle_event(event, mouse_pos):
            return
        if self.btn_fs.handle_event(event, mouse_pos):
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 1. Check Conveyor Nut click
            for nut in self.conveyor_nuts:
                if nut.rect.collidepoint(mouse_pos):
                    self.selected_nut_type = nut.nut_type
                    self.conveyor_nuts.remove(nut)
                    return

            # 2. Check placement on bowling lawn
            if self.selected_nut_type:
                mx, my = mouse_pos
                # Can only drop behind the red foul line (x < BOWLING_LINE_X and inside grid y)
                if (GRID_START_X - 40) <= mx < BOWLING_LINE_X and GRID_START_Y <= my <= (GRID_START_Y + 5 * CELL_HEIGHT):
                    row = int((my - GRID_START_Y) // CELL_HEIGHT)
                    row = max(0, min(GRID_ROWS - 1, row))
                    y_center = GRID_START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2

                    new_bowling_nut = BowlingNut(float(mx), float(y_center), row)
                    if self.selected_nut_type == "explosive":
                        new_bowling_nut.damage = 1800.0  # instant kill
                    self.rolling_nuts.append(new_bowling_nut)
                    self.selected_nut_type = None
                    self.particle_sys.spawn_splat(mx, y_center)
                    return

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # Cancel selection
            if self.selected_nut_type:
                self.conveyor_nuts.append(ConveyorNut(self.selected_nut_type, 300, 30))
                self.selected_nut_type = None

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        if self.is_paused:
            self.pause_dialog.update(mouse_pos)
            return

        if self.is_game_over:
            self.game_over_dialog.update(mouse_pos)
            return

        self.btn_pause.update(mouse_pos)
        self.btn_fs.update(mouse_pos)

        # 1. Update Conveyor Belt
        self.conveyor_spawn_timer += dt
        if self.conveyor_spawn_timer >= self.conveyor_interval and len(self.conveyor_nuts) < 5:
            self.conveyor_spawn_timer = 0.0
            n_type = "explosive" if random.random() < 0.20 else "regular"
            self.conveyor_nuts.append(ConveyorNut(n_type, 650, 30))

        # Position conveyor nuts
        for i, nut in enumerate(self.conveyor_nuts):
            target_x = 180 + i * 80
            nut.update(dt, target_x)

        # 2. Spawn Zombies
        self.spawn_timer += dt
        spawn_delay = max(2.5, 6.0 - (self.score / 2000.0))
        if self.spawn_timer >= spawn_delay:
            self.spawn_timer = 0.0
            self.spawn_zombie()

        # 3. Update Rolling Nuts and Collisions
        for nut in self.rolling_nuts:
            nut.update(dt)
            n_hitbox = nut.get_hitbox()

            for z in self.zombies:
                if z.is_alive and z.row == nut.row and id(z) not in nut.hit_cooldown_zombies:
                    if n_hitbox.colliderect(z.get_hitbox()):
                        nut.hit_cooldown_zombies.add(id(z))
                        z.take_damage(nut.damage)
                        self.score += 100
                        self.particle_sys.spawn_splat(z.x, z.y)

                        if not z.is_alive:
                            self.zombies_killed += 1
                            self.score += 150
                            self.particle_sys.add_floating_text(
                                "+250",
                                z.x,
                                z.y - 25,
                                (255, 230, 40),
                                self.font_title,
                            )

                        # Ricochet bounce to adjacent row!
                        nut.on_hit_zombie()
                        break

        self.rolling_nuts = [n for n in self.rolling_nuts if n.is_alive]

        # 4. Update Zombies & Lawn Mowers
        for z in self.zombies:
            z.update(dt, [], self.particle_sys)  # No plants in bowling

            # Check Lawn Mower trigger
            if z.x <= (GRID_START_X - 10):
                for mower in self.lawn_mowers:
                    if mower.row == z.row and not mower.is_active and mower.is_alive:
                        mower.activate()

            # Check Breach
            if z.x <= (GRID_START_X - 70):
                self.is_game_over = True
                self.manager.save_mgr.record_bowling_score(self.score)
                return

        for mower in self.lawn_mowers:
            mower.update(dt)
            if mower.is_active:
                m_rect = mower.get_hitbox()
                for z in self.zombies:
                    if z.is_alive and z.row == mower.row and m_rect.colliderect(z.get_hitbox()):
                        z.take_damage(9999.0)
                        self.particle_sys.spawn_splat(z.x, z.y)
                        self.score += 100

        self.lawn_mowers = [m for m in self.lawn_mowers if m.is_alive]
        self.zombies = [z for z in self.zombies if z.is_alive]

        # 5. Particles
        self.particle_sys.update(dt)

    def render(self, surface: pygame.Surface):
        # 1. Background
        surface.blit(self.bg_img, (0, 0))

        # 2. Conveyor Belt Tray UI
        tray_rect = pygame.Rect(160, 20, 440, 90)
        pygame.draw.rect(surface, (50, 50, 55), tray_rect, border_radius=10)
        pygame.draw.rect(surface, (90, 95, 105), tray_rect, width=3, border_radius=10)

        # Draw Conveyor Nuts
        for nut in self.conveyor_nuts:
            img = self.cherry_img if nut.nut_type == "explosive" else self.nut_img
            surface.blit(img, (nut.x + 5, nut.y + 5))

        # 3. Score Board
        score_surf = self.font_score.render(f"Punkte: {self.score}", True, (255, 235, 60))
        surface.blit(score_surf, (640, 30))

        # Highscore display
        hs = self.manager.save_mgr.data.get("bowling_highscore", 0)
        hs_surf = self.font_desc.render(f"Rekord: {max(hs, self.score)}", True, (220, 220, 220))
        surface.blit(hs_surf, (640, 75))

        # 4. Buttons
        self.btn_pause.render(surface)
        self.btn_fs.render(surface)

        # 5. Lawn Mowers
        for mower in self.lawn_mowers:
            mower.render(surface)

        # 6. Zombies
        self.zombies.sort(key=lambda z: (z.row, z.y))
        for z in self.zombies:
            z.render(surface)

        # 7. Rolling Nuts
        for nut in self.rolling_nuts:
            nut.render(surface)

        # 8. Particle System
        self.particle_sys.render(surface)

        # 9. Cursor preview if holding a nut
        if self.selected_nut_type:
            raw_mouse = pygame.mouse.get_pos()
            vm = self.manager.window_to_virtual_coords(raw_mouse)
            img = self.cherry_img if self.selected_nut_type == "explosive" else self.nut_img
            surface.blit(img, (vm[0] - 30, vm[1] - 30))

        # 10. Dialogs
        if self.is_paused:
            self.pause_dialog.render(surface)
        elif self.is_game_over:
            self.game_over_dialog.render(surface)

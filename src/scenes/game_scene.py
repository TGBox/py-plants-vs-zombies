"""
Core gameplay scene for Campaign levels and Endless Mode.
Orchestrates lawn grid, plant placement, zombie waves, combat collisions, and game state.
"""

import random
import pygame
from assets import AssetManager
from config import (
    CAMPAIGN_LEVELS,
    CELL_HEIGHT,
    CELL_WIDTH,
    GRID_ROWS,
    GRID_START_X,
    GRID_START_Y,
    PLANT_SPECS,
    VIRTUAL_HEIGHT,
    VIRTUAL_WIDTH,
)
from entities.lawn_mower import LawnMower
from entities.plant import (
    CherryBomb,
    Peashooter,
    Plant,
    PotatoMine,
    SnowPea,
    Sunflower,
    Wallnut,
)
from entities.projectile import BowlingNut, Pea, Projectile, SnowPea as SnowPeaProj
from entities.sun import Sun
from entities.zombie import Zombie
from scenes.scene_manager import Scene, SceneManager
from systems.grid import LawnGrid
from systems.particle import ParticleSystem
from systems.wave_manager import WaveManager
from ui.dialogs import GameOverDialog, LevelWonDialog, PauseDialog
from ui.hud import HUD


class GameScene(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager)
        self.assets = AssetManager.get_instance()

        self.level_num = 1
        self.is_endless = False
        self.current_sun = 150
        self.is_night = False

        self.grid: LawnGrid = LawnGrid()
        self.wave_mgr: WaveManager | None = None
        self.particle_sys: ParticleSystem = ParticleSystem()
        self.hud: HUD | None = None

        self.zombies: list[Zombie] = []
        self.projectiles: list[Projectile] = []
        self.suns: list[Sun] = []
        self.lawn_mowers: list[LawnMower] = []

        self.natural_sun_timer = 0.0
        self.natural_sun_interval = 9.0

        # Game state flags
        self.is_paused = False
        self.is_game_over = False
        self.is_level_won = False

        # Dialogs
        self.pause_dialog: PauseDialog | None = None
        self.won_dialog: LevelWonDialog | None = None
        self.game_over_dialog: GameOverDialog | None = None

        self.bg_img = self.assets.get_image("backgrounds/lawn_day")

    def on_enter(self, level_num: int = 1, is_endless: bool = False):
        self.level_num = level_num
        self.is_endless = is_endless
        self.is_paused = False
        self.is_game_over = False
        self.is_level_won = False

        self.zombies.clear()
        self.projectiles.clear()
        self.suns.clear()
        self.lawn_mowers.clear()
        self.particle_sys = ParticleSystem()

        # Find level spec or setup endless
        if self.is_endless:
            lvl_spec = {
                "level_num": 99,
                "title_de": "Endlos-Modus",
                "bg": "lawn_day",
                "initial_sun": 200,
                "available_plants": ["peashooter", "sunflower", "wallnut", "cherry_bomb", "snow_pea", "potato_mine"],
                "active_rows": [0, 1, 2, 3, 4],
                "total_waves": 9999,
                "zombie_types": ["normal", "conehead", "buckethead", "flag", "polevaulter", "newspaper"],
                "unlock_reward": None,
            }
        else:
            lvl_idx = min(self.level_num - 1, len(CAMPAIGN_LEVELS) - 1)
            lvl_spec = CAMPAIGN_LEVELS[lvl_idx]

        self.current_sun = lvl_spec["initial_sun"]
        self.is_night = (lvl_spec["bg"] == "lawn_night")
        self.bg_img = self.assets.get_image(f"backgrounds/{lvl_spec['bg']}")

        active_rows = lvl_spec["active_rows"]
        self.grid = LawnGrid(active_rows=active_rows)

        # Initialize Lawn Mowers for active rows
        for r in active_rows:
            self.lawn_mowers.append(LawnMower(r))

        # Initialize Wave Manager
        self.wave_mgr = WaveManager(
            total_waves=lvl_spec["total_waves"],
            active_rows=active_rows,
            allowed_zombie_types=lvl_spec["zombie_types"],
            is_endless=self.is_endless,
        )

        # Initialize HUD
        self.hud = HUD(
            available_plants=lvl_spec["available_plants"],
            on_pause_click=self.toggle_pause,
            on_fullscreen_toggle=self.manager.toggle_fullscreen,
        )

        # Dialog instances
        self.pause_dialog = PauseDialog(
            on_resume=self.toggle_pause,
            on_restart=self.restart_level,
            on_fullscreen=self.manager.toggle_fullscreen,
            on_menu=self.return_to_menu,
        )

        self.game_over_dialog = GameOverDialog(
            on_retry=self.restart_level,
            on_menu=self.return_to_menu,
        )

        self.won_dialog = LevelWonDialog(
            unlocked_plant_id=lvl_spec.get("unlock_reward"),
            on_continue=self.advance_level,
        )

        self.natural_sun_timer = 3.0  # first natural sun falls soon

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def restart_level(self):
        self.on_enter(self.level_num, self.is_endless)

    def return_to_menu(self):
        self.manager.switch_to("menu")

    def advance_level(self):
        # Save progress and unlock plant
        lvl_idx = self.level_num - 1
        if lvl_idx < len(CAMPAIGN_LEVELS):
            reward = CAMPAIGN_LEVELS[lvl_idx].get("unlock_reward")
            if reward:
                self.manager.save_mgr.unlock_plant(reward)

        next_level = self.level_num + 1
        if next_level <= len(CAMPAIGN_LEVELS):
            self.manager.save_mgr.set_campaign_level(next_level)
            self.on_enter(next_level, False)
        else:
            self.return_to_menu()

    def spawn_plant_instance(self, plant_type: str, row: int, col: int) -> Plant:
        if plant_type == "sunflower":
            return Sunflower(row, col)
        elif plant_type == "peashooter":
            return Peashooter(row, col)
        elif plant_type == "snow_pea":
            return SnowPea(row, col)
        elif plant_type == "wallnut":
            return Wallnut(row, col)
        elif plant_type == "cherry_bomb":
            return CherryBomb(row, col)
        elif plant_type == "potato_mine":
            return PotatoMine(row, col)
        else:
            return Plant(plant_type, row, col)

    def handle_event(self, event: pygame.event.Event, mouse_pos: tuple[int, int]):
        if self.is_game_over:
            if self.game_over_dialog:
                self.game_over_dialog.handle_event(event, mouse_pos)
            return

        if self.is_level_won:
            if self.won_dialog:
                self.won_dialog.handle_event(event, mouse_pos)
            return

        if self.is_paused:
            if self.pause_dialog:
                self.pause_dialog.handle_event(event, mouse_pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            return

        # In-game ESC toggles pause
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.toggle_pause()
            return

        # Check HUD clicks (Buttons, Seed Packets, Shovel)
        if self.hud and self.hud.handle_event(event, mouse_pos, self.current_sun):
            return

        # Left mouse click on playfield
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 1. Check Sun collection click
            clicked_sun = False
            for sun in self.suns:
                if sun.is_clicked(mouse_pos[0], mouse_pos[1]):
                    sun.collect()
                    self.particle_sys.spawn_sun_sparkles(sun.x, sun.y)
                    clicked_sun = True
                    break

            if clicked_sun:
                return

            # 2. Check Shovel action on grid
            cell = self.grid.mouse_to_cell(mouse_pos[0], mouse_pos[1])
            if cell and self.hud and self.hud.is_shovel_selected:
                r, c = cell
                removed = self.grid.remove_plant(r, c)
                if removed:
                    self.particle_sys.spawn_splat(removed.x, removed.y)
                    self.hud.select_shovel()  # turn off shovel after use
                return

            # 3. Check Plant placement on grid
            if cell and self.hud and self.hud.selected_plant_type:
                r, c = cell
                plant_type = self.hud.selected_plant_type
                cost = PLANT_SPECS[plant_type]["cost"]

                if self.grid.can_place_plant(r, c) and self.current_sun >= cost:
                    new_plant = self.spawn_plant_instance(plant_type, r, c)
                    if self.grid.place_plant(new_plant):
                        self.current_sun -= cost
                        self.hud.trigger_cooldown(plant_type)
                        self.hud.deselect_all()
                        self.particle_sys.spawn_splat(new_plant.x, new_plant.y)
                return

        # Right click cancels any selection
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if self.hud:
                self.hud.deselect_all()

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        if self.is_paused:
            if self.pause_dialog:
                self.pause_dialog.update(mouse_pos)
            return

        if self.is_game_over:
            if self.game_over_dialog:
                self.game_over_dialog.update(mouse_pos)
            return

        if self.is_level_won:
            if self.won_dialog:
                self.won_dialog.update(mouse_pos)
            return

        # 1. Update HUD
        if self.hud:
            self.hud.update(dt, mouse_pos)

        # 2. Natural Sun Falling (slower at night)
        if not self.is_night:
            self.natural_sun_timer += dt
            if self.natural_sun_timer >= self.natural_sun_interval:
                self.natural_sun_timer = 0.0
                drop_x = random.uniform(GRID_START_X + 40, GRID_START_X + 9 * CELL_WIDTH - 40)
                self.suns.append(Sun(drop_x, -40.0, is_from_plant=False))

        # 3. Update Suns
        for sun in self.suns:
            if sun.update(dt):
                self.current_sun += Sun.VALUE
                self.particle_sys.add_floating_text(
                    f"+{Sun.VALUE}",
                    85,
                    55,
                    (255, 235, 40),
                    self.assets.get_font("normal"),
                )
        self.suns = [s for s in self.suns if s.is_alive]

        # 4. Update Grid and Plants
        self.grid.update()
        for plant in self.grid.get_all_plants():
            zombies_in_row = [z for z in self.zombies if z.row == plant.row and z.is_alive]
            plant.update(dt, zombies_in_row, self.projectiles, self.suns, self.particle_sys)

        # 5. Update Projectiles and Collisions
        for proj in self.projectiles:
            proj.update(dt)
            if not proj.is_alive:
                continue

            # Collision with zombies in same row
            p_hitbox = proj.get_hitbox()
            for z in self.zombies:
                if z.is_alive and z.row == proj.row and p_hitbox.colliderect(z.get_hitbox()):
                    z.take_damage(proj.damage)
                    if isinstance(proj, SnowPeaProj):
                        z.apply_freeze(proj.slow_duration)
                        self.particle_sys.spawn_splat(proj.x, proj.y, is_ice=True)
                    else:
                        self.particle_sys.spawn_splat(proj.x, proj.y, is_ice=False)

                    proj.is_alive = False
                    if not z.is_alive:
                        self.wave_mgr.zombies_killed_total += 1
                    break

        self.projectiles = [p for p in self.projectiles if p.is_alive]

        # 6. Update Zombies & Lawn Mowers
        for z in self.zombies:
            plants_in_row = self.grid.get_plants_in_row(z.row)
            z.update(dt, plants_in_row, self.particle_sys)

            # Check Lawn Mower activation
            if z.x <= (GRID_START_X - 10):
                for mower in self.lawn_mowers:
                    if mower.row == z.row and not mower.is_active and mower.is_alive:
                        mower.activate()
                        self.particle_sys.add_floating_text(
                            "WROOOM!",
                            mower.x + 30,
                            mower.y - 20,
                            (255, 60, 40),
                            self.assets.get_font("large"),
                        )

            # Check Breach (Game Over)
            if z.x <= (GRID_START_X - 70):
                # Zombie reached the house and lawn mower is gone!
                self.is_game_over = True
                if self.is_endless:
                    self.manager.save_mgr.record_endless_score(
                        self.wave_mgr.current_wave,
                        self.wave_mgr.zombies_killed_total,
                    )
                return

        # 7. Update Lawn Mowers
        for mower in self.lawn_mowers:
            mower.update(dt)
            if mower.is_active:
                m_rect = mower.get_hitbox()
                for z in self.zombies:
                    if z.is_alive and z.row == mower.row and m_rect.colliderect(z.get_hitbox()):
                        z.take_damage(9999.0)  # instant kill
                        self.particle_sys.spawn_splat(z.x, z.y)
                        self.wave_mgr.zombies_killed_total += 1

        self.lawn_mowers = [m for m in self.lawn_mowers if m.is_alive]

        # Remove dead zombies
        self.zombies = [z for z in self.zombies if z.is_alive]

        # 8. Update Wave Manager
        if self.wave_mgr:
            new_z = self.wave_mgr.update(dt, self.zombies)
            self.zombies.extend(new_z)

            # Check Level Won
            if self.wave_mgr.is_level_completed(self.zombies):
                self.is_level_won = True

        # 9. Update Particles
        self.particle_sys.update(dt)

    def render(self, surface: pygame.Surface):
        # 1. Background
        surface.blit(self.bg_img, (0, 0))

        # 2. Grid Highlights
        raw_mouse = pygame.mouse.get_pos()
        v_mouse = self.manager.window_to_virtual_coords(raw_mouse)
        hovered_cell = self.grid.mouse_to_cell(v_mouse[0], v_mouse[1])

        is_valid = False
        if hovered_cell and self.hud:
            r, c = hovered_cell
            if self.hud.selected_plant_type:
                cost = PLANT_SPECS[self.hud.selected_plant_type]["cost"]
                is_valid = self.grid.can_place_plant(r, c) and self.current_sun >= cost
            elif self.hud.is_shovel_selected:
                is_valid = not self.grid.is_cell_empty(r, c)

        self.grid.render_overlay(surface, hovered_cell, is_valid)

        # 3. Lawn Mowers
        for mower in self.lawn_mowers:
            mower.render(surface)

        # 4. Plants
        # Sort plants by row so front rows overlap properly
        all_plants = self.grid.get_all_plants()
        all_plants.sort(key=lambda p: p.row)
        for plant in all_plants:
            plant.render(surface)

        # 5. Zombies
        # Sort zombies by row and y so lower rows overlap upper ones
        self.zombies.sort(key=lambda z: (z.row, z.y))
        for z in self.zombies:
            z.render(surface)

        # 6. Projectiles
        for proj in self.projectiles:
            proj.render(surface)

        # 7. Suns
        for sun in self.suns:
            sun.render(surface)

        # 8. Particles and Text
        self.particle_sys.render(surface)

        # 9. Wave Manager Warning Banners
        if self.wave_mgr:
            self.wave_mgr.render_overlay(surface)

        # 10. HUD
        if self.hud and self.wave_mgr:
            self.hud.render(surface, self.current_sun, self.wave_mgr.get_progress())

        # 11. Modal Dialogs
        if self.is_paused and self.pause_dialog:
            self.pause_dialog.render(surface)
        elif self.is_game_over and self.game_over_dialog:
            self.game_over_dialog.render(surface)
        elif self.is_level_won and self.won_dialog:
            self.won_dialog.render(surface)

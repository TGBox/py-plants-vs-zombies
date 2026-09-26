"""
Main Menu scene with campaign start, endless mode, bowling minigame, and almanac access.
"""

import math
import pygame
from assets import AssetManager
from config import TITLE, VIRTUAL_HEIGHT, VIRTUAL_WIDTH
from scenes.scene_manager import Scene, SceneManager
from ui.button import Button


class MenuScene(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager)
        self.assets = AssetManager.get_instance()
        self.bg_img = self.assets.get_image("backgrounds/menu_bg")
        self.font_title = self.assets.get_font("huge")
        self.font_sub = self.assets.get_font("medium")
        self.font_info = self.assets.get_font("small")

        # Decorative sprites
        self.peashooter_img = self.assets.get_image("plants/peashooter")
        self.sunflower_img = self.assets.get_image("plants/sunflower")
        self.zombie_img = self.assets.get_image("zombies/zombie_normal")
        self.conehead_img = self.assets.get_image("zombies/zombie_conehead")

        btn_w, btn_h = 350, 56
        bx = 100
        start_y = 230
        spacing = 70

        self.btn_campaign = Button(
            (bx, start_y, btn_w, btn_h),
            "Abenteuer",
            self.on_start_campaign,
            "large",
            "green",
        )
        self.btn_endless = Button(
            (bx, start_y + spacing, btn_w, btn_h),
            "Endlos-Modus",
            self.on_start_endless,
            "large",
            "wood",
        )
        self.btn_bowling = Button(
            (bx, start_y + spacing * 2, btn_w, btn_h),
            "Wallnuss-Bowling",
            self.on_start_bowling,
            "medium",
            "wood",
        )
        self.btn_almanac = Button(
            (bx, start_y + spacing * 3, btn_w, btn_h),
            "Almanach (Lexikon)",
            self.on_open_almanac,
            "medium",
            "gray",
        )
        self.btn_fullscreen = Button(
            (bx, start_y + spacing * 4, btn_w, btn_h),
            "Vollbild umschalten (F11)",
            self.on_toggle_fs,
            "normal",
            "gray",
        )
        self.btn_quit = Button(
            (bx, start_y + spacing * 5, btn_w, btn_h),
            "Beenden",
            self.on_quit,
            "normal",
            "gray",
        )

        self.buttons = [
            self.btn_campaign,
            self.btn_endless,
            self.btn_bowling,
            self.btn_almanac,
            self.btn_fullscreen,
            self.btn_quit,
        ]

        self.anim_timer = 0.0

    def on_start_campaign(self):
        saved_level = self.manager.save_mgr.data.get("campaign_level", 1)
        self.manager.switch_to("game", level_num=saved_level, is_endless=False)

    def on_start_endless(self):
        self.manager.switch_to("game", level_num=1, is_endless=True)

    def on_start_bowling(self):
        self.manager.switch_to("bowling")

    def on_open_almanac(self):
        self.manager.switch_to("almanac")

    def on_toggle_fs(self):
        self.manager.toggle_fullscreen()

    def on_quit(self):
        self.manager.is_running = False

    def handle_event(self, event: pygame.event.Event, mouse_pos: tuple[int, int]):
        for btn in self.buttons:
            if btn.handle_event(event, mouse_pos):
                break

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        self.anim_timer += dt
        for btn in self.buttons:
            btn.update(mouse_pos)

    def render(self, surface: pygame.Surface):
        # 1. Background
        surface.blit(self.bg_img, (0, 0))

        # 2. Game Title with double drop shadow and outline
        title_text = "PFLANZEN GEGEN ZOMBIES"
        t_surf = self.font_title.render(title_text, True, (255, 235, 60))
        t_shadow = self.font_title.render(title_text, True, (20, 40, 10))

        tx = 100
        ty = 80
        surface.blit(t_shadow, (tx + 5, ty + 5))
        surface.blit(t_surf, (tx, ty))

        # Subtitle
        sub_text = "Ein epischer Kampf um deinen Vorgarten"
        sub_surf = self.font_sub.render(sub_text, True, (230, 245, 220))
        surface.blit(sub_surf, (tx + 4, ty + 80))

        # 3. Render Buttons
        for btn in self.buttons:
            btn.render(surface)

        # 4. Save Status Plaque on Gravestone (right side)
        gx, gy = 960, 310
        save_box = pygame.Surface((240, 220), pygame.SRCALPHA)
        pygame.draw.rect(save_box, (55, 55, 65, 200), save_box.get_rect(), border_radius=12)
        pygame.draw.rect(save_box, (100, 100, 115), save_box.get_rect(), width=3, border_radius=12)
        surface.blit(save_box, (gx, gy))

        # Gravestone text header
        h_surf = self.font_sub.render("FORTSCHRITT", True, (240, 230, 180))
        surface.blit(h_surf, (gx + (240 - h_surf.get_width()) // 2, gy + 15))

        # Stats lines
        camp_lvl = self.manager.save_mgr.data.get("campaign_level", 1)
        endless_w = self.manager.save_mgr.data.get("endless_highscore_waves", 0)
        bowl_pts = self.manager.save_mgr.data.get("bowling_highscore", 0)

        l1 = self.font_info.render(f"Kampagne: Level 1-{camp_lvl}", True, (230, 230, 230))
        l2 = self.font_info.render(f"Endlos-Rekord: {endless_w} Wellen", True, (230, 230, 230))
        l3 = self.font_info.render(f"Bowling-Rekord: {bowl_pts} Pkt", True, (230, 230, 230))

        surface.blit(l1, (gx + 20, gy + 70))
        surface.blit(l2, (gx + 20, gy + 110))
        surface.blit(l3, (gx + 20, gy + 150))

        # 5. Animated Characters at the bottom
        # Sunflower dancing
        sunflower_bob = math.sin(self.anim_timer * 4.0) * 8
        surface.blit(self.sunflower_img, (580, 520 + sunflower_bob))

        # Peashooter bobbing
        pea_bob = math.cos(self.anim_timer * 4.0) * 6
        surface.blit(self.peashooter_img, (690, 520 + pea_bob))

        # Zombies shambling
        z_bob = math.sin(self.anim_timer * 3.0) * 5
        surface.blit(self.zombie_img, (830, 480 + z_bob))
        surface.blit(self.conehead_img, (760, 470 - z_bob))

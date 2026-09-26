"""
Almanac scene (Plants and Zombies Encyclopedia / Lexikon).
Displays detailed stats, lore, animated previews, and descriptions in German.
"""

import math
import pygame
from assets import AssetManager
from config import PLANT_SPECS, VIRTUAL_HEIGHT, VIRTUAL_WIDTH, ZOMBIE_SPECS
from scenes.scene_manager import Scene, SceneManager
from ui.button import Button


class AlmanacScene(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager)
        self.assets = AssetManager.get_instance()
        self.bg_img = self.assets.get_image("backgrounds/menu_bg")

        self.font_title = self.assets.get_font("title")
        self.font_name = self.assets.get_font("large")
        self.font_sub = self.assets.get_font("medium")
        self.font_desc = self.assets.get_font("normal")
        self.font_lore = self.assets.get_font("small")

        self.active_tab = "plants"  # "plants" or "zombies"
        self.selected_plant_id = "peashooter"
        self.selected_zombie_id = "normal"

        # Tab navigation buttons
        self.btn_tab_plants = Button((80, 70, 180, 48), "Pflanzen", self.show_plants, "normal", "green")
        self.btn_tab_zombies = Button((280, 70, 180, 48), "Zombies", self.show_zombies, "normal", "wood")
        self.btn_back = Button((VIRTUAL_WIDTH - 220, 70, 140, 48), "Zurück", self.back_to_menu, "normal", "gray")

        self.anim_timer = 0.0

    def show_plants(self):
        self.active_tab = "plants"

    def show_zombies(self):
        self.active_tab = "zombies"

    def back_to_menu(self):
        self.manager.switch_to("menu")

    def handle_event(self, event: pygame.event.Event, mouse_pos: tuple[int, int]):
        if self.btn_tab_plants.handle_event(event, mouse_pos):
            return
        if self.btn_tab_zombies.handle_event(event, mouse_pos):
            return
        if self.btn_back.handle_event(event, mouse_pos):
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.back_to_menu()
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = mouse_pos
            # Check grid selection clicks on left panel (x: 80..520, y: 140..660)
            if self.active_tab == "plants":
                plant_keys = list(PLANT_SPECS.keys())
                for i, p_key in enumerate(plant_keys):
                    col = i % 4
                    row = i // 4
                    card_x = 80 + col * 105
                    card_y = 150 + row * 115
                    if pygame.Rect(card_x, card_y, 90, 100).collidepoint(mx, my):
                        self.selected_plant_id = p_key
                        return
            else:
                zombie_keys = list(ZOMBIE_SPECS.keys())
                for i, z_key in enumerate(zombie_keys):
                    col = i % 4
                    row = i // 4
                    card_x = 80 + col * 105
                    card_y = 150 + row * 115
                    if pygame.Rect(card_x, card_y, 90, 100).collidepoint(mx, my):
                        self.selected_zombie_id = z_key
                        return

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        self.anim_timer += dt
        self.btn_tab_plants.update(mouse_pos)
        self.btn_tab_zombies.update(mouse_pos)
        self.btn_back.update(mouse_pos)

    def render(self, surface: pygame.Surface):
        # 1. Darkened Menu Background
        surface.blit(self.bg_img, (0, 0))
        dim = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        dim.fill((20, 20, 30, 220))
        surface.blit(dim, (0, 0))

        # Title
        title_surf = self.font_title.render("ALMANACH (LEXIKON)", True, (255, 230, 70))
        surface.blit(title_surf, (80, 15))

        # Tab Buttons
        self.btn_tab_plants.color_scheme = "green" if self.active_tab == "plants" else "gray"
        self.btn_tab_zombies.color_scheme = "wood" if self.active_tab == "zombies" else "gray"
        self.btn_tab_plants.render(surface)
        self.btn_tab_zombies.render(surface)
        self.btn_back.render(surface)

        # 2. Left Grid Selection Panel (Wood Plaque)
        grid_panel = pygame.Surface((440, 520), pygame.SRCALPHA)
        pygame.draw.rect(grid_panel, (135, 95, 55, 230), grid_panel.get_rect(), border_radius=14)
        pygame.draw.rect(grid_panel, (85, 55, 30), grid_panel.get_rect(), width=4, border_radius=14)
        surface.blit(grid_panel, (70, 135))

        if self.active_tab == "plants":
            plant_keys = list(PLANT_SPECS.keys())
            for i, p_key in enumerate(plant_keys):
                col = i % 4
                row = i // 4
                cx = 85 + col * 105
                cy = 150 + row * 115
                is_selected = (p_key == self.selected_plant_id)

                # Card tile
                tile_bg = (245, 235, 205) if is_selected else (215, 195, 160)
                tile_rect = pygame.Rect(cx, cy, 90, 100)
                pygame.draw.rect(surface, tile_bg, tile_rect, border_radius=8)
                border_c = (255, 220, 40) if is_selected else (100, 70, 40)
                pygame.draw.rect(surface, border_c, tile_rect, width=3 if is_selected else 2, border_radius=8)

                # Plant image thumbnail
                img = self.assets.get_image(f"plants/{p_key}")
                scaled = pygame.transform.smoothscale(img, (60, 60))
                surface.blit(scaled, (cx + 15, cy + 8))

                # Mini label
                label = self.assets.get_font("tiny").render(PLANT_SPECS[p_key]["name_de"][:10], True, (40, 20, 10))
                surface.blit(label, (cx + (90 - label.get_width()) // 2, cy + 74))

        else:
            zombie_keys = list(ZOMBIE_SPECS.keys())
            for i, z_key in enumerate(zombie_keys):
                col = i % 4
                row = i // 4
                cx = 85 + col * 105
                cy = 150 + row * 115
                is_selected = (z_key == self.selected_zombie_id)

                tile_bg = (245, 235, 205) if is_selected else (215, 195, 160)
                tile_rect = pygame.Rect(cx, cy, 90, 100)
                pygame.draw.rect(surface, tile_bg, tile_rect, border_radius=8)
                border_c = (255, 220, 40) if is_selected else (100, 70, 40)
                pygame.draw.rect(surface, border_c, tile_rect, width=3 if is_selected else 2, border_radius=8)

                img = self.assets.get_image(f"zombies/zombie_{z_key}")
                scaled = pygame.transform.smoothscale(img, (48, 64))
                surface.blit(scaled, (cx + 21, cy + 6))

                label = self.assets.get_font("tiny").render(ZOMBIE_SPECS[z_key]["name_de"][:10], True, (40, 20, 10))
                surface.blit(label, (cx + (90 - label.get_width()) // 2, cy + 74))

        # 3. Right Inspection Showcase Card
        card_w, card_h = 670, 520
        card_x, card_y = 540, 135

        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (245, 240, 220), card_surf.get_rect(), border_radius=14)
        pygame.draw.rect(card_surf, (110, 75, 40), card_surf.get_rect(), width=5, border_radius=14)
        surface.blit(card_surf, (card_x, card_y))

        # Render selected plant details
        if self.active_tab == "plants":
            spec = PLANT_SPECS[self.selected_plant_id]
            # Animated large preview
            p_img = self.assets.get_image(f"plants/{self.selected_plant_id}")
            bounce = math.sin(self.anim_timer * 4.0) * 6
            p_large = pygame.transform.smoothscale(p_img, (130, 130))
            surface.blit(p_large, (card_x + 40, card_y + 40 + int(bounce)))

            # Plant Name
            name_surf = self.font_name.render(spec["name_de"], True, (35, 110, 25))
            surface.blit(name_surf, (card_x + 200, card_y + 35))

            # Stats line
            cost_str = f"Sonnenkosten: {spec['cost']}  |  Aufladezeit: {spec['cooldown']}s  |  KP: {spec['hp']}"
            stats_surf = self.font_lore.render(cost_str, True, (80, 50, 20))
            surface.blit(stats_surf, (card_x + 200, card_y + 80))

            # Divider line
            pygame.draw.line(surface, (180, 160, 130), (card_x + 30, card_y + 185), (card_x + card_w - 30, card_y + 185), 2)

            # Description section
            d_hdr = self.font_sub.render("Fähigkeit:", True, (50, 40, 30))
            surface.blit(d_hdr, (card_x + 40, card_y + 200))
            self._render_wrapped_text(surface, spec["description_de"], self.font_desc, (30, 30, 30), card_x + 40, card_y + 235, card_w - 80, 26)

            # Lore / Story section
            l_hdr = self.font_sub.render("Garten-Geschichten:", True, (50, 40, 30))
            surface.blit(l_hdr, (card_x + 40, card_y + 315))
            self._render_wrapped_text(surface, spec["lore_de"], self.font_lore, (60, 50, 40), card_x + 40, card_y + 355, card_w - 80, 24)

        # Render selected zombie details
        else:
            spec = ZOMBIE_SPECS[self.selected_zombie_id]
            z_img = self.assets.get_image(f"zombies/zombie_{self.selected_zombie_id}")
            bounce = math.sin(self.anim_timer * 3.0) * 5
            z_large = pygame.transform.smoothscale(z_img, (110, 146))
            surface.blit(z_large, (card_x + 50, card_y + 30 + int(bounce)))

            name_surf = self.font_name.render(spec["name_de"], True, (130, 35, 35))
            surface.blit(name_surf, (card_x + 200, card_y + 35))

            stats_str = f"Zähigkeit: {spec['hp']} KP  |  Tempo: {spec['speed']} px/s  |  Biss: {int(spec['bite_dps'])} DPS"
            stats_surf = self.font_lore.render(stats_str, True, (80, 50, 20))
            surface.blit(stats_surf, (card_x + 200, card_y + 80))

            pygame.draw.line(surface, (180, 160, 130), (card_x + 30, card_y + 185), (card_x + card_w - 30, card_y + 185), 2)

            d_hdr = self.font_sub.render("Eigenschaften:", True, (50, 40, 30))
            surface.blit(d_hdr, (card_x + 40, card_y + 200))
            self._render_wrapped_text(surface, spec["description_de"], self.font_desc, (30, 30, 30), card_x + 40, card_y + 235, card_w - 80, 26)

            l_hdr = self.font_sub.render("Zombie-Akte:", True, (50, 40, 30))
            surface.blit(l_hdr, (card_x + 40, card_y + 315))
            self._render_wrapped_text(surface, spec["lore_de"], self.font_lore, (60, 50, 40), card_x + 40, card_y + 355, card_w - 80, 24)

    def _render_wrapped_text(self, surface: pygame.Surface, text: str, font: pygame.font.Font, color: tuple, start_x: int, start_y: int, max_width: int, line_spacing: int):
        words = text.split(" ")
        lines = []
        curr = ""
        for w in words:
            test = curr + " " + w if curr else w
            if font.size(test)[0] < max_width:
                curr = test
            else:
                lines.append(curr)
                curr = w
        if curr:
            lines.append(curr)

        for idx, line in enumerate(lines):
            l_surf = font.render(line, True, color)
            surface.blit(l_surf, (start_x, start_y + idx * line_spacing))

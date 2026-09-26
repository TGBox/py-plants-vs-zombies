"""
In-game HUD system.
Handles Sun bank, seed packet tray, cooldown wipes, shovel, wave progress meter, and HUD buttons.
"""

from collections.abc import Callable
import pygame
from assets import AssetManager
from config import COLOR_BLACK, COLOR_WHITE, PLANT_SPECS, VIRTUAL_WIDTH
from ui.button import Button


class SeedPacket:
    def __init__(self, plant_type: str, index: int, x: int, y: int):
        self.plant_type = plant_type
        self.index = index
        self.rect = pygame.Rect(x, y, 76, 92)

        spec = PLANT_SPECS[plant_type]
        self.cost = spec["cost"]
        self.name_de = spec["name_de"]
        self.cooldown_max = float(spec["cooldown"])
        self.cooldown_timer = 0.0

        self.assets = AssetManager.get_instance()
        self.card_base = self.assets.get_image("ui/seed_packet_base")
        self.plant_img = self.assets.get_image(f"plants/{plant_type}")
        # Scale plant preview image to fit nicely inside card slot
        self.plant_preview = pygame.transform.smoothscale(self.plant_img, (54, 54))

        self.font_cost = self.assets.get_font("small")
        self.font_key = self.assets.get_font("tiny")

    def trigger_cooldown(self):
        self.cooldown_timer = self.cooldown_max

    def is_ready(self, current_sun: int) -> bool:
        return self.cooldown_timer <= 0 and current_sun >= self.cost

    def update(self, dt: float):
        if self.cooldown_timer > 0:
            self.cooldown_timer = max(0.0, self.cooldown_timer - dt)

    def render(self, surface: pygame.Surface, current_sun: int, is_selected: bool):
        # Base card
        card_scaled = pygame.transform.smoothscale(self.card_base, (self.rect.width, self.rect.height))
        surface.blit(card_scaled, self.rect)

        # Plant miniature icon inside card
        px = self.rect.x + (self.rect.width - self.plant_preview.get_width()) // 2
        py = self.rect.y + 12
        surface.blit(self.plant_preview, (px, py))

        # Hotkey number badge in top-left
        key_str = str(self.index + 1)
        key_surf = self.font_key.render(key_str, True, (60, 40, 20))
        surface.blit(key_surf, (self.rect.x + 5, self.rect.y + 4))

        # Sun cost tag at bottom
        cost_str = str(self.cost)
        cost_color = (20, 20, 20) if current_sun >= self.cost else (200, 40, 40)
        cost_surf = self.font_cost.render(cost_str, True, cost_color)
        cx = self.rect.x + (self.rect.width - cost_surf.get_width()) // 2
        cy = self.rect.y + self.rect.height - cost_surf.get_height() - 4
        surface.blit(cost_surf, (cx, cy))

        # Cooldown wipe overlay (from top downwards)
        if self.cooldown_timer > 0:
            ratio = self.cooldown_timer / self.cooldown_max
            wipe_height = int(self.rect.height * ratio)
            if wipe_height > 0:
                shade = pygame.Surface((self.rect.width, wipe_height), pygame.SRCALPHA)
                shade.fill((0, 0, 0, 160))
                surface.blit(shade, (self.rect.x, self.rect.y))

        # Dim overlay if cannot afford sun
        elif current_sun < self.cost:
            dim = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 110))
            surface.blit(dim, self.rect)

        # Selected glowing border
        if is_selected:
            pygame.draw.rect(surface, (255, 230, 40), self.rect, width=3, border_radius=6)


class HUD:
    def __init__(
        self,
        available_plants: list[str],
        on_pause_click: Callable[[], None],
        on_fullscreen_toggle: Callable[[], None],
    ):
        self.assets = AssetManager.get_instance()
        self.sun_counter_bg = self.assets.get_image("ui/sun_counter_bg")
        self.sun_icon = pygame.transform.smoothscale(self.assets.get_image("projectiles/sun"), (46, 46))
        self.shovel_icon = pygame.transform.smoothscale(self.assets.get_image("ui/shovel"), (50, 50))
        self.progress_frame = self.assets.get_image("ui/progress_bar_frame")

        self.font_sun = self.assets.get_font("medium")
        self.font_small = self.assets.get_font("small")
        self.font_tiny = self.assets.get_font("tiny")

        # Top Sun Bank: x=15, y=10
        self.sun_bank_rect = pygame.Rect(15, 10, 140, 54)

        # Seed Packets tray: starts right after sun bank
        self.seed_packets: list[SeedPacket] = []
        tray_x = 165
        for i, plant_type in enumerate(available_plants):
            pkt = SeedPacket(plant_type, i, tray_x + i * 82, 6)
            self.seed_packets.append(pkt)

        # Shovel slot: placed to the right of seed packets
        shovel_x = tray_x + len(available_plants) * 82 + 15
        self.shovel_rect = pygame.Rect(shovel_x, 10, 64, 64)
        self.is_shovel_selected = False

        # Progress bar: top right
        self.progress_rect = pygame.Rect(VIRTUAL_WIDTH - 440, 18, 220, 26)

        # Pause and Fullscreen Buttons
        self.btn_pause = Button(
            rect=(VIRTUAL_WIDTH - 200, 12, 90, 40),
            text="Pause",
            on_click=on_pause_click,
            font_size="small",
            color_scheme="wood",
        )
        self.btn_fs = Button(
            rect=(VIRTUAL_WIDTH - 100, 12, 85, 40),
            text="Vollbild",
            on_click=on_fullscreen_toggle,
            font_size="tiny",
            color_scheme="gray",
        )

        self.selected_plant_type: str | None = None

    def deselect_all(self):
        self.selected_plant_type = None
        self.is_shovel_selected = False

    def select_plant(self, plant_type: str):
        self.selected_plant_type = plant_type
        self.is_shovel_selected = False

    def select_shovel(self):
        self.is_shovel_selected = not self.is_shovel_selected
        self.selected_plant_type = None

    def trigger_cooldown(self, plant_type: str):
        for pkt in self.seed_packets:
            if pkt.plant_type == plant_type:
                pkt.trigger_cooldown()
                break

    def handle_event(self, event: pygame.event.Event, mouse_pos: tuple[int, int], current_sun: int) -> bool:
        if self.btn_pause.handle_event(event, mouse_pos):
            return True
        if self.btn_fs.handle_event(event, mouse_pos):
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check shovel click
            if self.shovel_rect.collidepoint(mouse_pos):
                self.select_shovel()
                return True

            # Check seed packet clicks
            for pkt in self.seed_packets:
                if pkt.rect.collidepoint(mouse_pos):
                    if pkt.is_ready(current_sun):
                        if self.selected_plant_type == pkt.plant_type:
                            self.deselect_all()
                        else:
                            self.select_plant(pkt.plant_type)
                    return True

        elif event.type == pygame.KEYDOWN:
            # Hotkey 'S' for shovel
            if event.key == pygame.K_s:
                self.select_shovel()
                return True
            # Number keys 1..8
            if pygame.K_1 <= event.key <= pygame.K_8:
                idx = event.key - pygame.K_1
                if idx < len(self.seed_packets):
                    pkt = self.seed_packets[idx]
                    if pkt.is_ready(current_sun):
                        self.select_plant(pkt.plant_type)
                    return True

        return False

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        for pkt in self.seed_packets:
            pkt.update(dt)
        self.btn_pause.update(mouse_pos)
        self.btn_fs.update(mouse_pos)

    def render(self, surface: pygame.Surface, current_sun: int, progress: float):
        # 1. Sun Bank
        surface.blit(self.sun_counter_bg, self.sun_bank_rect)
        surface.blit(self.sun_icon, (self.sun_bank_rect.x + 2, self.sun_bank_rect.y + 4))

        sun_text = str(current_sun)
        sun_surf = self.font_sun.render(sun_text, True, (45, 30, 10))
        surface.blit(sun_surf, (self.sun_bank_rect.x + 60, self.sun_bank_rect.y + 12))

        # 2. Seed Packets
        for pkt in self.seed_packets:
            is_sel = self.selected_plant_type == pkt.plant_type
            pkt.render(surface, current_sun, is_sel)

        # 3. Shovel Slot
        shovel_bg = pygame.Surface((self.shovel_rect.width, self.shovel_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shovel_bg, (135, 95, 55), shovel_bg.get_rect(), border_radius=8)
        pygame.draw.rect(shovel_bg, (85, 55, 30), shovel_bg.get_rect(), width=3, border_radius=8)
        surface.blit(shovel_bg, self.shovel_rect)

        # Shovel icon
        surface.blit(self.shovel_icon, (self.shovel_rect.x + 7, self.shovel_rect.y + 7))

        # Hotkey badge 'S'
        badge_surf = self.font_tiny.render("S", True, (240, 240, 220))
        surface.blit(badge_surf, (self.shovel_rect.x + 4, self.shovel_rect.y + 2))

        if self.is_shovel_selected:
            pygame.draw.rect(surface, (255, 230, 40), self.shovel_rect, width=3, border_radius=8)

        # 4. Level Progress Bar
        pygame.draw.rect(surface, (45, 45, 50), self.progress_rect, border_radius=6)
        # Green fill
        fill_w = int(self.progress_rect.width * progress)
        if fill_w > 0:
            fill_rect = pygame.Rect(self.progress_rect.x + 2, self.progress_rect.y + 2, fill_w - 4, self.progress_rect.height - 4)
            pygame.draw.rect(surface, (95, 195, 50), fill_rect, border_radius=4)
        pygame.draw.rect(surface, (140, 145, 155), self.progress_rect, width=2, border_radius=6)

        # Progress text label
        prog_label = self.font_tiny.render("WELLEN", True, (220, 220, 220))
        surface.blit(prog_label, (self.progress_rect.x + (self.progress_rect.width - prog_label.get_width()) // 2, self.progress_rect.y + 5))

        # 5. Buttons
        self.btn_pause.render(surface)
        self.btn_fs.render(surface)

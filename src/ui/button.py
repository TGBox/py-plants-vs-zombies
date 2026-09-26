"""
Interactive UI button component with hover animations and styled German text.
"""

from collections.abc import Callable
import pygame
from assets import AssetManager


class Button:
    def __init__(
        self,
        rect: pygame.Rect | tuple[int, int, int, int],
        text: str,
        on_click: Callable[[], None] | None = None,
        font_size: str = "normal",
        color_scheme: str = "green",
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.font = AssetManager.get_instance().get_font(font_size)
        self.color_scheme = color_scheme
        self.is_hovered = False
        self.is_disabled = False

    def handle_event(self, event: pygame.event.Event, mouse_pos: tuple[int, int]) -> bool:
        if self.is_disabled:
            return False

        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                if self.on_click:
                    self.on_click()
                return True
        return False

    def update(self, mouse_pos: tuple[int, int]):
        if not self.is_disabled:
            self.is_hovered = self.rect.collidepoint(mouse_pos)

    def render(self, surface: pygame.Surface):
        # Determine background color based on scheme and state
        if self.is_disabled:
            bg_top = (120, 120, 120)
            bg_bot = (80, 80, 80)
            border = (60, 60, 60)
            text_color = (180, 180, 180)
        elif self.color_scheme == "green":
            if self.is_hovered:
                bg_top = (120, 225, 95)
                bg_bot = (85, 195, 60)
                border = (35, 120, 30)
            else:
                bg_top = (95, 190, 75)
                bg_bot = (65, 160, 45)
                border = (25, 90, 20)
            text_color = (255, 255, 255)
        elif self.color_scheme == "wood":
            if self.is_hovered:
                bg_top = (210, 155, 95)
                bg_bot = (165, 110, 60)
                border = (110, 70, 35)
            else:
                bg_top = (185, 130, 75)
                bg_bot = (145, 90, 45)
                border = (90, 55, 25)
            text_color = (255, 245, 220)
        else:  # gray / neutral
            if self.is_hovered:
                bg_top = (170, 175, 185)
                bg_bot = (130, 135, 145)
                border = (80, 85, 95)
            else:
                bg_top = (145, 150, 160)
                bg_bot = (110, 115, 125)
                border = (65, 70, 80)
            text_color = (255, 255, 255)

        # Draw rounded button body
        btn_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        # Background bevel
        pygame.draw.rect(btn_surf, bg_bot, btn_surf.get_rect(), border_radius=10)
        # Top highlight half
        top_rect = pygame.Rect(3, 3, self.rect.width - 6, self.rect.height // 2)
        pygame.draw.rect(btn_surf, bg_top, top_rect, border_radius=8)
        # Outer border
        pygame.draw.rect(btn_surf, border, btn_surf.get_rect(), width=3, border_radius=10)

        # Render Text with shadow
        text_surf = self.font.render(self.text, True, text_color)
        shadow_surf = self.font.render(self.text, True, (20, 20, 20))

        # Ensure text never overflows button boundaries
        max_w = self.rect.width - 24
        if text_surf.get_width() > max_w:
            scale = max_w / text_surf.get_width()
            new_w = int(max_w)
            new_h = max(10, int(text_surf.get_height() * scale))
            text_surf = pygame.transform.smoothscale(text_surf, (new_w, new_h))
            shadow_surf = pygame.transform.smoothscale(shadow_surf, (new_w, new_h))

        tx = (self.rect.width - text_surf.get_width()) // 2
        ty = (self.rect.height - text_surf.get_height()) // 2

        btn_surf.blit(shadow_surf, (tx + 2, ty + 2))
        btn_surf.blit(text_surf, (tx, ty))

        surface.blit(btn_surf, self.rect)

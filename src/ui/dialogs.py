"""
Modal dialogs for Pause menu, Level Complete victory screen, and Game Over screen.
"""

from collections.abc import Callable
import pygame
from assets import AssetManager
from config import PLANT_SPECS, VIRTUAL_HEIGHT, VIRTUAL_WIDTH
from ui.button import Button


class PauseDialog:
    def __init__(
        self,
        on_resume: Callable[[], None],
        on_restart: Callable[[], None],
        on_fullscreen: Callable[[], None],
        on_menu: Callable[[], None],
    ):
        self.assets = AssetManager.get_instance()
        self.font_title = self.assets.get_font("title")

        # Dialog Box
        dw, dh = 400, 360
        dx = (VIRTUAL_WIDTH - dw) // 2
        dy = (VIRTUAL_HEIGHT - dh) // 2
        self.rect = pygame.Rect(dx, dy, dw, dh)

        btn_w, btn_h = 240, 50
        bx = dx + (dw - btn_w) // 2

        self.btn_resume = Button((bx, dy + 90, btn_w, btn_h), "Weiterspielen", on_resume, "normal", "green")
        self.btn_restart = Button((bx, dy + 155, btn_w, btn_h), "Level neustarten", on_restart, "normal", "wood")
        self.btn_fs = Button((bx, dy + 220, btn_w, btn_h), "Vollbild (F11)", on_fullscreen, "normal", "gray")
        self.btn_menu = Button((bx, dy + 285, btn_w, btn_h), "Hauptmenü", on_menu, "normal", "wood")

    def handle_event(self, event: pygame.event.Event, mouse_pos: tuple[int, int]) -> bool:
        if self.btn_resume.handle_event(event, mouse_pos):
            return True
        if self.btn_restart.handle_event(event, mouse_pos):
            return True
        if self.btn_fs.handle_event(event, mouse_pos):
            return True
        if self.btn_menu.handle_event(event, mouse_pos):
            return True
        return False

    def update(self, mouse_pos: tuple[int, int]):
        self.btn_resume.update(mouse_pos)
        self.btn_restart.update(mouse_pos)
        self.btn_fs.update(mouse_pos)
        self.btn_menu.update(mouse_pos)

    def render(self, surface: pygame.Surface):
        # Dark dim background
        dim = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 175))
        surface.blit(dim, (0, 0))

        # Wooden / stone plaque
        plaque = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(plaque, (140, 95, 55), plaque.get_rect(), border_radius=16)
        pygame.draw.rect(plaque, (85, 55, 30), plaque.get_rect(), width=5, border_radius=16)
        surface.blit(plaque, self.rect)

        # Title
        title_surf = self.font_title.render("PAUSE", True, (255, 235, 140))
        shadow_surf = self.font_title.render("PAUSE", True, (40, 20, 10))
        tx = self.rect.x + (self.rect.width - title_surf.get_width()) // 2
        ty = self.rect.y + 20
        surface.blit(shadow_surf, (tx + 3, ty + 3))
        surface.blit(title_surf, (tx, ty))

        # Buttons
        self.btn_resume.render(surface)
        self.btn_restart.render(surface)
        self.btn_fs.render(surface)
        self.btn_menu.render(surface)


class LevelWonDialog:
    def __init__(self, unlocked_plant_id: str | None, on_continue: Callable[[], None]):
        self.assets = AssetManager.get_instance()
        self.font_title = self.assets.get_font("title")
        self.font_name = self.assets.get_font("large")
        self.font_desc = self.assets.get_font("normal")
        self.font_lore = self.assets.get_font("small")

        self.unlocked_plant_id = unlocked_plant_id
        self.unlocked_spec = PLANT_SPECS.get(unlocked_plant_id) if unlocked_plant_id else None

        dw, dh = 540, 480 if self.unlocked_spec else 320
        dx = (VIRTUAL_WIDTH - dw) // 2
        dy = (VIRTUAL_HEIGHT - dh) // 2
        self.rect = pygame.Rect(dx, dy, dw, dh)

        btn_w, btn_h = 240, 56
        bx = dx + (dw - btn_w) // 2
        by = dy + dh - 75
        self.btn_continue = Button((bx, by, btn_w, btn_h), "Weiter!", on_continue, "large", "green")

    def handle_event(self, event: pygame.event.Event, mouse_pos: tuple[int, int]) -> bool:
        return self.btn_continue.handle_event(event, mouse_pos)

    def update(self, mouse_pos: tuple[int, int]):
        self.btn_continue.update(mouse_pos)

    def render(self, surface: pygame.Surface):
        dim = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 185))
        surface.blit(dim, (0, 0))

        # Frame
        box = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(box, (70, 120, 50), box.get_rect(), border_radius=18)
        pygame.draw.rect(box, (30, 70, 20), box.get_rect(), width=6, border_radius=18)
        surface.blit(box, self.rect)

        # Header Title
        title_surf = self.font_title.render("LEVEL GESCHAFFT!", True, (255, 235, 60))
        shadow_surf = self.font_title.render("LEVEL GESCHAFFT!", True, (20, 30, 10))
        tx = self.rect.x + (self.rect.width - title_surf.get_width()) // 2
        ty = self.rect.y + 24
        surface.blit(shadow_surf, (tx + 3, ty + 3))
        surface.blit(title_surf, (tx, ty))

        if self.unlocked_spec:
            sub = self.font_desc.render("Neue Pflanze freigeschaltet:", True, (255, 255, 255))
            sx = self.rect.x + (self.rect.width - sub.get_width()) // 2
            surface.blit(sub, (sx, ty + 65))

            # Plant Icon
            p_img = self.assets.get_image(f"plants/{self.unlocked_plant_id}")
            p_scaled = pygame.transform.smoothscale(p_img, (90, 90))
            px = self.rect.x + (self.rect.width - 90) // 2
            py = ty + 105
            surface.blit(p_scaled, (px, py))

            # Plant Name
            name_surf = self.font_name.render(self.unlocked_spec["name_de"], True, (255, 230, 80))
            nx = self.rect.x + (self.rect.width - name_surf.get_width()) // 2
            surface.blit(name_surf, (nx, py + 95))

            # Description
            desc_surf = self.font_desc.render(self.unlocked_spec["description_de"], True, (240, 240, 240))
            dx_pos = self.rect.x + (self.rect.width - desc_surf.get_width()) // 2
            surface.blit(desc_surf, (dx_pos, py + 140))

        self.btn_continue.render(surface)


class GameOverDialog:
    def __init__(self, on_retry: Callable[[], None], on_menu: Callable[[], None]):
        self.assets = AssetManager.get_instance()
        self.font_title = self.assets.get_font("title")
        self.font_sub = self.assets.get_font("large")

        dw, dh = 600, 360
        dx = (VIRTUAL_WIDTH - dw) // 2
        dy = (VIRTUAL_HEIGHT - dh) // 2
        self.rect = pygame.Rect(dx, dy, dw, dh)

        btn_w, btn_h = 240, 54
        bx1 = dx + (dw - btn_w) // 2
        self.btn_retry = Button((bx1, dy + 180, btn_w, btn_h), "Erneut versuchen", on_retry, "normal", "green")
        self.btn_menu = Button((bx1, dy + 250, btn_w, btn_h), "Hauptmenü", on_menu, "normal", "wood")

    def handle_event(self, event: pygame.event.Event, mouse_pos: tuple[int, int]) -> bool:
        if self.btn_retry.handle_event(event, mouse_pos):
            return True
        if self.btn_menu.handle_event(event, mouse_pos):
            return True
        return False

    def update(self, mouse_pos: tuple[int, int]):
        self.btn_retry.update(mouse_pos)
        self.btn_menu.update(mouse_pos)

    def render(self, surface: pygame.Surface):
        dim = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        dim.fill((50, 0, 0, 215))  # bloody dark red
        surface.blit(dim, (0, 0))

        # Grave plaque
        box = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(box, (60, 45, 45), box.get_rect(), border_radius=18)
        pygame.draw.rect(box, (35, 20, 20), box.get_rect(), width=6, border_radius=18)
        surface.blit(box, self.rect)

        # Title
        t1 = self.font_title.render("DIE ZOMBIES HABEN", True, (240, 40, 40))
        t2 = self.font_title.render("DEIN GEHIRN GEGESSEN!", True, (240, 40, 40))
        tx1 = self.rect.x + (self.rect.width - t1.get_width()) // 2
        tx2 = self.rect.x + (self.rect.width - t2.get_width()) // 2
        surface.blit(t1, (tx1, self.rect.y + 35))
        surface.blit(t2, (tx2, self.rect.y + 95))

        self.btn_retry.render(surface)
        self.btn_menu.render(surface)

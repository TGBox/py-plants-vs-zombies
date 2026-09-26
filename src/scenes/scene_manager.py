"""
Scene manager and display scaling handler.
Supports seamless switching between Windowed and Fullscreen modes,
virtual 1280x720 canvas rendering, letterboxing, and mouse coordinate mapping.
"""

from typing import TYPE_CHECKING
import pygame
from config import TITLE, VIRTUAL_HEIGHT, VIRTUAL_WIDTH
from savegame import SaveManager

if TYPE_CHECKING:
    pass


class Scene:
    def __init__(self, scene_manager: "SceneManager"):
        self.manager = scene_manager

    def on_enter(self, **kwargs):
        pass

    def on_exit(self):
        pass

    def handle_event(self, event: pygame.event.Event, mouse_pos: tuple[int, int]):
        pass

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        pass

    def render(self, surface: pygame.Surface):
        pass


class SceneManager:
    def __init__(self, save_mgr: SaveManager):
        self.save_mgr = save_mgr
        self.is_fullscreen = self.save_mgr.data.get("fullscreen", False)

        # Pygame display setup
        pygame.display.set_caption(TITLE)

        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)

        # Virtual 1280x720 render canvas
        self.canvas = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene | None = None
        self.is_running = True

        # Scaling and viewport metrics
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.update_viewport()

    def update_viewport(self):
        win_w, win_h = self.screen.get_size()
        scale_x = win_w / VIRTUAL_WIDTH
        scale_y = win_h / VIRTUAL_HEIGHT
        self.scale = min(scale_x, scale_y)

        scaled_w = int(VIRTUAL_WIDTH * self.scale)
        scaled_h = int(VIRTUAL_HEIGHT * self.scale)

        self.offset_x = (win_w - scaled_w) // 2
        self.offset_y = (win_h - scaled_h) // 2

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.save_mgr.set_fullscreen(self.is_fullscreen)

        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)

        self.update_viewport()

    def window_to_virtual_coords(self, win_pos: tuple[int, int]) -> tuple[int, int]:
        """Translates window mouse coordinates to virtual 1280x720 coordinates."""
        wx, wy = win_pos
        vx = (wx - self.offset_x) / self.scale
        vy = (wy - self.offset_y) / self.scale
        return int(max(0, min(VIRTUAL_WIDTH, vx))), int(max(0, min(VIRTUAL_HEIGHT, vy)))

    def register_scene(self, name: str, scene: Scene):
        self.scenes[name] = scene

    def switch_to(self, name: str, **kwargs):
        if self.current_scene:
            self.current_scene.on_exit()
        self.current_scene = self.scenes[name]
        self.current_scene.on_enter(**kwargs)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.is_running = False
            return

        if event.type == pygame.VIDEORESIZE and not self.is_fullscreen:
            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            self.update_viewport()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            self.toggle_fullscreen()
            return

        # Map mouse coordinates to virtual canvas
        raw_mouse = pygame.mouse.get_pos()
        virtual_mouse = self.window_to_virtual_coords(raw_mouse)

        if self.current_scene:
            self.current_scene.handle_event(event, virtual_mouse)

    def update(self, dt: float):
        raw_mouse = pygame.mouse.get_pos()
        virtual_mouse = self.window_to_virtual_coords(raw_mouse)
        if self.current_scene:
            self.current_scene.update(dt, virtual_mouse)

    def render(self):
        # 1. Render active scene onto the virtual canvas
        if self.current_scene:
            self.current_scene.render(self.canvas)

        # 2. Scale canvas to window with letterboxing
        scaled_w = int(VIRTUAL_WIDTH * self.scale)
        scaled_h = int(VIRTUAL_HEIGHT * self.scale)
        scaled_surf = pygame.transform.smoothscale(self.canvas, (scaled_w, scaled_h))

        self.screen.fill((0, 0, 0))
        self.screen.blit(scaled_surf, (self.offset_x, self.offset_y))
        pygame.display.flip()

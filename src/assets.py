"""
Asset manager and resource loader for Plants vs. Zombies.
Loads, caches, and provides access to images, fonts, and icons.
"""

import os
import pygame


class AssetManager:
    _instance = None

    def __init__(self):
        self.images: dict[str, pygame.Surface] = {}
        self.fonts: dict[str, pygame.font.Font] = {}
        self.initialized = False

    @classmethod
    def get_instance(cls) -> "AssetManager":
        if cls._instance is None:
            cls._instance = AssetManager()
        return cls._instance

    def initialize(self):
        if self.initialized:
            return

        # Ensure pygame font is initialized
        if not pygame.font.get_init():
            pygame.font.init()

        # Load fonts in multiple sizes
        # Prefer Arial, Segoe UI, Trebuchet MS or fallback to default
        font_candidates = ["Arial", "Segoe UI", "Trebuchet MS", "DejaVu Sans"]
        available_fonts = pygame.font.get_fonts()
        selected_font = None
        for candidate in font_candidates:
            if candidate.lower().replace(" ", "") in available_fonts:
                selected_font = candidate
                break

        sizes = {
            "tiny": 14,
            "small": 18,
            "normal": 22,
            "medium": 28,
            "large": 38,
            "title": 52,
            "huge": 68,
        }

        for name, size in sizes.items():
            try:
                self.fonts[name] = pygame.font.SysFont(selected_font, size, bold=True)
            except Exception:
                self.fonts[name] = pygame.font.Font(None, size)

        # Preload all image assets
        self._load_all_images("assets")
        self.initialized = True

    def _load_all_images(self, root_dir: str):
        if not os.path.exists(root_dir):
            return

        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith(".png"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")
                    key = os.path.splitext(rel_path)[0]  # e.g. "plants/peashooter"
                    try:
                        surf = pygame.image.load(full_path)
                        if pygame.display.get_surface() is not None:
                            try:
                                surf = surf.convert_alpha()
                            except Exception:
                                pass
                        self.images[key] = surf
                        # Also register bare filename without subfolder for easy lookup
                        bare_key = os.path.splitext(file)[0]
                        if bare_key not in self.images:
                            self.images[bare_key] = surf
                    except Exception as e:
                        print(f"Failed to load image {full_path}: {e}")

    def get_image(self, key: str, fallback_size: tuple[int, int] = (64, 64)) -> pygame.Surface:
        if key in self.images:
            return self.images[key]

        # Generate a colored placeholder if missing
        print(f"Warning: Image '{key}' not found, creating placeholder.")
        placeholder = pygame.Surface(fallback_size, pygame.SRCALPHA)
        placeholder.fill((200, 100, 200, 200))
        pygame.draw.rect(placeholder, (255, 255, 255), placeholder.get_rect(), 2)
        self.images[key] = placeholder
        return placeholder

    def get_font(self, size_key: str = "normal") -> pygame.font.Font:
        return self.fonts.get(size_key, self.fonts.get("normal", pygame.font.Font(None, 24)))

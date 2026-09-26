"""
Main entry point for Plants vs. Zombies (Pflanzen gegen Zombies).
Initializes Pygame, loads assets, starts the SceneManager, and runs the main loop.
"""

import sys
import pygame
from assets import AssetManager
from config import FPS
from savegame import SaveManager
from scenes.almanac_scene import AlmanacScene
from scenes.bowling_scene import BowlingScene
from scenes.game_scene import GameScene
from scenes.menu_scene import MenuScene
from scenes.scene_manager import SceneManager


def main():
    # Initialize Pygame without audio mixer (user specified no sound)
    pygame.init()
    if pygame.mixer.get_init():
        pygame.mixer.quit()

    # Initialize Savegame
    save_mgr = SaveManager()

    # Initialize Scene Manager & Display (sets display mode)
    scene_mgr = SceneManager(save_mgr)

    # Initialize Assets (textures, fonts)
    assets = AssetManager.get_instance()
    assets.initialize()

    # Register Scenes
    scene_mgr.register_scene("menu", MenuScene(scene_mgr))
    scene_mgr.register_scene("game", GameScene(scene_mgr))
    scene_mgr.register_scene("bowling", BowlingScene(scene_mgr))
    scene_mgr.register_scene("almanac", AlmanacScene(scene_mgr))

    # Start at Main Menu
    scene_mgr.switch_to("menu")

    clock = pygame.time.Clock()

    # Main Game Loop
    while scene_mgr.is_running:
        dt = clock.tick(FPS) / 1000.0
        dt = min(dt, 0.05)  # Cap dt to avoid large delta time jumps

        for event in pygame.event.get():
            scene_mgr.handle_event(event)

        scene_mgr.update(dt)
        scene_mgr.render()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

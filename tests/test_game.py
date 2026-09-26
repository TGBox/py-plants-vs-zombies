"""
Automated validation suite for Plants vs. Zombies clone.
Tests asset loading, entity logic, damage/combat mechanics, saving/loading,
and runs a multi-frame headless simulation.
"""

import os
import sys

# Ensure headless video driver for automated testing
os.environ["SDL_VIDEODRIVER"] = "dummy"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from assets import AssetManager
from config import GRID_ROWS, PLANT_SPECS, ZOMBIE_SPECS
from entities.lawn_mower import LawnMower
from entities.plant import (
    CherryBomb,
    Peashooter,
    PotatoMine,
    SnowPea,
    Sunflower,
    Wallnut,
)
from entities.projectile import BowlingNut, Pea, SnowPea as SnowPeaProj
from entities.sun import Sun
from entities.zombie import (
    BucketheadZombie,
    ConeheadZombie,
    FlagZombie,
    NewspaperZombie,
    NormalZombie,
    PoleVaulterZombie,
)
from savegame import SaveManager
from scenes.almanac_scene import AlmanacScene
from scenes.bowling_scene import BowlingScene
from scenes.game_scene import GameScene
from scenes.menu_scene import MenuScene
from scenes.scene_manager import SceneManager
from systems.grid import LawnGrid
from systems.particle import ParticleSystem
from systems.wave_manager import WaveManager


def test_assets():
    print("Testing asset loading...")
    pygame.init()
    pygame.display.set_mode((1280, 720))
    assets = AssetManager.get_instance()
    assets.initialize()

    # Verify essential assets
    assert assets.get_image("backgrounds/lawn_day") is not None
    assert assets.get_image("backgrounds/lawn_night") is not None
    assert assets.get_image("plants/peashooter") is not None
    assert assets.get_image("plants/sunflower") is not None
    assert assets.get_image("plants/wallnut") is not None
    assert assets.get_image("zombies/zombie_normal") is not None
    assert assets.get_image("projectiles/pea") is not None
    assert assets.get_image("projectiles/sun") is not None
    assert assets.get_font("normal") is not None
    print("  -> Assets OK!")


def test_savegame():
    print("Testing savegame manager...")
    test_file = "test_save.json"
    if os.path.exists(test_file):
        os.remove(test_file)

    sm = SaveManager(test_file)
    assert sm.data["campaign_level"] == 1

    sm.set_campaign_level(3)
    assert sm.data["campaign_level"] == 3

    sm.unlock_plant("cherry_bomb")
    assert "cherry_bomb" in sm.data["unlocked_plants"]

    sm.record_endless_score(15, 120)
    assert sm.data["endless_highscore_waves"] == 15
    assert sm.data["endless_highscore_zombies"] == 120

    sm.record_bowling_score(2400)
    assert sm.data["bowling_highscore"] == 2400

    # Reload from disk to verify persistence
    sm2 = SaveManager(test_file)
    assert sm2.data["campaign_level"] == 3
    assert "cherry_bomb" in sm2.data["unlocked_plants"]
    assert sm2.data["bowling_highscore"] == 2400

    if os.path.exists(test_file):
        os.remove(test_file)
    print("  -> Savegame persistence OK!")


def test_grid_and_plants():
    print("Testing grid and plant interactions...")
    grid = LawnGrid(active_rows=[0, 1, 2, 3, 4])
    assert grid.can_place_plant(2, 4)

    peashooter = Peashooter(2, 4)
    assert grid.place_plant(peashooter)
    assert not grid.can_place_plant(2, 4)  # Now occupied
    assert grid.get_plant(2, 4) == peashooter

    # Shovel removal
    removed = grid.remove_plant(2, 4)
    assert removed == peashooter
    assert grid.can_place_plant(2, 4)  # Empty again
    print("  -> Grid & Plant placement OK!")


def test_combat_mechanics():
    print("Testing combat physics and zombie behaviors...")
    ps = ParticleSystem()
    zombies = [NormalZombie(row=2, start_x=800.0)]
    projectiles = []
    suns = []

    peashooter = Peashooter(2, 0)
    # Update peashooter until it fires a pea
    for _ in range(120):
        peashooter.update(0.016, zombies, projectiles, suns, ps)

    assert len(projectiles) > 0
    pea = projectiles[0]
    assert isinstance(pea, Pea)
    assert pea.row == 2

    # Simulate pea hitting normal zombie
    initial_z_hp = zombies[0].hp
    pea.x = zombies[0].x  # move directly to zombie
    assert pea.get_hitbox().colliderect(zombies[0].get_hitbox())
    zombies[0].take_damage(pea.damage)
    assert zombies[0].hp == initial_z_hp - pea.damage

    # Test Newspaper zombie rage
    np_z = NewspaperZombie(row=1, start_x=600.0)
    assert np_z.has_newspaper
    assert np_z.speed == float(ZOMBIE_SPECS["newspaper"]["speed"])
    np_z.take_damage(160.0)  # destroy newspaper
    np_z.update(0.016, [], ps)
    assert not np_z.has_newspaper
    assert np_z.speed == float(ZOMBIE_SPECS["newspaper"]["enraged_speed"])

    # Test Pole Vaulter jump
    pv_z = PoleVaulterZombie(row=0, start_x=450.0)
    wallnut = Wallnut(row=0, col=2)
    wallnut.x = 400.0  # place plant ahead
    assert not pv_z.has_vaulted
    # Update until vault triggers
    for _ in range(60):
        pv_z.update(0.02, [wallnut], ps)
    assert pv_z.is_vaulting or pv_z.has_vaulted

    # Test Bowling ricochet
    bowling_nut = BowlingNut(x=500.0, y=300.0, row=2)
    bowling_nut.on_hit_zombie()
    assert bowling_nut.row in (1, 3)

    print("  -> Combat & Zombie mechanics OK!")


def test_scenes_and_simulation():
    print("Testing scene manager and headless simulation loop...")
    save_mgr = SaveManager("test_sim_save.json")
    sm = SceneManager(save_mgr)

    menu = MenuScene(sm)
    game = GameScene(sm)
    bowling = BowlingScene(sm)
    almanac = AlmanacScene(sm)

    sm.register_scene("menu", menu)
    sm.register_scene("game", game)
    sm.register_scene("bowling", bowling)
    sm.register_scene("almanac", almanac)

    # Test Menu -> Almanac -> Bowling -> Game
    sm.switch_to("menu")
    assert sm.current_scene == menu

    sm.switch_to("almanac")
    assert sm.current_scene == almanac
    almanac.show_zombies()
    almanac.show_plants()

    sm.switch_to("bowling")
    assert sm.current_scene == bowling

    sm.switch_to("game", level_num=1)
    assert sm.current_scene == game

    # Run 180 simulation frames (approx 3 seconds of in-game time)
    for _ in range(180):
        sm.update(0.016)
        sm.render()

    if os.path.exists("test_sim_save.json"):
        os.remove("test_sim_save.json")

    print("  -> Scene simulation loop OK!")


def main():
    test_assets()
    test_savegame()
    test_grid_and_plants()
    test_combat_mechanics()
    test_scenes_and_simulation()
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY! (100% OK)")


if __name__ == "__main__":
    main()

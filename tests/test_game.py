"""
Automated validation suite for Plants vs. Zombies clone.
Tests asset loading, tinting/alpha transparency, entity logic, damage/combat mechanics,
new plants & zombies, bowling nut variants (Cherry explosion, Giant steamroller, Ice nut),
saving/loading, and runs a multi-frame headless simulation.
"""

import os
import sys

# Ensure headless video driver for automated testing
os.environ["SDL_VIDEODRIVER"] = "dummy"

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(1, ROOT_DIR)

import pygame
from assets import AssetManager, apply_tint
from config import GRID_ROWS, PLANT_SPECS, ZOMBIE_SPECS
from entities.lawn_mower import LawnMower
from entities.plant import (
    CherryBomb,
    Chomper,
    FumeShroom,
    Jalapeno,
    Peashooter,
    Plant,
    PotatoMine,
    PuffShroom,
    Repeater,
    SnowPea,
    Squash,
    Sunflower,
    Wallnut,
)
from entities.projectile import (
    BaseBowlingNut,
    BowlingCherryNut,
    BowlingGiantNut,
    BowlingIceNut,
    BowlingNut,
    FumeSpore,
    JalapenoFlame,
    Pea,
    SnowPea as SnowPeaProj,
)
from entities.sun import Sun
from entities.zombie import (
    BackupZombie,
    BucketheadZombie,
    ConeheadZombie,
    DiscoZombie,
    FlagZombie,
    FootballZombie,
    Gargantuar,
    NewspaperZombie,
    NormalZombie,
    PoleVaulterZombie,
    ScreenDoorZombie,
    Zombie,
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


def test_assets_and_tinting():
    print("Testing asset loading and alpha tinting...")
    pygame.init()
    pygame.display.set_mode((1280, 720))
    assets = AssetManager.get_instance()
    assets.initialize()

    # Verify essential assets
    assert assets.get_image("backgrounds/lawn_day") is not None
    assert assets.get_image("backgrounds/lawn_night") is not None
    assert assets.get_image("backgrounds/lawn_bowling") is not None
    assert assets.get_image("backgrounds/menu_bg") is not None

    # Verify all 12 plant images
    for p_id in PLANT_SPECS:
        img = assets.get_image(f"plants/{p_id}")
        assert img is not None, f"Plant asset missing: {p_id}"

    # Verify all 11 zombie images
    for z_id in ZOMBIE_SPECS:
        img = assets.get_image(f"zombies/zombie_{z_id}")
        assert img is not None, f"Zombie asset missing: {z_id}"

    # Verify potato mine specific stages & projectiles
    assert assets.get_image("plants/potato_mine_unarmed") is not None
    assert assets.get_image("plants/potato_mine_armed") is not None
    assert assets.get_image("projectiles/bowling_giant_nut") is not None
    assert assets.get_image("projectiles/bowling_ice_nut") is not None
    assert assets.get_image("projectiles/fume_spore") is not None
    assert assets.get_image("projectiles/jalapeno_fire") is not None

    # Test alpha preservation in damage tinting (Fix for colored rectangle bug)
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))  # fully transparent
    surf.fill((100, 200, 100, 255), rect=pygame.Rect(8, 8, 16, 16))  # opaque center

    tinted = apply_tint(surf, (255, 60, 60))
    # Corner pixel must STILL be 100% transparent (alpha == 0)
    corner_alpha = tinted.get_at((0, 0)).a
    assert corner_alpha == 0, f"Transparent pixel gained alpha: {corner_alpha}!"
    # Center pixel must have been tinted and remain opaque
    center_pixel = tinted.get_at((12, 12))
    assert center_pixel.a == 255
    assert center_pixel.r > 100  # Red boost from tint

    print("  -> Assets & Alpha Tinting OK!")


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
    print("Testing combat physics and plant/zombie behaviors...")
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
    pea.x = zombies[0].x
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
    wallnut.x = 400.0
    assert not pv_z.has_vaulted
    for _ in range(60):
        pv_z.update(0.02, [wallnut], ps)
    assert pv_z.is_vaulting or pv_z.has_vaulted

    # Test Potato Mine arming & detonation
    mine = PotatoMine(row=2, col=2)
    assert not mine.is_armed
    # Advance time until armed
    for _ in range(350):
        mine.update(0.05, zombies, projectiles, suns, ps)
    assert mine.is_armed
    # Zombie walks over armed mine
    zombies[0].x = mine.x
    mine.update(0.05, zombies, projectiles, suns, ps)
    assert not mine.is_alive  # Exploded!
    assert not zombies[0].is_alive  # Zombie blown up!

    # Test Repeater double shot
    repeater = Repeater(row=3, col=0)
    r_zombies = [NormalZombie(row=3, start_x=700.0)]
    r_projs = []
    for _ in range(120):
        repeater.update(0.016, r_zombies, r_projs, suns, ps)
    assert len(r_projs) >= 2  # Fired pea pair

    # Test Jalapeno line flame
    jalapeno = Jalapeno(row=4, col=1)
    j_projs = []
    for _ in range(120):
        jalapeno.update(0.016, [], j_projs, suns, ps)
    assert any(isinstance(p, JalapenoFlame) for p in j_projs)

    # Test Disco Zombie summoning dancers
    disco = DiscoZombie(row=2, start_x=600.0)
    dancers = []
    disco.summon_timer = 20.0  # trigger summon (interval is 14.0s)
    disco.update(0.1, [], ps, spawned_zombies_list=dancers)
    assert len(dancers) > 0, "Disco zombie failed to summon backup dancers"

    print("  -> Combat & Zombie mechanics OK!")


def test_bowling_mechanics():
    print("Testing Wall-nut Bowling nut variants...")
    ps = ParticleSystem()

    # 1. Regular Nut Ricochet
    dummy_z = NormalZombie(row=2, start_x=500.0)
    all_z = [dummy_z]
    bowling_nut = BowlingNut(x=500.0, y=300.0, row=2)
    pts = bowling_nut.on_hit_zombie(dummy_z, ps, all_z)
    assert pts == 100
    assert bowling_nut.row in (1, 3)

    # 2. Explosive Cherry Nut (3x3 massive blast)
    cherry_nut = BowlingCherryNut(x=500.0, y=300.0, row=2)
    z1 = NormalZombie(row=1, start_x=505.0)
    z2 = NormalZombie(row=2, start_x=500.0)
    z3 = NormalZombie(row=3, start_x=510.0)
    z_cluster = [z1, z2, z3]
    pts = cherry_nut.on_hit_zombie(z2, ps, z_cluster)
    assert not cherry_nut.is_alive  # Exploded!
    assert not z1.is_alive  # Obliterated!
    assert not z2.is_alive  # Obliterated!
    assert not z3.is_alive  # Obliterated!
    assert pts >= 500  # Strike combo bonus!

    # 3. Giant Nut (Steamroller)
    giant_nut = BowlingGiantNut(x=400.0, y=300.0, row=2)
    boss_z = Gargantuar(row=2, start_x=410.0)
    pts = giant_nut.on_hit_zombie(boss_z, ps, [boss_z])
    assert giant_nut.is_alive  # Keeps rolling!
    assert not boss_z.is_alive  # Flattened by 9999 damage!

    # 4. Ice Nut (Freeze slow)
    ice_nut = BowlingIceNut(x=500.0, y=300.0, row=2)
    target_z = FootballZombie(row=2, start_x=505.0)
    pts = ice_nut.on_hit_zombie(target_z, ps, [target_z])
    assert not ice_nut.is_alive
    assert target_z.freeze_timer > 0  # Frozen!

    print("  -> Bowling variants OK!")


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


def test_lawn_mower_and_game_over():
    print("Testing lawn mower trigger and game over breach detection...")
    from config import GRID_START_X

    # 1. Verify 15 seconds initial wave delay
    wm = WaveManager(total_waves=5, active_rows=[0, 1, 2, 3, 4], allowed_zombie_types=["normal"])
    assert wm.wave_delay == 15.0, f"Expected 15.0s wave delay, got {wm.wave_delay}s"

    save_mgr = SaveManager("test_mower_save.json")
    sm = SceneManager(save_mgr)
    game = GameScene(sm)
    game.on_enter(level_num=1, is_endless=False)

    # 2. Test lawn mower activation when zombie reaches GRID_START_X - 10
    assert len(game.lawn_mowers) > 0
    active_row = game.lawn_mowers[0].row
    row_mower = [m for m in game.lawn_mowers if m.row == active_row][0]
    assert not row_mower.is_active

    test_z = NormalZombie(row=active_row, start_x=GRID_START_X - 12.0)
    game.zombies.append(test_z)

    # Update frame: mower should activate
    game.update(0.016, (0, 0))
    assert row_mower.is_active, "Lawn mower failed to activate when zombie reached row end!"

    # Run frames until mower clears zombie
    for _ in range(60):
        game.update(0.016, (0, 0))
    assert not test_z.is_alive, "Lawn mower failed to crush zombie!"

    # 3. Test game over when another zombie breaches without mower
    # Remove all lawn mowers in that row
    game.lawn_mowers = [m for m in game.lawn_mowers if m.row != active_row]
    breaching_z = NormalZombie(row=active_row, start_x=GRID_START_X - 75.0)
    game.zombies.append(breaching_z)

    assert not game.is_game_over
    game.update(0.016, (0, 0))
    assert game.is_game_over, "Game Over failed to trigger when zombie breached the house!"

    if os.path.exists("test_mower_save.json"):
        os.remove("test_mower_save.json")

    print("  -> Lawn Mower activation & Game Over breach OK!")


def main():
    test_assets_and_tinting()
    test_savegame()
    test_grid_and_plants()
    test_combat_mechanics()
    test_bowling_mechanics()
    test_scenes_and_simulation()
    test_lawn_mower_and_game_over()
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY! (100% OK)")


if __name__ == "__main__":
    main()

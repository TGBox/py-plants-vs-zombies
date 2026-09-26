"""
Save game manager for Plants vs. Zombies clone.
Handles persistence of campaign progression, high scores, and settings.
"""

import json
import os

SAVE_FILE_PATH = "savegame.json"

DEFAULT_SAVE_DATA = {
    "campaign_level": 1,
    "endless_highscore_waves": 0,
    "endless_highscore_zombies": 0,
    "bowling_highscore": 0,
    "unlocked_plants": ["peashooter"],
    "fullscreen": False,
}


class SaveManager:
    def __init__(self, file_path: str = SAVE_FILE_PATH):
        self.file_path = file_path
        self.data = DEFAULT_SAVE_DATA.copy()
        self.load()

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
            except Exception as e:
                print(f"Error loading savegame, using defaults: {e}")
        else:
            self.save()

    def save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving savegame: {e}")

    def unlock_plant(self, plant_id: str):
        if plant_id and plant_id not in self.data["unlocked_plants"]:
            self.data["unlocked_plants"].append(plant_id)
            self.save()

    def set_campaign_level(self, level: int):
        if level > self.data.get("campaign_level", 1):
            self.data["campaign_level"] = level
            self.save()

    def record_endless_score(self, waves: int, zombies: int):
        updated = False
        if waves > self.data.get("endless_highscore_waves", 0):
            self.data["endless_highscore_waves"] = waves
            updated = True
        if zombies > self.data.get("endless_highscore_zombies", 0):
            self.data["endless_highscore_zombies"] = zombies
            updated = True
        if updated:
            self.save()

    def record_bowling_score(self, score: int):
        if score > self.data.get("bowling_highscore", 0):
            self.data["bowling_highscore"] = score
            self.save()

    def toggle_fullscreen(self) -> bool:
        self.data["fullscreen"] = not self.data.get("fullscreen", False)
        self.save()
        return self.data["fullscreen"]

    def set_fullscreen(self, value: bool):
        self.data["fullscreen"] = value
        self.save()

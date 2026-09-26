"""
Configuration and constants for Plants vs. Zombies clone.
Includes grid layout, plant/zombie stats, colors, and German localized strings.
"""

# Screen & Rendering
VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720
FPS = 60
TITLE = "Pflanzen gegen Zombies"

# Grid Metrics (5 rows x 9 columns)
GRID_START_X = 224
GRID_START_Y = 150
CELL_WIDTH = 104
CELL_HEIGHT = 112
GRID_COLS = 9
GRID_ROWS = 5

# Bowling Minigame Line
BOWLING_LINE_X = GRID_START_X + 3 * CELL_WIDTH  # column 3 boundary (536 px)

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_SUN_YELLOW = (255, 220, 40)
COLOR_UI_TEXT = (245, 240, 225)
COLOR_UI_SHADOW = (40, 30, 20)
COLOR_COOLDOWN_OVERLAY = (0, 0, 0, 160)
COLOR_HIGHLIGHT_VALID = (50, 220, 50, 90)
COLOR_HIGHLIGHT_INVALID = (220, 50, 50, 90)

# Plant Specifications
PLANT_SPECS = {
    "peashooter": {
        "id": "peashooter",
        "name_de": "Erbsenkanone",
        "cost": 100,
        "cooldown": 7.5,
        "hp": 300,
        "description_de": "Verschießt Erbsen auf herannahende Zombies.",
        "lore_de": "Wie kann eine Pflanze so schnell und zielsicher schießen? Erbsenkanone sagt: 'Harte Arbeit, Hingabe und eine ballaststoffreiche Ernährung!'",
        "unlocked_level": 1,
    },
    "sunflower": {
        "id": "sunflower",
        "name_de": "Sonnenblume",
        "cost": 50,
        "cooldown": 7.5,
        "hp": 300,
        "description_de": "Produziert lebenswichtige zusätzliche Sonnenenergie.",
        "lore_de": "Sonnenblumen können gar nicht anders, als zum Takt der Musik zu tanzen. Ihr Optimismus erleuchtet selbst die dunkelste Zombie-Apokalypse.",
        "unlocked_level": 2,
    },
    "wallnut": {
        "id": "wallnut",
        "name_de": "Wallnuss",
        "cost": 50,
        "cooldown": 25.0,
        "hp": 4000,
        "description_de": "Hält Zombies dank extrem harter Schale lange auf.",
        "lore_de": "'Die Leute fragen mich oft, wie es sich anfühlt, von Zombies angeknabbert zu werden', sagt Wallnuss. 'Ehrlich gesagt kitzelt es meistens nur.'",
        "unlocked_level": 3,
    },
    "cherry_bomb": {
        "id": "cherry_bomb",
        "name_de": "Kirschbombe",
        "cost": 150,
        "cooldown": 30.0,
        "hp": 300,
        "description_de": "Explodiert sofort und vernichtet alle Zombies im 3x3-Umfeld.",
        "lore_de": "'Wir explodieren vor Wut!', rufen die Kirsch-Zwillinge im Chor. Niemand weiß genau, worüber sie sich eigentlich ärgern.",
        "unlocked_level": 4,
    },
    "snow_pea": {
        "id": "snow_pea",
        "name_de": "Schneekanone",
        "cost": 175,
        "cooldown": 7.5,
        "hp": 300,
        "description_de": "Verschießt gefrorene Erbsen, die Zombies verlangsamen.",
        "lore_de": "Schneekanone behält stets einen kühlen Kopf. Manche halten ihn für arrogant, aber er ist einfach nur cool.",
        "unlocked_level": 5,
    },
    "potato_mine": {
        "id": "potato_mine",
        "name_de": "Kartoffelmine",
        "cost": 25,
        "cooldown": 25.0,
        "hp": 300,
        "description_de": "Braucht etwas Zeit zum Scharfschalten. Explodiert bei Kontakt.",
        "lore_de": "SPUDOW! Kartoffelmine mag zwar geduldig im Boden verharren, doch wenn sie hochgeht, fliegt die Zombie-Mütze!",
        "unlocked_level": 5,
    },
}

# Zombie Specifications
ZOMBIE_SPECS = {
    "normal": {
        "id": "normal",
        "name_de": "Normaler Zombie",
        "hp": 200,
        "speed": 22.0,  # pixels per second
        "bite_dps": 100.0,
        "description_de": "Der gewöhnliche Garten-Zombie. Liebt frische Gehirne.",
        "lore_de": "Dieser Zombie schätzt die einfachen Dinge im Leben: frische Luft, gemächliche Spaziergänge und appetitliche Gärtner.",
    },
    "conehead": {
        "id": "conehead",
        "name_de": "Pylonen-Zombie",
        "hp": 560,
        "speed": 22.0,
        "bite_dps": 100.0,
        "description_de": "Die Pylone schützt seinen Kopf vor zweifachem Erbsen-Beschuss.",
        "lore_de": "Verkehrssicherheit geht vor – dachte sich dieser Zombie und stülpte sich eine Pylone über den Kopf.",
    },
    "buckethead": {
        "id": "buckethead",
        "name_de": "Eimer-Zombie",
        "hp": 1300,
        "speed": 22.0,
        "bite_dps": 100.0,
        "description_de": "Extrem widerstandsfähig dank feuerverzinktem Metalleimer.",
        "lore_de": "Der Metalleimer schützt nicht nur vor Erbsen, sondern empfängt gelegentlich auch ukrainische Radiosender.",
    },
    "flag": {
        "id": "flag",
        "name_de": "Flaggen-Zombie",
        "hp": 200,
        "speed": 32.0,
        "bite_dps": 100.0,
        "description_de": "Kündigt das Eintreffen einer gewaltigen Zombiewelle an.",
        "lore_de": "Er trägt stolz die Flagge mit dem Gehirn-Symbol voran und motiviert die Horde zum Sprint.",
    },
    "polevaulter": {
        "id": "polevaulter",
        "name_de": "Stabhochspringer",
        "hp": 500,
        "speed": 55.0,  # Fast sprint before vault
        "post_vault_speed": 22.0,
        "bite_dps": 100.0,
        "description_de": "Sprintet heran und überspringt mit dem Stab die erste Pflanze.",
        "lore_de": "Ehemaliger Schulmeister im Stabhochsprung. Trainiert immer noch täglich für die Zombie-Olympiade.",
    },
    "newspaper": {
        "id": "newspaper",
        "name_de": "Zeitungs-Zombie",
        "hp": 350,  # 150 paper + 200 body
        "speed": 18.0,
        "enraged_speed": 62.0,  # Sprints furiously when paper is torn!
        "bite_dps": 100.0,
        "description_de": "Liest friedlich Zeitung. Wird rasend wütend, wenn sie zerstört wird!",
        "lore_de": "Er war gerade beim letzten Sudoku-Rätsel! Wehe dem, der seine Sonntagsausgabe zerfetzt!",
    },
}

# Levels Configuration
CAMPAIGN_LEVELS = [
    {
        "level_num": 1,
        "title_de": "Level 1-1: Die ersten Schritte",
        "bg": "lawn_day",
        "initial_sun": 150,
        "available_plants": ["peashooter"],
        "active_rows": [2],  # Only middle row for tutorial level!
        "total_waves": 6,
        "zombie_types": ["normal"],
        "unlock_reward": "sunflower",
    },
    {
        "level_num": 2,
        "title_de": "Level 1-2: Sonnige Aussichten",
        "bg": "lawn_day",
        "initial_sun": 100,
        "available_plants": ["peashooter", "sunflower"],
        "active_rows": [1, 2, 3],  # 3 rows
        "total_waves": 8,
        "zombie_types": ["normal", "conehead"],
        "unlock_reward": "wallnut",
    },
    {
        "level_num": 3,
        "title_de": "Level 1-3: Harte Nüsse",
        "bg": "lawn_day",
        "initial_sun": 100,
        "available_plants": ["peashooter", "sunflower", "wallnut"],
        "active_rows": [0, 1, 2, 3, 4],  # full 5 rows
        "total_waves": 10,
        "zombie_types": ["normal", "conehead", "polevaulter"],
        "unlock_reward": "cherry_bomb",
    },
    {
        "level_num": 4,
        "title_de": "Level 1-4: Explosive Überraschung",
        "bg": "lawn_day",
        "initial_sun": 125,
        "available_plants": ["peashooter", "sunflower", "wallnut", "cherry_bomb"],
        "active_rows": [0, 1, 2, 3, 4],
        "total_waves": 12,
        "zombie_types": ["normal", "conehead", "buckethead", "polevaulter"],
        "unlock_reward": "snow_pea",
    },
    {
        "level_num": 5,
        "title_de": "Level 1-5: Der Eisige Ansturm",
        "bg": "lawn_day",
        "initial_sun": 150,
        "available_plants": ["peashooter", "sunflower", "wallnut", "cherry_bomb", "snow_pea"],
        "active_rows": [0, 1, 2, 3, 4],
        "total_waves": 14,
        "zombie_types": ["normal", "conehead", "buckethead", "flag", "polevaulter"],
        "unlock_reward": "potato_mine",
    },
    {
        "level_num": 6,
        "title_de": "Level 2-1: Nächtlicher Schrecken",
        "bg": "lawn_night",
        "initial_sun": 150,
        "available_plants": ["peashooter", "sunflower", "wallnut", "cherry_bomb", "snow_pea", "potato_mine"],
        "active_rows": [0, 1, 2, 3, 4],
        "total_waves": 16,
        "zombie_types": ["normal", "conehead", "buckethead", "flag", "newspaper", "polevaulter"],
        "unlock_reward": None,
    },
]

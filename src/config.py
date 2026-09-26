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
        "description_de": "Produziert lebenswichtige zusätzliche Sonnenenergie (+25).",
        "lore_de": "Sonnenblumen können gar nicht anders, als zum Takt der Musik zu tanzen. Ihr Optimismus erleuchtet selbst die dunkelste Zombie-Apokalypse.",
        "unlocked_level": 1,
    },
    "wallnut": {
        "id": "wallnut",
        "name_de": "Wallnuss",
        "cost": 50,
        "cooldown": 25.0,
        "hp": 4000,
        "description_de": "Hält Zombies dank extrem harter Schale lange auf.",
        "lore_de": "'Die Leute fragen mich oft, wie es sich anfühlt, von Zombies angeknabbert zu werden', sagt Wallnuss. 'Ehrlich gesagt kitzelt es meistens nur.'",
        "unlocked_level": 2,
    },
    "cherry_bomb": {
        "id": "cherry_bomb",
        "name_de": "Kirschbombe",
        "cost": 150,
        "cooldown": 30.0,
        "hp": 300,
        "description_de": "Explodiert sofort und vernichtet alle Zombies im 3x3-Umfeld.",
        "lore_de": "'Wir explodieren vor Wut!', rufen die Kirsch-Zwillinge im Chor. Niemand weiß genau, worüber sie sich eigentlich ärgern.",
        "unlocked_level": 3,
    },
    "repeater": {
        "id": "repeater",
        "name_de": "Doppelerbse",
        "cost": 200,
        "cooldown": 7.5,
        "hp": 300,
        "description_de": "Feuert zwei Erbsen in rascher Folge ab.",
        "lore_de": "Doppelerbse ist extrem motiviert. 'Ich schieße nicht einfach doppelt so viel', sagt er, 'ich liebe meinen Job einfach doppelt so sehr!'",
        "unlocked_level": 3,
    },
    "snow_pea": {
        "id": "snow_pea",
        "name_de": "Schneekanone",
        "cost": 175,
        "cooldown": 7.5,
        "hp": 300,
        "description_de": "Verschießt gefrorene Erbsen, die Zombies um 50% verlangsamen.",
        "lore_de": "Schneekanone behält stets einen kühlen Kopf. Manche halten ihn für arrogant, aber er ist einfach nur cool.",
        "unlocked_level": 4,
    },
    "chomper": {
        "id": "chomper",
        "name_de": "Schnapper",
        "cost": 150,
        "cooldown": 7.5,
        "hp": 400,
        "description_de": "Verschlingt einen Zombie auf einen Happs ganz. Braucht Zeit zum Kauen.",
        "lore_de": "Schnapper hat riesigen Appetit. Seine Freunde warnen ihn oft vor Sodbrennen, aber Gehirnfresser schmecken ihm einfach zu gut.",
        "unlocked_level": 4,
    },
    "potato_mine": {
        "id": "potato_mine",
        "name_de": "Kartoffelmine",
        "cost": 25,
        "cooldown": 25.0,
        "hp": 300,
        "description_de": "Braucht 14s zum Scharfschalten. Explodiert bei Kontakt sofort (SPUDOW!).",
        "lore_de": "Kartoffelmine mag zwar geduldig im Boden verharren, doch wenn sie hochgeht, fliegt die Zombie-Mütze!",
        "unlocked_level": 5,
    },
    "squash": {
        "id": "squash",
        "name_de": "Riesenkürbis",
        "cost": 50,
        "cooldown": 25.0,
        "hp": 300,
        "description_de": "Hüpft in die Luft und zerquetscht herannahende Zombies platt.",
        "lore_de": "'Ich sehe vielleicht grimmig aus', brummt Riesenkürbis, 'aber wartet erst mal ab, wie grimmig ich werde, wenn ich lande!'",
        "unlocked_level": 5,
    },
    "jalapeno": {
        "id": "jalapeno",
        "name_de": "Chili",
        "cost": 125,
        "cooldown": 30.0,
        "hp": 300,
        "description_de": "Entfacht eine gewaltige Feuerwand, die eine ganze Reihe vernichtet.",
        "lore_de": "Chili brennt darauf, das Spielfeld aufzuräumen. Ein einziger Biss in diese Schote lässt selbst die kältesten Zombies verglühen!",
        "unlocked_level": 5,
    },
    "puff_shroom": {
        "id": "puff_shroom",
        "name_de": "Pustepilz",
        "cost": 0,
        "cooldown": 7.5,
        "hp": 200,
        "description_de": "Kostenloser Nacht-Pilz. Schießt Sporen auf kurze Distanz.",
        "lore_de": "Pustepilz kostet absolut keine Sonnenenergie und ist stolz darauf. Er ist klein, aber oho!",
        "unlocked_level": 6,
    },
    "fume_shroom": {
        "id": "fume_shroom",
        "name_de": "Rauchpilz",
        "cost": 75,
        "cooldown": 7.5,
        "hp": 300,
        "description_de": "Verschießt durchdringenden Rauch, der Schilde (z.B. Fliegengitter) ignoriert.",
        "lore_de": "Seine violetten Sporenwolken durchdringen selbst Fliegengitter und Pylonen mühelos.",
        "unlocked_level": 6,
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
    "screendoor": {
        "id": "screendoor",
        "name_de": "Fliegengitter-Zombie",
        "hp": 1000,  # 800 door + 200 body
        "speed": 20.0,
        "bite_dps": 100.0,
        "description_de": "Trägt eine Fliegengittertür als Schutzschild gegen normale Erbsen.",
        "lore_de": "Hält Fliegen draußen – und Erbsen ebenso. Nur Rauchsporen und Explosives kümmern sich nicht darum.",
    },
    "football": {
        "id": "football",
        "name_de": "Football-Zombie",
        "hp": 1600,  # 1400 helmet + 200 body
        "speed": 44.0,  # very fast
        "bite_dps": 100.0,
        "description_de": "Harte Schale, schneller Sprint. Einer der zähesten Zombies.",
        "lore_de": "Er gibt auf dem Rasen immer 110 Prozent. Helm auf, Schulterpolster fest und ab durch die Mitte!",
    },
    "disco": {
        "id": "disco",
        "name_de": "Disco-Zombie",
        "hp": 450,
        "speed": 20.0,
        "bite_dps": 100.0,
        "description_de": "Tanzt über den Rasen und beschwört regelmäßig 4 Backup-Tänzer!",
        "lore_de": "Die 70er Jahre sind nie gestorben – und dieser Zombie auch nicht so ganz.",
    },
    "backup": {
        "id": "backup",
        "name_de": "Backup-Tänzer",
        "hp": 200,
        "speed": 20.0,
        "bite_dps": 100.0,
        "description_de": "Folgt den Choreografien des Disco-Zombies aufs Wort.",
        "lore_de": "Jahrelange Tanzschule zahlt sich endlich in der Zombie-Apokalypse aus.",
    },
    "gargantuar": {
        "id": "gargantuar",
        "name_de": "Gargantuar",
        "hp": 3000,
        "speed": 14.0,
        "bite_dps": 300.0,
        "description_de": "Gigantischer Riese. Zerschmettert Pflanzen mit einem Telegrafenmast!",
        "lore_de": "Wenn Gargantuar den Vorgarten betritt, bebt die Erde. Nichts hält ihn auf – außer jede Menge Feuerkraft!",
    },
}

# Levels Configuration (Balanced for smooth, fair, and engaging progression)
CAMPAIGN_LEVELS = [
    {
        "level_num": 1,
        "title_de": "Level 1-1: Die ersten Schritte",
        "bg": "lawn_day",
        "initial_sun": 250,  # Generous start
        "available_plants": ["peashooter"],
        "active_rows": [2],  # Only middle row for tutorial level
        "total_waves": 4,
        "zombie_types": ["normal"],
        "unlock_reward": "sunflower",
    },
    {
        "level_num": 2,
        "title_de": "Level 1-2: Sonnige Aussichten",
        "bg": "lawn_day",
        "initial_sun": 250,  # Ample starting sun to plant sunflowers immediately!
        "available_plants": ["peashooter", "sunflower"],
        "active_rows": [1, 2, 3],  # 3 rows
        "total_waves": 6,
        "zombie_types": ["normal", "conehead"],
        "unlock_reward": "wallnut",
    },
    {
        "level_num": 3,
        "title_de": "Level 1-3: Harte Nüsse",
        "bg": "lawn_day",
        "initial_sun": 250,
        "available_plants": ["peashooter", "sunflower", "wallnut"],
        "active_rows": [0, 1, 2, 3, 4],  # full 5 rows
        "total_waves": 8,
        "zombie_types": ["normal", "conehead", "polevaulter"],
        "unlock_reward": "cherry_bomb",
    },
    {
        "level_num": 4,
        "title_de": "Level 1-4: Explosive Überraschung",
        "bg": "lawn_day",
        "initial_sun": 250,
        "available_plants": ["peashooter", "sunflower", "wallnut", "cherry_bomb"],
        "active_rows": [0, 1, 2, 3, 4],
        "total_waves": 10,
        "zombie_types": ["normal", "conehead", "buckethead", "polevaulter"],
        "unlock_reward": "repeater",
    },
    {
        "level_num": 5,
        "title_de": "Level 1-5: Doppelte Feuerkraft",
        "bg": "lawn_day",
        "initial_sun": 250,
        "available_plants": ["peashooter", "sunflower", "wallnut", "cherry_bomb", "repeater"],
        "active_rows": [0, 1, 2, 3, 4],
        "total_waves": 12,
        "zombie_types": ["normal", "conehead", "buckethead", "flag", "polevaulter"],
        "unlock_reward": "snow_pea",
    },
    {
        "level_num": 6,
        "title_de": "Level 2-1: Nächtlicher Schrecken",
        "bg": "lawn_night",
        "initial_sun": 200,
        "available_plants": ["peashooter", "sunflower", "wallnut", "cherry_bomb", "repeater", "snow_pea", "puff_shroom"],
        "active_rows": [0, 1, 2, 3, 4],
        "total_waves": 14,
        "zombie_types": ["normal", "conehead", "newspaper", "screendoor"],
        "unlock_reward": "fume_shroom",
    },
    {
        "level_num": 7,
        "title_de": "Level 2-2: Tanz auf dem Rasen",
        "bg": "lawn_night",
        "initial_sun": 200,
        "available_plants": ["peashooter", "sunflower", "wallnut", "cherry_bomb", "repeater", "snow_pea", "puff_shroom", "fume_shroom"],
        "active_rows": [0, 1, 2, 3, 4],
        "total_waves": 16,
        "zombie_types": ["normal", "conehead", "buckethead", "disco", "football"],
        "unlock_reward": "chomper",
    },
    {
        "level_num": 8,
        "title_de": "Level 2-3: Die Kolosse erwachen",
        "bg": "lawn_night",
        "initial_sun": 250,
        "available_plants": ["peashooter", "sunflower", "wallnut", "cherry_bomb", "repeater", "snow_pea", "chomper", "potato_mine", "squash", "jalapeno"],
        "active_rows": [0, 1, 2, 3, 4],
        "total_waves": 18,
        "zombie_types": ["normal", "conehead", "buckethead", "football", "screendoor", "disco", "gargantuar"],
        "unlock_reward": None,
    },
]

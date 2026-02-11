"""Прототипы игровых уровней"""

# Игровые объекты
import scripts.game_objects.enemy as enemy

# Макет прототипа уровня:
# "<имя>": {
#   "tilemap": путь к карте
#   "background_soundtrack": саундтрек на фоне
#   "waves": набор волн
#   "wave_rate": длительность волны
#   "difficulty": модификатор сложности
#   "reward": награда за прохождение уровня
# }

LEVEL_PROTOTYPES = {
    "The first steps": {
        "tilemap": "resources/levels/level1.tmx",
        "background_soundtrack": "resources/assets/sounds/soundtracks/level_1.mp3",
        "waves": tuple([
            tuple(enemy.BasicEnemy for _ in range(5)),
            tuple(enemy.BasicEnemy for _ in range(6)),
            tuple(enemy.BasicEnemy for _ in range(8)),
            tuple(enemy.BasicEnemy for _ in range(10)),
            tuple(enemy.BasicEnemy for _ in range(15)),
            tuple(enemy.BasicEnemy for _ in range(20)),
            tuple(enemy.BasicEnemy for _ in range(25)),
            tuple(enemy.BasicEnemy for _ in range(30))
        ]),
        "wave_rate": 15.0,
        "difficulty": 1.0,
        "reward": {"level": "High-speed traffic", "tower": "explosive_tower"}
    },

    "High-speed traffic": {
        "tilemap": "resources/levels/level2.tmx",
        "background_soundtrack": "resources/assets/sounds/soundtracks/level_2.mp3",
        "waves": tuple([
            tuple(enemy.BasicEnemy for _ in range(5)),
            tuple(enemy.FastEnemy for _ in range(5)),
            tuple(enemy.BasicEnemy for _ in range(8)),
            tuple(enemy.FastEnemy for _ in range(8)),
            tuple([enemy.BasicEnemy for _ in range(10)] + [enemy.FastEnemy for _ in range(10)]),
            tuple([enemy.BasicEnemy for _ in range(15)] + [enemy.FastEnemy for _ in range(15)]),
            tuple(enemy.BasicEnemy for _ in range(25)),
            tuple(enemy.FastEnemy for _ in range(25)),
            tuple([enemy.BasicEnemy for _ in range(20)] + [enemy.FastEnemy for _ in range(20)]),
            tuple([enemy.BasicEnemy for _ in range(25)] + [enemy.FastEnemy for _ in range(25)]),
            tuple(enemy.BasicEnemy for _ in range(30)),
            tuple(enemy.FastEnemy for _ in range(30)),
            tuple(enemy.BasicEnemy for _ in range(40)),
            tuple(enemy.FastEnemy for _ in range(40)),
            tuple(enemy.BasicEnemy for _ in range(40)),
            tuple(enemy.FastEnemy for _ in range(40)),
            tuple([enemy.BasicEnemy for _ in range(40)] + [enemy.FastEnemy for _ in range(40)]),
        ]),
        "wave_rate": 20.0,
        "difficulty": 1.1,
        "reward": {"level": "The heavyweights", "tower": "sniper_tower"}
    },

    "The heavyweights": {
        "tilemap": "resources/levels/level3.tmx",
        "background_soundtrack": "resources/assets/sounds/soundtracks/level_3.mp3",
        "waves": ([
            tuple(enemy.BasicEnemy for _ in range(5)),
            tuple(enemy.BasicEnemy for _ in range(8)),
            tuple(enemy.FastEnemy for _ in range(8)),
            tuple(enemy.BigEnemy for _ in range(4)),
            tuple(enemy.BigEnemy for _ in range(6)),
            tuple(enemy.BigEnemy for _ in range(8)),
            tuple([enemy.BasicEnemy for _ in range(6)] + [enemy.FastEnemy for _ in range(6)]),
            tuple([enemy.BasicEnemy for _ in range(6)] + [enemy.BigEnemy for _ in range(6)]),
            tuple(enemy.BasicEnemy for _ in range(15)),
            tuple(enemy.BasicEnemy for _ in range(20)),
            tuple(enemy.FastEnemy for _ in range(20)),
            tuple(enemy.BigEnemy for _ in range(10)),
            tuple(enemy.BigEnemy for _ in range(15)),
            tuple(enemy.BigEnemy for _ in range(20)),
            tuple([enemy.BasicEnemy for _ in range(15)] + [enemy.FastEnemy for _ in range(15)]),
            tuple([enemy.BasicEnemy for _ in range(20)] + [enemy.BigEnemy for _ in range(10)]),
            tuple(enemy.BigEnemy for _ in range(15)),
            tuple([enemy.BasicEnemy for _ in range(20)] + [enemy.BigEnemy for _ in range(15)]),
            tuple([enemy.BasicEnemy for _ in range(20)] + [enemy.BigEnemy for _ in range(20)]),
            tuple([enemy.BasicEnemy for _ in range(20)] + [enemy.FastEnemy for _ in range(20)] +
                  [enemy.BigEnemy for _ in range(20)]),
            tuple([enemy.BasicEnemy for _ in range(30)] + [enemy.FastEnemy for _ in range(30)] +
                  [enemy.BigEnemy for _ in range(30)])
        ]),
        "wave_rate": 25.0,
        "difficulty": 1.2,
        "reward": {"level": "Breakthrough", "tower": "minigun_tower"}
    },

    "Breakthrough": {
        "tilemap": "resources/levels/level4.tmx",
        "background_soundtrack": "resources/assets/sounds/soundtracks/level_4.mp3",
        "waves": tuple([
            tuple(enemy.BasicEnemy for _ in range(6)),
            tuple(enemy.FastEnemy for _ in range(6)),
            tuple(enemy.BigEnemy for _ in range(4)),
            tuple(enemy.PushEnemy for _ in range(3)),
            tuple(enemy.BasicEnemy for _ in range(12)),
            tuple(enemy.FastEnemy for _ in range(12)),
            tuple([enemy.BasicEnemy for _ in range(8)] + [enemy.FastEnemy for _ in range(8)]),
            tuple([enemy.BasicEnemy for _ in range(10)] + [enemy.BigEnemy for _ in range(4)]),
            tuple(enemy.BigEnemy for _ in range(6)),
            tuple(enemy.PushEnemy for _ in range(6)),
            tuple(enemy.FastEnemy for _ in range(20)),
            tuple(enemy.BigEnemy for _ in range(10)),
            tuple(enemy.PushEnemy for _ in range(10)),
            tuple(enemy.BasicEnemy for _ in range(20)),
            tuple([enemy.PushEnemy for _ in range(8)] + [enemy.FastEnemy for _ in range(16)]),
            tuple([enemy.PushEnemy for _ in range(8)] + [enemy.BigEnemy for _ in range(8)]),
            tuple(enemy.BasicEnemy for _ in range(30)),
            tuple([enemy.BasicEnemy for _ in range(15)] + [enemy.PushEnemy for _ in range(10)]),
            tuple([enemy.PushEnemy for _ in range(10)] + [enemy.FastEnemy for _ in range(15)]),
            tuple([enemy.PushEnemy for _ in range(12)] + [enemy.FastEnemy for _ in range(12)] +
                  [enemy.PushEnemy for _ in range(20)]),
            tuple([enemy.BasicEnemy for _ in range(25)] + [enemy.BigEnemy for _ in range(20)] +
                  [enemy.PushEnemy for _ in range(30)])
        ]),
        "wave_rate": 30.0,
        "difficulty": 1.3,
        "reward": {"level": "The last frontier", "tower": None}
    },

    "The last frontier": {
        "tilemap": "resources/levels/level5.tmx",
        "background_soundtrack": "resources/assets/sounds/soundtracks/level_5.mp3",
        "waves": tuple([
            tuple(enemy.BasicEnemy for _ in range(6)),
            tuple(enemy.BasicEnemy for _ in range(8)),
            tuple(enemy.FastEnemy for _ in range(6)),
            tuple([enemy.BasicEnemy for _ in range(6)] + [enemy.FastEnemy for _ in range(6)]),
            tuple(enemy.FastEnemy for _ in range(12)),
            tuple(enemy.BigEnemy for _ in range(4)),
            tuple([enemy.BigEnemy for _ in range(4)] + [enemy.FastEnemy for _ in range(10)]),
            tuple([enemy.BigEnemy for _ in range(4)] + [enemy.BasicEnemy for _ in range(10)]),
            tuple(enemy.BigEnemy for _ in range(8)),
            tuple(enemy.PushEnemy for _ in range(4)),
            tuple(enemy.PushEnemy for _ in range(6)),
            tuple([enemy.BigEnemy for _ in range(6)] + [enemy.PushEnemy for _ in range(6)]),
            tuple([enemy.BigEnemy for _ in range(10)] + [enemy.PushEnemy for _ in range(6)]),
            tuple(enemy.FastEnemy for _ in range(20)),
            tuple(enemy.BasicEnemy for _ in range(30)),
            tuple([enemy.BasicEnemy for _ in range(20)] + [enemy.FastEnemy for _ in range(15)]),
            tuple(enemy.BigEnemy for _ in range(16)),
            tuple(enemy.PushEnemy for _ in range(8)),
            tuple(enemy.PushEnemy for _ in range(12)),
            tuple(enemy.PushEnemy for _ in range(16)),
            tuple([enemy.BossEnemy] + [enemy.PushEnemy for _ in range(8)])
        ]),
        "wave_rate": 35.0,
        "difficulty": 1.5,
        "reward": {"level": None, "tower": None}
    }
}

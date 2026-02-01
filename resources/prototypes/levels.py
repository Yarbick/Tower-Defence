import enemy

# Макет прототипа уровня:
# "<имя>": {
#   "tilemap": путь к карте
#   "waves": набор волн
#   "wave_rate": длительность волны
#   "difficulty": модификатор сложности
# }

LEVELS = {
    "The first steps": {
        "tilemap": "resources/levels/level1.tmx",
        "waves": (
            (enemy.BasicEnemy for _ in range(5)),
            (enemy.BasicEnemy for _ in range(6)),
            (enemy.BasicEnemy for _ in range(8)),
            (enemy.BasicEnemy for _ in range(10)),
            (enemy.BasicEnemy for _ in range(15)),
            (enemy.BasicEnemy for _ in range(20)),
            (enemy.BasicEnemy for _ in range(25)),
            (enemy.BasicEnemy for _ in range(30))
        ),
        "wave_rate": 15.0,
        "difficulty": 1.0
    },

    "High-speed traffic": {
        "tilemap": "resources/levels/level2.tmx",
        "waves": (
            (enemy.BasicEnemy for _ in range(5)),
            (enemy.FastEnemy for _ in range(5)),
            (enemy.BasicEnemy for _ in range(8)),
            (enemy.FastEnemy for _ in range(8)),
            ([enemy.BasicEnemy for _ in range(10)] + [enemy.FastEnemy for _ in range(10)]),
            ([enemy.BasicEnemy for _ in range(15)] + [enemy.FastEnemy for _ in range(15)]),
            (enemy.BasicEnemy for _ in range(25)),
            (enemy.FastEnemy for _ in range(25)),
            ([enemy.BasicEnemy for _ in range(20)] + [enemy.FastEnemy for _ in range(20)]),
            ([enemy.BasicEnemy for _ in range(25)] + [enemy.FastEnemy for _ in range(25)]),
            (enemy.BasicEnemy for _ in range(30)),
            (enemy.FastEnemy for _ in range(30)),
            (enemy.BasicEnemy for _ in range(40)),
            (enemy.FastEnemy for _ in range(40)),
            (enemy.BasicEnemy for _ in range(40)),
            (enemy.FastEnemy for _ in range(40)),
            ([enemy.BasicEnemy for _ in range(40)] + [enemy.FastEnemy for _ in range(40)]),
        ),
        "wave_rate": 20.0,
        "difficulty": 1.1
    },

    "The heavyweights": {
        "tilemap": "resources/levels/level3.tmx",
        "waves": (
            (enemy.BasicEnemy for _ in range(5)),
            (enemy.BasicEnemy for _ in range(8)),
            (enemy.FastEnemy for _ in range(8)),
            (enemy.BigEnemy for _ in range(4)),
            (enemy.BigEnemy for _ in range(6)),
            (enemy.BigEnemy for _ in range(8)),
            ([enemy.BasicEnemy for _ in range(6)] + [enemy.FastEnemy for _ in range(6)]),
            ([enemy.BasicEnemy for _ in range(6)] + [enemy.BigEnemy for _ in range(6)]),
            (enemy.BasicEnemy for _ in range(15)),
            (enemy.BasicEnemy for _ in range(20)),
            (enemy.FastEnemy for _ in range(20)),
            (enemy.BigEnemy for _ in range(10)),
            (enemy.BigEnemy for _ in range(15)),
            (enemy.BigEnemy for _ in range(20)),
            ([enemy.BasicEnemy for _ in range(15)] + [enemy.FastEnemy for _ in range(15)]),
            ([enemy.BasicEnemy for _ in range(20)] + [enemy.BigEnemy for _ in range(10)]),
            (enemy.BigEnemy for _ in range(15)),
            ([enemy.BasicEnemy for _ in range(20)] + [enemy.BigEnemy for _ in range(15)]),
            ([enemy.BasicEnemy for _ in range(20)] + [enemy.BigEnemy for _ in range(20)]),
            ([enemy.BasicEnemy for _ in range(20)] + [enemy.FastEnemy for _ in range(20)] +
             [enemy.BigEnemy for _ in range(20)]),
            ([enemy.BasicEnemy for _ in range(30)] + [enemy.FastEnemy for _ in range(30)] +
             [enemy.BigEnemy for _ in range(30)])
        ),
        "wave_rate": 25.0,
        "difficulty": 1.2
    },

    "Breakthrough": {
        "tilemap": "resources/levels/level4.tmx",
        "waves": (
            (enemy.BasicEnemy for _ in range(6)),
            (enemy.FastEnemy for _ in range(6)),
            (enemy.BigEnemy for _ in range(4)),
            (enemy.PushEnemy for _ in range(3)),
            (enemy.BasicEnemy for _ in range(12)),
            (enemy.FastEnemy for _ in range(12)),
            ([enemy.BasicEnemy for _ in range(8)] + [enemy.FastEnemy for _ in range(8)]),
            ([enemy.BasicEnemy for _ in range(10)] + [enemy.BigEnemy for _ in range(4)]),
            (enemy.BigEnemy for _ in range(6)),
            (enemy.PushEnemy for _ in range(6)),
            (enemy.FastEnemy for _ in range(20)),
            (enemy.BigEnemy for _ in range(10)),
            (enemy.PushEnemy for _ in range(10)),
            (enemy.BasicEnemy for _ in range(20)),
            ([enemy.PushEnemy for _ in range(8)] + [enemy.FastEnemy for _ in range(16)]),
            ([enemy.PushEnemy for _ in range(8)] + [enemy.BigEnemy for _ in range(8)]),
            (enemy.BasicEnemy for _ in range(30)),
            ([enemy.BasicEnemy for _ in range(15)] + [enemy.PushEnemy for _ in range(10)]),
            ([enemy.PushEnemy for _ in range(10)] + [enemy.FastEnemy for _ in range(15)]),
            ([enemy.PushEnemy for _ in range(12)] + [enemy.FastEnemy for _ in range(12)] +
             [enemy.PushEnemy for _ in range(20)]),
            ([enemy.BasicEnemy for _ in range(25)] + [enemy.BigEnemy for _ in range(20)] +
             [enemy.PushEnemy for _ in range(30)])
        ),
        "wave_rate": 30.0,
        "difficulty": 1.3
    },

    "The last frontier": {
        "tilemap": "resources/levels/level5.tmx",
        "waves": (
            (enemy.BasicEnemy for _ in range(6)),
            (enemy.BasicEnemy for _ in range(8)),
            (enemy.FastEnemy for _ in range(6)),
            ([enemy.BasicEnemy for _ in range(6)] + [enemy.FastEnemy for _ in range(6)]),
            (enemy.FastEnemy for _ in range(12)),
            (enemy.BigEnemy for _ in range(4)),
            ([enemy.BigEnemy for _ in range(4)] + [enemy.FastEnemy for _ in range(10)]),
            ([enemy.BigEnemy for _ in range(4)] + [enemy.BasicEnemy for _ in range(10)]),
            (enemy.BigEnemy for _ in range(8)),
            (enemy.PushEnemy for _ in range(4)),
            (enemy.PushEnemy for _ in range(6)),
            ([enemy.BigEnemy for _ in range(6)] + [enemy.PushEnemy for _ in range(6)]),
            ([enemy.BigEnemy for _ in range(10)] + [enemy.PushEnemy for _ in range(6)]),
            (enemy.FastEnemy for _ in range(20)),
            (enemy.BasicEnemy for _ in range(30)),
            ([enemy.BasicEnemy for _ in range(20)] + [enemy.FastEnemy for _ in range(15)]),
            (enemy.BigEnemy for _ in range(16)),
            (enemy.PushEnemy for _ in range(8)),
            (enemy.PushEnemy for _ in range(12)),
            (enemy.PushEnemy for _ in range(16)),
            ([enemy.BossEnemy] + [enemy.PushEnemy for _ in range(8)])
        ),
        "wave_rate": 35.0,
        "difficulty": 1.5
    }
}

# Макет прототипа башни:
# "<имя>": {
#   "base_texture": путь к текстуре с основанием
#   "base_max_texture": путь к текстуре с улучшенным основанием
#   "turret_texture": путь к текстуре турели
#   "bullet_texture": путь к текстуре пули
#   "damage": урон
#   "fire_rate": скорость пули
#   "radius": радиус атаки
#   "bullet_speed": скорость пули
#   "price": цена покупки
# }

TOWERS = {
    "basic_tower": {
        "base_texture": "resources/assets/images/towers/basic_tower/base.png",
        "base_max_texture": "resources/assets/images/towers/basic_tower/base_max.png",
        "turret_texture": "resources/assets/images/towers/basic_tower/turret.png",
        "bullet_texture": "resources/assets/images/towers/basic_tower/bullet.png",
        "shot_sound": "resources/assets/sounds/towers/basic_tower_shot.wav",
        "damage": 70,
        "fire_rate": 1 / 3,
        "radius": 5,
        "bullet_speed": 750,
        "price": 150
    },

    "explosive_tower": {
        "base_texture": "resources/assets/images/towers/explosive_tower/base.png",
        "base_max_texture": "resources/assets/images/towers/explosive_tower/base_max.png",
        "turret_texture": "resources/assets/images/towers/explosive_tower/turret.png",
        "bullet_texture": "resources/assets/images/towers/explosive_tower/bullet.png",
        "shot_sound": "resources/assets/sounds/towers/explosive_tower_shot.wav",
        "damage": 50,
        "fire_rate": 1 / 2,
        "radius": 4,
        "bullet_speed": 600,
        "price": 200
    },

    "sniper_tower": {
        "base_texture": "resources/assets/images/towers/sniper_tower/base.png",
        "base_max_texture": "resources/assets/images/towers/sniper_tower/base_max.png",
        "turret_texture": "resources/assets/images/towers/sniper_tower/turret.png",
        "bullet_texture": "resources/assets/images/towers/sniper_tower/bullet.png",
        "shot_sound": "resources/assets/sounds/towers/sniper_tower_shot.wav",
        "damage": 400,
        "fire_rate": 1 / 0.75,
        "radius": 12,
        "bullet_speed": 1500,
        "price": 250
    },

    "minigun_tower": {
        "base_texture": "resources/assets/images/towers/minigun_tower/base.png",
        "base_max_texture": "resources/assets/images/towers/minigun_tower/base_max.png",
        "turret_texture": "resources/assets/images/towers/minigun_tower/turret.png",
        "bullet_texture": "resources/assets/images/towers/minigun_tower/bullet.png",
        "shot_sound": "resources/assets/sounds/towers/minigun_tower_shot.wav",
        "damage": 40,
        "fire_rate": 1 / 10,
        "radius": 7,
        "bullet_speed": 1000,
        "price": 300
    }
}

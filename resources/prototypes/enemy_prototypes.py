"""Прототипы врагов"""

# Графика
from arcade import load_texture

# Макет прототипа врага:
# "<имя>": {
#   "idle_texture": путь к текстуре с стандартной позицией
#   "dead_animation_textures": список путей к текстурами с анимацией смерти
#   "health": здоровье
#   "armor": процентное поглощение урона
#   "speed": скорость
#   "damage": урон по базе игрока
#   "kill_reward": награда за убийство
# }

ENEMY_PROTOTYPES = {
    "basic_enemy": {
        "idle_texture": "resources/assets/images/enemies/basic_enemy/idle.png",
        "dead_animation_textures": tuple(
            f"resources/assets/images/enemies/basic_enemy/dead_animation/dead_{i}.png" for i in range(1, 6)
        ),
        "health": 100,
        "armor": 0.1,
        "speed": 200,
        "damage": 1,
        "kill_reward": 15
    },

    "fast_enemy": {
        "idle_texture": "resources/assets/images/enemies/fast_enemy/idle.png",
        "dead_animation_textures": tuple(
            f"resources/assets/images/enemies/fast_enemy/dead_animation/dead_{i}.png" for i in range(1, 6)
        ),
        "health": 75,
        "armor": 0.0,
        "speed": 350,
        "damage": 1,
        "kill_reward": 15
    },

    "big_enemy": {
        "idle_texture": "resources/assets/images/enemies/big_enemy/idle.png",
        "dead_animation_textures": tuple(
            f"resources/assets/images/enemies/big_enemy/dead_animation/dead_{i}.png" for i in range(1, 6)
        ),
        "health": 300,
        "armor": 0.4,
        "speed": 125,
        "damage": 2,
        "kill_reward": 25
    },

    "push_enemy": {
        "idle_texture": "resources/assets/images/enemies/push_enemy/idle.png",
        "dead_animation_textures": tuple(
            f"resources/assets/images/enemies/push_enemy/dead_animation/dead_{i}.png" for i in range(1, 6)
        ),
        "health": 225,
        "armor": 0.25,
        "speed": 275,
        "damage": 2,
        "kill_reward": 35
    },

    "boss_enemy": {
        "idle_texture": "resources/assets/images/enemies/boss_enemy/1_phase/idle.png",
        "idle_texture_1_phase": "resources/assets/images/enemies/boss_enemy/1_phase/idle.png",
        "idle_texture_2_phase": "resources/assets/images/enemies/boss_enemy/2_phase/idle.png",
        "rocket_texture": "resources/assets/images/enemies/boss_enemy/rocket.png",
        "attack_animation_textures_1_phase": tuple(
            f"resources/assets/images/enemies/boss_enemy/1_phase/attack_animation/attack_{i}.png" for i in range(1, 3)
        ),
        "attack_animation_textures_2_phase": tuple(
            f"resources/assets/images/enemies/boss_enemy/2_phase/attack_animation/attack_{i}.png" for i in range(1, 3)
        ),
        "dead_animation_textures": tuple(
            f"resources/assets/images/enemies/boss_enemy/2_phase/dead_animation/dead_{i}.png" for i in range(1, 8)
        ),
        "boss_soundtrack": "resources/assets/sounds/soundtracks/level_5_boss.mp3",
        "attack_sound": "resources/assets/sounds/enemies/boss/boss_attack.wav",
        "dead_sound": "resources/assets/sounds/enemies/boss/boss_dead.wav",
        "rocket_explosive": "resources/assets/sounds/enemies/boss/rocket_explosive.wav",
        "health": 75000,
        "armor": 0.35,
        "speed": 25,
        "damage": 100,
        "kill_reward": 1000,
        "spawn_attack_rate": 5.0,
        "spawn_rate": 0.25,
        "rocket_attack_rate": 8.0,
        "rockets_count": 4,
        "rocket_speed": 1000,
        "rocket_stun_duration": 5.0
    },
}

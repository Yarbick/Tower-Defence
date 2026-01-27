import arcade
from math import atan2

import bullet

# Константы
TOWER_SCALING = 2.0


class Tower(arcade.Sprite):
    """Башня"""

    def update(self, delta_time: float = 1 / 60) -> None:
        self.find_target()
        self.rotate_to_target()
        self.shoot(delta_time)

    def find_target(self) -> None:
        """Поиск цели"""

        # Проверка на наличие цели
        if self.curr_target:
            # Прекращаем поиск, если цель в радиусе атаки башни и не уничтожена
            if arcade.check_for_collision(self.attack_range, self.curr_target) and not self.curr_target.is_dead:
                return
            self.curr_target = None

        # Поиск новой цели
        targets = arcade.check_for_collision_with_list(self.attack_range, self.enemy_list)  # Цели в радиусе атаки башни
        if self.curr_target is None and targets:
            # Выбор самой первой цели
            self.curr_target = max(
                targets,
                key=lambda target: target.way_traveled
            )

    def rotate_to_target(self) -> None:
        """Поворот башни к цели"""

        if self.curr_target:
            self.angle = atan2(
                self.curr_target.center_y - self.center_y, self.curr_target.center_x - self.center_x
            ) * -60 + 90

    def shoot(self, delta_time: float) -> None:
        """Стрельба"""

        self.fire_timer += delta_time
        # Проверка на возможность выстрелить
        if self.curr_target and self.fire_timer >= self.fire_rate:
            # Создание пули
            self.bullets_list.append(self.bullet(
                self.center_x, self.center_y, self.angle, self.bullet_texture,
                self.bullet_speed, self.damage, self.curr_target
            ))

            # Сброс таймера
            self.fire_timer = 0.0


class BasicTower(Tower):
    def __init__(self, center_x: int | float, center_y: int | float,
                 enemies_list: arcade.SpriteList, bullets_list: arcade.SpriteList):
        super().__init__(center_x=center_x, center_y=center_y, scale=TOWER_SCALING)

        # Загрузка текстур
        self.base_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/basic_tower/base.png"
        )
        self.base_max_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/basic_tower/base_max.png"
        )
        self.turret_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/basic_tower/turret.png"
        )
        self.bullet_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/basic_tower/bullet.png"
        )
        self.attack_range_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/attack_range.png"
        )
        self.texture = self.turret_texture

        # Показатели башни
        self.damage: int | float = 80
        self.fire_rate: int | float = 1 / 2
        self.radius: int | float = 5
        self.bullet_speed: int | float = 750

        # Текущий уровень улучшения
        self.upgrade_level: int = 1
        # Время с последнего выстрела
        self.fire_timer: float = 0.0

        # Основание башни
        self.base: arcade.Sprite = arcade.Sprite(self.base_texture, scale=TOWER_SCALING)
        self.base.position = self.center_x, self.center_y

        # Радиус атаки
        self.attack_range: arcade.Sprite = arcade.Sprite(self.attack_range_texture, scale=self.radius * TOWER_SCALING)
        self.attack_range.position = center_x, center_y

        # Пуля
        self.bullet = bullet.Bullet

        # Ссылка на списки
        self.enemy_list: arcade.SpriteList = enemies_list
        self.bullets_list: arcade.SpriteList = bullets_list

        # Текущая цель
        self.curr_target: arcade.Sprite | None = None


class ExplosiveTower(Tower):
    def __init__(self, center_x: int | float, center_y: int | float,
                 enemies_list: arcade.SpriteList, bullets_list: arcade.SpriteList):
        super().__init__(center_x=center_x, center_y=center_y, scale=TOWER_SCALING)

        # Загрузка текстур
        self.base_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/explosive_tower/base.png"
        )
        self.base_max_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/explosive_tower/base_max.png"
        )
        self.turret_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/explosive_tower/turret.png"
        )
        self.bullet_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/explosive_tower/bullet.png"
        )
        self.attack_range_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/attack_range.png"
        )
        self.texture = self.turret_texture

        # Показатели башни
        self.damage: int | float = 50
        self.fire_rate: int | float = 1 / 2
        self.radius: int | float = 4
        self.bullet_speed: int | float = 600

        # Текущий уровень улучшения
        self.upgrade_level: int = 1
        # Время с последнего выстрела
        self.fire_timer: float = 0.0

        # Основание башни
        self.base: arcade.Sprite = arcade.Sprite(self.base_texture, scale=TOWER_SCALING)
        self.base.position = self.center_x, self.center_y

        # Радиус атаки
        self.attack_range: arcade.Sprite = arcade.Sprite(self.attack_range_texture, scale=self.radius * TOWER_SCALING)
        self.attack_range.position = center_x, center_y

        # Пуля
        self.bullet = bullet.ExplosiveBullet

        # Ссылка на списки
        self.enemy_list: arcade.SpriteList = enemies_list
        self.bullets_list: arcade.SpriteList = bullets_list

        # Текущая цель
        self.curr_target: arcade.Sprite | None = None


class SniperTower(Tower):
    def __init__(self, center_x: int | float, center_y: int | float,
                 enemies_list: arcade.SpriteList, bullets_list: arcade.SpriteList):
        super().__init__(center_x=center_x, center_y=center_y, scale=TOWER_SCALING)

        # Загрузка текстур
        self.base_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/sniper_tower/base.png"
        )
        self.base_max_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/sniper_tower/base_max.png"
        )
        self.turret_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/sniper_tower/turret.png"
        )
        self.bullet_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/sniper_tower/bullet.png"
        )
        self.attack_range_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/attack_range.png"
        )
        self.texture = self.turret_texture

        # Показатели башни
        self.damage: int | float = 300
        self.fire_rate: int | float = 1 / 0.5
        self.radius: int | float = 12
        self.bullet_speed: int | float = 1500

        # Текущий уровень улучшения
        self.upgrade_level: int = 1
        # Время с последнего выстрела
        self.fire_timer: float = 0.0

        # Основание башни
        self.base: arcade.Sprite = arcade.Sprite(self.base_texture, scale=TOWER_SCALING)
        self.base.position = self.center_x, self.center_y

        # Радиус атаки
        self.attack_range: arcade.Sprite = arcade.Sprite(self.attack_range_texture, scale=self.radius * TOWER_SCALING)
        self.attack_range.position = center_x, center_y

        # Пуля
        self.bullet = bullet.Bullet

        # Ссылка на списки
        self.enemy_list: arcade.SpriteList = enemies_list
        self.bullets_list: arcade.SpriteList = bullets_list

        # Текущая цель
        self.curr_target: arcade.Sprite | None = None


class MinigunTower(Tower):
    def __init__(self, center_x: int | float, center_y: int | float,
                 enemies_list: arcade.SpriteList, bullets_list: arcade.SpriteList):
        super().__init__(center_x=center_x, center_y=center_y, scale=TOWER_SCALING)

        # Загрузка текстур
        self.base_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/minigun_tower/base.png"
        )
        self.base_max_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/minigun_tower/base_max.png"
        )
        self.turret_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/minigun_tower/turret.png"
        )
        self.bullet_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/minigun_tower/bullet.png"
        )
        self.attack_range_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/attack_range.png"
        )
        self.texture = self.turret_texture

        # Показатели башни
        self.damage: int | float = 25
        self.fire_rate: int | float = 1 / 15
        self.radius: int | float = 8
        self.bullet_speed: int | float = 1000

        # Текущий уровень улучшения
        self.upgrade_level: int = 1
        # Время с последнего выстрела
        self.fire_timer: float = 0.0

        # Основание башни
        self.base: arcade.Sprite = arcade.Sprite(self.base_texture, scale=TOWER_SCALING)
        self.base.position = self.center_x, self.center_y

        # Радиус атаки
        self.attack_range: arcade.Sprite = arcade.Sprite(self.attack_range_texture, scale=self.radius * TOWER_SCALING)
        self.attack_range.position = center_x, center_y

        # Пуля
        self.bullet = bullet.Bullet

        # Ссылка на списки
        self.enemy_list: arcade.SpriteList = enemies_list
        self.bullets_list: arcade.SpriteList = bullets_list

        # Текущая цель
        self.curr_target: arcade.Sprite | None = None

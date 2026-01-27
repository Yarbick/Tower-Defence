import arcade
from math import atan2

TOWER_SCALING = 2.0


class Tower(arcade.Sprite):
    def update(self, delta_time: float = 1 / 60) -> None:
        self.find_target()
        self.rotate_to_target()

    def find_target(self) -> None:
        """Поиск цели"""

        # Проверка на наличие цели
        if self.curr_target is not None:
            # Прекращаем поиск, если цель в радиусе атаки башни
            if arcade.check_for_collision(self.attack_range, self.curr_target):
                return
            self.curr_target = None

        # Поиск новой цели
        targets = arcade.check_for_collision_with_list(self.attack_range, self.enemies)  # Цели в радиусе атаки башни
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


class BasicTower(Tower):
    def __init__(self, center_x: int | float, center_y: int | float, enemies: arcade.SpriteList):
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
        self.damage: int | float = 50
        self.fire_rate: int | float = 1 / 2
        self.radius: int | float = 5
        self.bullet_speed: int | float = 500

        # Текущий уровень улучшения
        self.upgrade_level: int = 1

        # Основание башни
        self.base: arcade.Sprite = arcade.Sprite(self.base_texture, scale=TOWER_SCALING)
        self.base.position = self.center_x, self.center_y

        # Радиус атаки
        self.attack_range: arcade.Sprite = arcade.Sprite(self.attack_range_texture, scale=self.radius * TOWER_SCALING)
        self.attack_range.position = center_x, center_y

        # Ссылка на список противников
        self.enemies: arcade.SpriteList = enemies
        # Текущая цель
        self.curr_target: arcade.Sprite | None = None

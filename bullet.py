import arcade
from math import atan2, sin, cos

import enemy

# Константы
BULLET_SCALE = 2.0

class Bullet(arcade.Sprite):
    """Стандартная пуля"""

    def __init__(self, center_x: float | int, center_y: float | int, angle: float | int, texture: arcade.Texture,
                 speed: int, damage: int, target: enemy.Enemy):
        super().__init__(center_x=center_x, center_y=center_y, angle=angle, path_or_texture=texture, scale=BULLET_SCALE)

        # Показатели пули
        self.speed: int = speed
        self.damage: int = damage

        # Цель
        self.target: enemy.Enemy = target

    def update(self, delta_time: float = 1 / 60) -> None:
        self.move(delta_time)
        self.hit()
        # Удаление пули, если цель уничтожена
        if self.target.is_dead:
            self.remove_from_sprite_lists()

    def move(self, delta_time: float) -> None:
        """Движение"""

        # Расчёт угла
        angle = atan2(self.target.center_y - self.center_y, self.target.center_x - self.center_x)
        # Движение
        self.center_x += cos(angle) * self.speed * delta_time
        self.center_y += sin(angle) * self.speed * delta_time
        # Поворот к врагу
        self.angle = angle * -60 + 90

    def hit(self):
        """Нанесение урона врагу"""

        # Проверка на попадание
        if arcade.check_for_collision(self, self.target):
            # Нанесение урона
            self.target.get_damage(self.damage)
            # Удаление пули
            self.remove_from_sprite_lists()


class ExplosiveBullet(Bullet):
    """Разрывная пуля"""

    def __init__(self, center_x: float | int, center_y: float | int, angle: float | int, texture: arcade.Texture,
                 speed: int, damage: int, target: enemy.Enemy):
        super().__init__(center_x, center_y, angle, texture, speed, damage, target)

        # Область взрыва
        self.explosive_radius: int = 3
        self.explosive_range: arcade.Sprite = arcade.Sprite(
            "resources/assets/images/towers/attack_range.png",
            scale=self.explosive_radius * BULLET_SCALE
        )

    def hit(self):
        """Нанесение урона врагу"""

        # Проверка на попадание
        if arcade.check_for_collision(self, self.target):
            # Перенос области взрыва
            self.explosive_range.position = self.position

            # Нанесение урона врагам, которые попали в область взрыва
            targets = arcade.check_for_collision_with_list(self.explosive_range, self.target.sprite_lists[0])
            for target in targets:
                target.get_damage(self.damage)

            # Удаление пули
            self.remove_from_sprite_lists()

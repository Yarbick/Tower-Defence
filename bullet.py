# Графика
import arcade
from arcade.particles import Emitter, EmitBurst, FadeParticle
# Рандом
from random import choice, uniform
# Математические расчёты
from math import atan2, sin, cos
# Игровые объекты
import enemy

# Константы
BULLET_SCALE: float = 2.0


class Bullet(arcade.Sprite):
    """Стандартная пуля"""

    def __init__(self, center_x: float | int, center_y: float | int, angle: float | int, texture: arcade.Texture,
                 speed: int, damage: int, target: enemy.Enemy, view: arcade.View):
        super().__init__(center_x=center_x, center_y=center_y, angle=angle, path_or_texture=texture, scale=BULLET_SCALE)

        # Привязка к уровню
        self.view: arcade.View = view

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
            self.delete()

    def delete(self) -> None:
        """Удаление"""

        # Удаление пули
        self.remove_from_sprite_lists()


class ExplosiveBullet(Bullet):
    """Разрывная пуля"""

    def __init__(self, center_x: float | int, center_y: float | int, angle: float | int, texture: arcade.Texture,
                 speed: int, damage: int, target: enemy.Enemy, view: arcade.View):
        super().__init__(center_x, center_y, angle, texture, speed, damage, target, view)

        # Область взрыва
        self.explosive_radius: int = 3
        self.explosive_range: arcade.Sprite = arcade.Sprite(
            "resources/assets/images/towers/attack_range.png",
            scale=self.explosive_radius * BULLET_SCALE
        )

        # Частицы
        self.EXPLOSIVE_SPARK: arcade.Texture = arcade.make_soft_circle_texture(16, arcade.color.REDWOOD)
        self.EXPLOSIVE_SMOKE: arcade.Texture = arcade.make_soft_circle_texture(24, arcade.color.REDWOOD, 255, 80)

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
            self.delete()

    def delete(self) -> None:
        """Удаление"""

        super().delete()

        # Создание частиц
        self.view.emitters.append(self.make_explosion())
        self.view.emitters.append(self.make_smoke_puff())

    # Частицы
    def gravity_drag(self, particle: FadeParticle) -> None:
        """Изменение скорости частицы"""

        particle.change_y += -0.025
        particle.change_x *= 0.9
        particle.change_y *= 0.9

    def smoke_mutator(self, particle: FadeParticle) -> None:
        """Раздувание дыма"""

        particle.scale_x *= 1.02
        particle.scale_y *= 1.02
        particle.alpha = max(0, particle.alpha - 2)

    def make_explosion(self) -> Emitter:
        """Эффект взрыва для взрывной пули"""

        emitter: Emitter = Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=EmitBurst(20),
            particle_factory=lambda e: FadeParticle(
                filename_or_texture=self.EXPLOSIVE_SPARK,
                change_xy=arcade.math.rand_in_circle((0.0, 0.0), 7.0),
                lifetime=uniform(0.2, 0.4),
                start_alpha=200, end_alpha=0,
                scale=uniform(0.5, 1.0),
                mutation_callback=self.gravity_drag,
            )
        )

        return emitter

    def make_smoke_puff(self):
        """Эффект дыма для взрывной пули"""

        emitter: Emitter = Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=EmitBurst(4),
            particle_factory=lambda e: FadeParticle(
                filename_or_texture=self.EXPLOSIVE_SMOKE,
                change_xy=arcade.math.rand_in_circle((0.0, 0.0), 1.5),
                lifetime=uniform(0.3, 0.5),
                start_alpha=255, end_alpha=0,
                scale=uniform(1.5, 2.0),
                mutation_callback=self.smoke_mutator,
            ),
        )

        return emitter

# Графика
import arcade
# Математические расчёты
from math import atan2
# Игровые объекты
import bullet
# Прототипы
from resources.prototypes.towers import TOWERS

# Константы
TOWER_SCALING = 2.0


class Tower(arcade.Sprite):
    """Макет башни"""

    def __init__(self, tower_name: str, center_x: int | float, center_y: int | float, view: arcade.View):
        super().__init__(center_x=center_x, center_y=center_y, scale=TOWER_SCALING)

        # Привязка к уровню
        self.view: arcade.View = view

        # Загрузка текстур
        self.base_texture: arcade.Texture = arcade.load_texture(TOWERS[tower_name]["base_texture"])
        self.base_max_texture: arcade.Texture = arcade.load_texture(TOWERS[tower_name]["base_max_texture"])
        self.turret_texture: arcade.Texture = arcade.load_texture(TOWERS[tower_name]["turret_texture"])
        self.bullet_texture: arcade.Texture = arcade.load_texture(TOWERS[tower_name]["bullet_texture"])
        self.attack_range_texture: arcade.Texture = arcade.load_texture(
            "resources/assets/images/towers/attack_range.png"
        )
        self.texture = self.turret_texture

        # Загрузка звуков
        self.shot_sound: arcade.Sound = arcade.load_sound(TOWERS[tower_name]["shot_sound"])
        self.money_sound: arcade.Sound = arcade.load_sound("resources/assets/sounds/money.wav")

        # Показатели башни
        self.damage: int | float = TOWERS[tower_name]["damage"]
        self.fire_rate: int | float = TOWERS[tower_name]["fire_rate"]
        self.radius: int | float = TOWERS[tower_name]["radius"]
        self.bullet_speed: int | float = TOWERS[tower_name]["bullet_speed"]
        self.price: int = TOWERS[tower_name]["price"]
        self.upgrade_price: int = self.price * 0.5
        self.delete_price: int = self.price * 0.75

        # Текущий уровень улучшения
        self.upgrade_level: int = 1
        # Время с последнего выстрела
        self.fire_timer: float = 0.0

        # Время оглушения
        self.stunned_time: float = 0.0

        # Основание башни
        self.base: arcade.Sprite = arcade.Sprite(self.base_texture, scale=TOWER_SCALING)
        self.base.position = self.center_x, self.center_y

        # Радиус атаки
        self.attack_range: arcade.Sprite = arcade.Sprite(self.attack_range_texture, scale=self.radius * TOWER_SCALING)
        self.attack_range.position = center_x, center_y

        # Пуля
        self.bullet = bullet.Bullet

        # Текущая цель
        self.curr_target: arcade.Sprite | None = None

    def update(self, delta_time: float = 1 / 60) -> None:
        # Проверка на оглушение
        if self.stunned_time > 0:
            self.stunned_time = max(0.0, self.stunned_time - delta_time)
            return

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
        targets = arcade.check_for_collision_with_list(self.attack_range,
                                                       self.view.enemies_list)  # Цели в радиусе атаки башни
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
            # Воспроизведение звука
            self.shot_sound.play()

            # Создание пули
            self.view.bullets_list.append(self.bullet(
                self.center_x, self.center_y, self.angle, self.bullet_texture,
                self.bullet_speed, self.damage, self.curr_target
            ))

            # Сброс таймера
            self.fire_timer = 0.0

    def upgrade(self) -> None:
        """Улучшение башни"""

        # Проверка на лимит уровней
        if self.upgrade_level < 5:
            # Воспроизведение звука
            self.money_sound.play()

            # Улучшение показателей
            self.damage *= 1.2
            self.fire_rate *= 0.9
            self.bullet_speed *= 1.2
            self.radius *= 1.1
            self.attack_range.scale = self.radius * TOWER_SCALING

            # Повышение цены удаления
            self.delete_price += self.upgrade_price * 0.75
            # Повышение целы улучшения
            self.upgrade_price *= 1.4

            # Прибавление уровня
            self.upgrade_level += 1

            # Смена текстуры основания на максимальном уровне
            if self.upgrade_level == 5:
                self.base.texture = self.base_max_texture

    def delete(self) -> None:
        """Удаление башни"""

        # Воспроизведение звука
        self.money_sound.play()

        # Прибавление денег игроку
        self.view.player_money += self.delete_price
        # Удаление башни
        self.base.remove_from_sprite_lists()
        self.remove_from_sprite_lists()


class BasicTower(Tower):
    """Базовая башня"""

    prototype_name: str = "basic_tower"

    def __init__(self, *args, **kwargs):
        super().__init__(self.prototype_name, *args, **kwargs)


class ExplosiveTower(Tower):
    """Взрывная башня"""

    prototype_name: str = "explosive_tower"

    def __init__(self, *args, **kwargs):
        super().__init__(self.prototype_name, *args, **kwargs)

        # Пуля
        self.bullet = bullet.ExplosiveBullet


class SniperTower(Tower):
    """Снайперская башня"""

    prototype_name: str = "sniper_tower"

    def __init__(self, *args, **kwargs):
        super().__init__(self.prototype_name, *args, **kwargs)


class MinigunTower(Tower):
    """Миниган башня"""

    prototype_name: str = "minigun_tower"

    def __init__(self, *args, **kwargs):
        super().__init__(self.prototype_name, *args, **kwargs)

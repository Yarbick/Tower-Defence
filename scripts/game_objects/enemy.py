"""Игровой объект врага"""

# Графика
import arcade
from arcade.particles import Emitter, EmitBurst, FadeParticle
# Рандом
from random import choices, choice, sample, uniform
# Звуки
import player_data.settings.sounds.sounds_volume as sounds_volume
# Игровые объекты
import scripts.game_objects.tower as tower
# Прототипы
from resources.prototypes.enemy_prototypes import ENEMY_PROTOTYPES

# Константы
ENEMY_SCALING: float = 3.0


class Enemy(arcade.Sprite):
    """Макет врага"""

    def __init__(self, enemy_name: str, center_x: int | float, center_y: int | float, way: tuple, difficulty: float,
                 view: arcade.View):
        super().__init__(center_x=center_x, center_y=center_y, scale=ENEMY_SCALING)

        # Привязка к уровню
        self.view: arcade.View = view

        # Загрузка текстур
        self.idle_texture: arcade.Texture = arcade.load_texture(ENEMY_PROTOTYPES[enemy_name]["idle_texture"])
        self.dead_animation_textures: tuple[arcade.Texture] = tuple(
            arcade.load_texture(ENEMY_PROTOTYPES[enemy_name]["dead_animation_textures"][i])
            for i in range(len(ENEMY_PROTOTYPES[enemy_name]["dead_animation_textures"]))
        )
        self.texture = self.idle_texture

        # Загрузка звуков
        self.hit: arcade.Sound = arcade.load_sound("resources/assets/sounds/hit.wav")

        # Показатели врага
        self.health: int = ENEMY_PROTOTYPES[enemy_name]["health"] * difficulty
        self.armor: float = ENEMY_PROTOTYPES[enemy_name]["armor"]
        self.speed: int = ENEMY_PROTOTYPES[enemy_name]["speed"]
        self.damage: int = ENEMY_PROTOTYPES[enemy_name]["damage"]
        self.kill_reward: int = ENEMY_PROTOTYPES[enemy_name]["kill_reward"]

        # Направление движения
        self.direction_x: int = 0
        self.direction_y: int = 0

        # Путь к базе игрока
        self.way: tuple = way
        self.curr_part: int = 0
        # Пройденное расстояние
        self.way_traveled: float = 0.0

        # Флаги
        self.is_dead = False

        # Анимация смерти
        self.dead_animation_running: bool = False
        self.dead_animation_frame: int = 0
        self.dead_animation_duration: float = 0.0
        self.dead_animation_speed: float = 1 / 30

    def update(self, delta_time: float = 1 / 60) -> None:
        # Проверка на смерть
        if self.is_dead:
            return

        # Движение
        self.move(delta_time)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        # Анимация смерти
        if self.dead_animation_running:
            self.dead_animation_duration += delta_time
            if self.dead_animation_duration >= self.dead_animation_speed:
                self.dead_animation_duration = 0.0

                self.dead_animation_frame += 1
                if self.dead_animation_frame >= len(self.dead_animation_textures):
                    self.dead_animation_running = False
                    # Удаление врага после завершения анимации
                    self.remove_from_sprite_lists()
                else:
                    self.texture = self.dead_animation_textures[self.dead_animation_frame]
        else:
            # Обновление анимации
            self.dead_animation_duration = 0.0
            self.dead_animation_frame = 0
            self.texture = self.idle_texture

    def move(self, delta_time: float) -> None:
        """Движение"""

        # Проверка на прохождение отрезка пути
        if (((self.way[self.curr_part][0] <= self.center_x and self.direction_x != -1) or
             (self.way[self.curr_part][0] >= self.center_x and self.direction_x != 1)) and
                ((self.way[self.curr_part][1] <= self.center_y and self.direction_y != -1) or
                 (self.way[self.curr_part][1] >= self.center_y and self.direction_y != 1))):
            old_part = self.curr_part

            # Переход на другой отрезок
            self.curr_part += 1
            # Смерть при завершении пути
            if self.curr_part >= len(self.way):
                # Воспроизведение звука
                self.hit.play(sounds_volume.others)

                # Нанесение урона базе
                self.view.player_health -= self.damage
                # Вычитание стоимости врага от денег игрока
                self.view.player_money -= self.kill_reward

                # Смерть
                self.dead()
                return

            # Определение нового направления
            if self.way[old_part][0] == self.way[self.curr_part][0]:
                self.direction_x = 0
            elif self.way[old_part][0] < self.way[self.curr_part][0]:
                self.direction_x = 1
            elif self.way[old_part][0] > self.way[self.curr_part][0]:
                self.direction_x = -1
            if self.way[old_part][1] == self.way[self.curr_part][1]:
                self.direction_y = 0
            elif self.way[old_part][1] < self.way[self.curr_part][1]:
                self.direction_y = 1
            elif self.way[old_part][1] > self.way[self.curr_part][1]:
                self.direction_y = -1

            # Определение угла
            if self.direction_x == 1:
                self.angle = 90
            elif self.direction_x == -1:
                self.angle = 270
            elif self.direction_y == 1:
                self.angle = 0
            elif self.direction_y == -1:
                self.angle = 180

        # Обновление позиции
        change_x, change_y = self.speed * self.direction_x * delta_time, self.speed * self.direction_y * delta_time
        self.center_x += change_x
        self.center_y += change_y
        self.way_traveled += abs(change_x) + abs(change_y)

    def get_damage(self, damage: int | float) -> None:
        """Получение урона"""

        # Определение и получение урона
        self.health -= damage * (1 - self.armor)
        # Проверка на смерть
        if self.health <= 0:
            self.dead()

    def dead(self) -> None:
        """Смерть"""

        # Переключение флага
        self.is_dead = True

        # Начисление денег игроку
        self.view.player_money += self.kill_reward

        # Запуск анимации
        self.dead_animation_running = True


class BasicEnemy(Enemy):
    """Базовый враг"""

    prototype_name: str = "basic_enemy"

    def __init__(self, *args, **kwargs):
        super().__init__(self.prototype_name, *args, **kwargs)


class FastEnemy(Enemy):
    """Быстрый враг"""

    prototype_name: str = "fast_enemy"

    def __init__(self, *args, **kwargs):
        super().__init__(self.prototype_name, *args, **kwargs)


class BigEnemy(Enemy):
    """Большой враг"""

    prototype_name: str = "big_enemy"

    def __init__(self, *args, **kwargs):
        super().__init__(self.prototype_name, *args, **kwargs)


class PushEnemy(Enemy):
    """Враг-пушер"""

    prototype_name: str = "push_enemy"

    def __init__(self, *args, **kwargs):
        super().__init__(self.prototype_name, *args, **kwargs)


class BossEnemy(Enemy):
    """Босс"""

    prototype_name: str = "boss_enemy"

    class Rocket(arcade.Sprite):
        """Ракета"""

        def __init__(self, speed, stun_duration, parent, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Создание атрибутов из аргументов
            self.speed = speed
            self.stun_duration: float = stun_duration
            self.parent: BossEnemy = parent

            # Частицы при взрыве ракеты
            self.EXPLOSIVE_SPARK: arcade.Texture = arcade.make_soft_circle_texture(16, arcade.color.PURPLE_NAVY)
            self.EXPLOSIVE_SMOKE: arcade.Texture = arcade.make_soft_circle_texture(24, arcade.color.PURPLE_NAVY, 255,
                                                                                   80)

            # Звуки
            self.rocket_explosive: arcade.Sound = arcade.load_sound(
                ENEMY_PROTOTYPES[self.parent.prototype_name]["rocket_explosive"]
            )

            # Физический движок для движения
            self.physics_engine = arcade.PhysicsEngineSimple(self)

        def update(self, delta_time: float = 1 / 60) -> None:
            # Обновление позиции
            self.change_y = self.speed * delta_time
            self.physics_engine.update()

            # Оглушение башни
            self.hit()

        def hit(self) -> None:
            """Оглушение башни"""

            # Проверка на попадание по башне
            targets: list = arcade.check_for_collision_with_list(self, self.parent.view.towers_turrets_list)
            for target in targets:
                # Оглушение башни
                target.stunned_time += self.stun_duration

                # Взрыв ракеты
                self.explosive()

        def explosive(self):
            """Взрыв"""

            # Удаление ракеты
            self.delete()

            # Тряска камеры
            self.parent.view.camera_shake.start()

            # Воспроизведение звуков
            self.rocket_explosive.play(volume=sounds_volume.enemies)

            # Создание частиц
            self.parent.view.emitters.append(self.make_explosion())
            self.parent.view.emitters.append(self.make_smoke_puff())

        def delete(self) -> None:
            """Удаление"""

            # Удаление ракеты
            self.remove_from_sprite_lists()

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
            """Эффект взрыва для ракеты"""

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
            """Эффект дыма для ракеты"""

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

    def __init__(self, *args, **kwargs):
        super().__init__(self.prototype_name, *args, **kwargs)

        # Загрузка текстур
        self.idle_texture_1_phase: arcade.Texture = arcade.load_texture(
            ENEMY_PROTOTYPES[self.prototype_name]["idle_texture_1_phase"]
        )
        self.idle_texture_2_phase: arcade.Texture = arcade.load_texture(
            ENEMY_PROTOTYPES[self.prototype_name]["idle_texture_2_phase"]
        )
        self.attack_animation_textures_1_phase: tuple[arcade.Texture] = tuple(
            arcade.load_texture(ENEMY_PROTOTYPES[self.prototype_name]["attack_animation_textures_1_phase"][i])
            for i in range(len(ENEMY_PROTOTYPES[self.prototype_name]["attack_animation_textures_1_phase"]))
        )
        self.attack_animation_textures_2_phase: tuple[arcade.Texture] = tuple(
            arcade.load_texture(ENEMY_PROTOTYPES[self.prototype_name]["attack_animation_textures_2_phase"][i])
            for i in range(len(ENEMY_PROTOTYPES[self.prototype_name]["attack_animation_textures_2_phase"]))
        )
        self.rocket_texture: arcade.Texture = arcade.load_texture(
            ENEMY_PROTOTYPES[self.prototype_name]["rocket_texture"])
        self.idle_texture = self.idle_texture_1_phase

        # Загрузка звуков
        self.boss_soundtrack: arcade.Sound = arcade.load_sound(ENEMY_PROTOTYPES[self.prototype_name]["boss_soundtrack"])
        self.attack_sound: arcade.Sound = arcade.load_sound(ENEMY_PROTOTYPES[self.prototype_name]["attack_sound"])
        self.dead_sound: arcade.Sound = arcade.load_sound(ENEMY_PROTOTYPES[self.prototype_name]["dead_sound"])

        # Показатели призывной атаки
        self.spawn_attack_rate: int | float = ENEMY_PROTOTYPES[self.prototype_name]["spawn_attack_rate"]
        self.spawn_queue: list[Enemy] = []
        self.spawn_rate: int | float = ENEMY_PROTOTYPES[self.prototype_name]["spawn_rate"]
        self.spawn_timer: float = 0.0
        # Показатели ракетной атаки
        self.rocket_attack_rate: float = ENEMY_PROTOTYPES[self.prototype_name]["rocket_attack_rate"]
        self.rockets_count: int = ENEMY_PROTOTYPES[self.prototype_name]["rockets_count"]
        self.rocket_speed: int | float = ENEMY_PROTOTYPES[self.prototype_name]["rocket_speed"]
        self.rocket_stun_duration: int | float = ENEMY_PROTOTYPES[self.prototype_name]["rocket_stun_duration"]
        # Порог здоровья для перехода на вторую фазу
        self.health_for_2_phase: int | float = self.health // 2

        # Флаги
        self.is_2_phase: bool = False

        # Анимация смерти
        self.dead_animation_speed: float = 1 / 10
        # Анимация атаки
        self.attack_animation_textures = self.attack_animation_textures_1_phase
        self.attack_animation_running: bool = False
        self.attack_animation_frame: int = 0
        self.attack_animation_duration: float = 0.0
        self.attack_animation_speed: float = 1 / 10

        # Атаки
        arcade.schedule(self.start_spawn_enemies, self.spawn_attack_rate)
        arcade.schedule(self.spawn_rockets, self.rocket_attack_rate)

        # Саундтрек
        self.view.background_soundtrack.stop(self.view.background_soundtrack_player)
        self.view.background_soundtrack_player = self.boss_soundtrack.play(volume=sounds_volume.soundtracks, loop=True)

    def update(self, delta_time: float = 1 / 60) -> None:
        super().update()

        if not self.is_dead:
            # Создание врагов из очереди призыва
            self.spawn_enemies(delta_time)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        super().update_animation(delta_time)

        if not self.is_dead:
            # Анимация атаки
            if self.attack_animation_running:
                self.attack_animation_duration += delta_time
                if self.attack_animation_duration >= self.attack_animation_speed:
                    self.attack_animation_frame = (self.attack_animation_frame + 1) % len(
                        self.attack_animation_textures)
                    self.texture = self.attack_animation_textures[self.attack_animation_frame]

                    self.attack_animation_duration = 0.0
            else:
                # Обновление анимации
                self.attack_animation_frame: int = 0
                self.attack_animation_duration: float = 0.0
                self.texture = self.idle_texture

    def start_spawn_enemies(self, *args) -> None:
        """Добавление врагов в очередь призыва"""

        # Воспроизведение звуков
        self.attack_sound.play(volume=sounds_volume.enemies)

        # Запуск анимации
        self.attack_animation_running = True

        # Добавление врагов в очередь призыва
        self.spawn_queue.extend(choices([BasicEnemy, FastEnemy, BigEnemy, PushEnemy], k=6))

    def spawn_enemies(self, delta_time: float) -> None:
        """Создание врагов из очереди призыва"""

        if self.spawn_queue:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_rate:
                # Создание врага
                self.view.enemies_list.append(
                    self.spawn_queue.pop(0)(self.center_x, self.center_y, self.way[self.curr_part - 1:], 2.0, self.view)
                )

                # Обновление таймера
                self.spawn_timer = 0.0
        else:
            # Отключение анимации
            self.attack_animation_running = False

    def spawn_rockets(self, *args) -> None:
        """Создание ракет"""

        # Воспроизведение звуков
        self.attack_sound.play(volume=sounds_volume.enemies)

        # Подбор трёх случайных башен
        targets: list = sample(
            list(self.view.towers_turrets_list),
            min(self.rockets_count, len(self.view.towers_turrets_list))
        )
        # Создание ракеты для выбранной башни
        for target in targets:
            # Выбор направления
            rocket_direction: int = choice((-1, 1))

            # Создание ракеты
            rocket = self.Rocket(
                self.rocket_speed * rocket_direction, self.rocket_stun_duration, self,
                path_or_texture=self.rocket_texture, scale=ENEMY_SCALING * (2 / 3),
                center_x=target.center_x, center_y=target.center_y + 32 * ENEMY_SCALING * 10 * -rocket_direction,
                angle=180 if rocket_direction == -1 else 0
            )
            self.view.enemy_bullets_list.append(rocket)

    def start_2_phase(self) -> None:
        """Запуск второй фазы"""

        # Смена текстур
        self.idle_texture = self.idle_texture_2_phase
        self.attack_animation_textures = self.attack_animation_textures_2_phase
        # Изменение показателей
        self.speed *= 2
        self.armor *= 0.6
        self.spawn_attack_rate *= 0.6
        self.rocket_attack_rate *= 0.6
        self.rockets_count = int(self.rockets_count * 1.5)
        self.rocket_stun_duration *= 1.5
        # Перезаписывание авто вызовов атак
        arcade.unschedule(self.start_spawn_enemies)
        arcade.schedule(self.start_spawn_enemies, self.spawn_attack_rate)
        arcade.unschedule(self.spawn_rockets)
        arcade.schedule(self.spawn_rockets, self.rocket_attack_rate)

        # Переключение флага
        self.is_2_phase = True

    def get_damage(self, damage: float) -> None:
        """Получение урона"""

        super().get_damage(damage)

        if (not self.is_2_phase) and (self.health <= self.health_for_2_phase):
            self.start_2_phase()

    def dead(self) -> None:
        """Смерть"""

        super().dead()

        # Воспроизведение звуков
        self.dead_sound.play(volume=sounds_volume.enemies)

        # Снятие всех авто вызовов
        arcade.unschedule(self.start_spawn_enemies)
        arcade.unschedule(self.spawn_rockets)

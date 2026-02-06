# Графика
import arcade
# Звуки
import pyglet.media
import sounds_volume


class Waves:
    def __init__(self, waves: tuple, wave_rate: float, enemy_way: list, difficulty: float, view: arcade.View):
        # Привязка к уровню
        self.view: arcade.View = view

        # Загрузка звуков
        self.wave_appear: arcade.Sound = arcade.load_sound("resources/assets/sounds/wave_appear.wav")

        # Список волн
        self.waves: list = [list(wave) for wave in waves]
        # Очередь появления противников
        self.enemy_queue: list = []

        # Атрибуты для генерации врагов
        self.enemy_start_x: int | float = self.view.enemy_base_list[0].center_x
        self.enemy_start_y: int | float = self.view.enemy_base_list[0].center_y
        self.enemy_way: list = enemy_way
        self.difficulty: float = difficulty

        # Атрибуты времени
        self.wave_rate: float = wave_rate  # Скорость появления волн
        self.wave_timer: float = wave_rate  # Время с появления последней волны
        self.spawn_rate: float = 0.25  # Скорость появления врагов
        self.spawn_timer: float = 0.0  # Время с появления последнего врага
        self.skip_rate: float = 4.0  # Лимит с вызова волны для вызова новой

        # Флаги
        self.running: bool = False  # Пора ли запускать волны
        self.skipping: bool = False  # Можно ли вызвать следующую волну в ручную

    def update(self, delta_time: float):
        # Проверка на запуск волн
        if not self.running:
            return

        # Появление новой волны
        if self.waves:
            self.wave_timer += delta_time
            self.spawn_wave()

        # Появление нового врага
        if self.enemy_queue:
            self.spawn_timer += delta_time
            self.spawn_enemy()

    def can_skip_wave(self) -> bool:
        """Проверка на возможность вызова следующей волны вручную"""

        return self.wave_timer >= self.skip_rate and self.waves

    def skip_wave(self) -> None:
        """Вызов следующей волны вручную"""

        if self.can_skip_wave():
            self.skipping = True

    def spawn_wave(self) -> None:
        """Вызов волны"""

        if self.wave_timer >= self.wave_rate or self.skipping:
            # Воспроизведение звука
            self.wave_appear.play(volume=sounds_volume.others)

            # Добавление врагов в очередь
            self.enemy_queue.extend(self.waves.pop(0))
            # Повышение сложности
            self.difficulty += 0.05

            # Сброс таймера
            self.wave_timer = 0.0 if self.waves else self.wave_rate
            # Сброс флага
            self.skipping = False

    def spawn_enemy(self) -> None:
        """Создание врагов"""

        if self.spawn_timer >= self.spawn_rate:
            # Создание противника
            self.view.enemies_list.append(
                self.enemy_queue.pop()(
                    self.enemy_start_x, self.enemy_start_y, self.enemy_way, self.difficulty, self.view
                )
            )

            # Сброс таймера
            self.spawn_timer = 0.0

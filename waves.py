import arcade


class Waves:
    def __init__(self, waves: tuple,
                 wave_rate: float,
                 enemies_list: arcade.SpriteList,
                 enemy_base_position: tuple,
                 enemy_way: list,
                 difficulty: float):
        # Список волн
        self.waves: list = [list(wave) for wave in waves]
        # Очередь появления противников
        self.enemy_queue: list = []

        # Атрибуты для генерации врагов
        self.enemies_list: arcade.SpriteList = enemies_list
        self.enemy_start_x: int | float = enemy_base_position[0]
        self.enemy_start_y: int | float = enemy_base_position[1]
        self.enemy_way: list = enemy_way
        self.difficulty: float = difficulty

        # Атрибуты времени
        self.wave_rate = wave_rate  # Скорость появления волн
        self.wave_timer = wave_rate  # Время с появления последней волны
        self.spawn_rate = 0.25  # Скорость появления врагов
        self.spawn_timer = 0.0  # Время с появления последнего врага
        self.skip_rate = 4.0  # Лимит с вызова волны для вызова новой

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

    def skip_wave(self) -> None:
        """Вызов следующей волны вручную"""

        if self.wave_timer >= self.skip_rate and self.waves:
            self.skipping = True

    def spawn_wave(self) -> None:
        """Вызов волны"""

        if self.wave_timer >= self.wave_rate or self.skipping:
            # Добавление врагов в очередь
            self.enemy_queue.extend(self.waves.pop(0))
            # Повышение сложности
            self.difficulty += 0.05

            # Сброс таймера
            self.wave_timer = 0.0
            # Сброс флага
            self.skipping = False

    def spawn_enemy(self) -> None:
        """Создание врагов"""

        if self.spawn_timer >= self.spawn_rate:
            # Создание противника
            self.enemies_list.append(
                self.enemy_queue.pop()(self.enemy_start_x, self.enemy_start_y, self.enemy_way, self.difficulty)
            )

            # Сброс таймера
            self.spawn_timer = 0

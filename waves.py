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
        self.spawn_rate = 0.2  # Скорость появления врагов
        self.spawn_timer = 0.0  # Время с появления последнего врага

        # Флаги
        self.running = False  # Пора ли запускать волны

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

    def spawn_wave(self) -> None:
        """Вызов волны"""

        if self.wave_timer >= self.wave_rate:
            # Добавление врагов в очередь
            self.enemy_queue.extend(self.waves.pop(0))
            # Повышение сложности
            self.difficulty += 0.05

            # Сброс таймера
            self.wave_timer = 0.0

    def spawn_enemy(self) -> None:
        """Создание врагов"""

        if self.spawn_timer >= self.spawn_rate:
            # Создание противника
            self.enemies_list.append(
                self.enemy_queue.pop()(self.enemy_start_x, self.enemy_start_y, self.enemy_way, self.difficulty)
            )

            # Сброс таймера
            self.spawn_timer = 0

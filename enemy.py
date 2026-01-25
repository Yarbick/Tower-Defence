import arcade


class Enemy(arcade.Sprite):
    def __init__(self, center_x: int | float, center_y: int | float, way: tuple, difficulty: float):
        super().__init__(center_x=center_x, center_y=center_y)

        # Загрузка текстур
        self.idle_texture: arcade.Texture | None = None
        self.dead_animation_textures: tuple[arcade.Texture] | None = None

        self.texture = self.idle_texture

        # Показатели врага
        self.health: int | None = None
        self.armor: int | None = None
        self.speed: int | None = None

        # Направление движения
        self.direction_x: int | None = None
        self.direction_y: int | None = None

        # Путь к базе игрока
        self.way: tuple = way
        self.curr_part: int = 0

        # Флаги
        self.is_dead = False

        # Анимации
        # Анимация смерти
        self.dead_animation_running: bool = False
        self.dead_animation_frame: int = 0
        self.dead_animation_duration: float = 0.0
        self.dead_animation_speed: float = 1 / len(self.dead_animation_textures) * 3

    def update(self, delta_time: float = 1 / 60) -> None:
        # Проверка на смерть
        if self.dead():
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
                    self.texture = self.dead_animation_texture[self.dead_animation_frame]

    def move(self, delta_time: float) -> None:
        """Движение врага"""

        # Обновление позиции
        self.center_x += self.speed * self.direction_x * delta_time
        self.center_y += self.speed * self.direction_y * delta_time

        # Проверка на прохождение отрезка пути
        if (((self.way[self.curr_part][0] <= self.center_x and self.direction_x == 1) or
             (self.way[self.curr_part][0] >= self.center_x and self.direction_x == -1)) and
                ((self.way[self.curr_part][1] <= self.center_y and self.direction_y == 1) or
                 (self.way[self.curr_part][1] >= self.center_y and self.direction_y == -1))):
            # Закрепление врага на конец прошлого отрезка пути
            self.center_x, self.center_y = self.way[self.curr_part]

            # Переход на другой отрезок
            self.curr_part += 1
            # Смерть при завершении пути
            if self.curr_part >= len(self.way):
                self.dead()
                return

            # Определение нового направления
            if self.center_x == self.way[self.curr_part][0]:
                self.direction_x = 0
            elif self.center_x < self.way[self.curr_part][0]:
                self.direction_x = 1
            elif self.center_x > self.way[self.curr_part][0]:
                self.direction_x = -1
            if self.center_y == self.way[self.curr_part][1]:
                self.direction_y = 0
            elif self.center_y < self.way[self.curr_part][1]:
                self.direction_y = 1
            elif self.center_y > self.way[self.curr_part][1]:
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

    def dead(self) -> None:
        """Смерть врага"""

        # Переключение флага
        self.is_dead = True

        # Обновление и запуск анимации
        self.dead_animation_running = True
        self.dead_animation_duration = 0.0
        self.dead_animation_frame = 0
        self.texture = self.dead_animation_textures[self.dead_animation_frame]

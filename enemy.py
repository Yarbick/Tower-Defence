import arcade

ENEMY_SCALING = 3.0
DEAD_ANIMATION_SPEED = 1 / 30


class Enemy(arcade.Sprite):
    """Основные методы врагов"""

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
            if self.dead_animation_duration >= DEAD_ANIMATION_SPEED:
                self.dead_animation_duration = 0.0

                self.dead_animation_frame += 1
                if self.dead_animation_frame >= len(self.dead_animation_textures):
                    self.dead_animation_running = False
                    # Удаление врага после завершения анимации
                    self.remove_from_sprite_lists()
                else:
                    self.texture = self.dead_animation_textures[self.dead_animation_frame]

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
                # Нанесение урона базе
                self.scene.player_health -= self.damage
                # Вычитание стоимости врага от денег игрока
                self.scene.player_money -= self.kill_reward

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

    def get_damage(self, damage) -> None:
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
        self.scene.player_money += self.kill_reward

        # Обновление и запуск анимации
        self.dead_animation_running = True
        self.dead_animation_duration = 0.0
        self.dead_animation_frame = 0
        self.texture = self.dead_animation_textures[self.dead_animation_frame]


class BasicEnemy(Enemy):
    """Базовый враг"""

    def __init__(self, center_x: int | float, center_y: int | float, way: tuple, difficulty: float, scene):
        super().__init__(center_x=center_x, center_y=center_y, scale=ENEMY_SCALING)
        # Привязка к уровню
        self.scene = scene

        # Загрузка текстур
        self.idle_texture: arcade.Texture = arcade.load_texture("resources/assets/images/enemies/basic_enemy/idle.png")
        self.dead_animation_textures: tuple[arcade.Texture] = tuple(
            arcade.load_texture(f"resources/assets/images/enemies/basic_enemy/dead_animation/dead_{i}.png")
            for i in range(1, 6)
        )

        self.texture = self.idle_texture

        # Показатели врага
        self.health: int = 100 * difficulty
        self.armor: int = 0.1
        self.speed: int = 200
        self.damage: int = 1
        self.kill_reward: int = 20

        # Направление движения
        self.direction_x: int = 0
        self.direction_y: int = 0

        # Путь к базе игрока
        self.way: tuple = way
        self.curr_part: int = 0
        # Пройденное расстояние
        self.way_traveled: float = 0

        # Флаги
        self.is_dead = False

        # Анимации
        # Анимация смерти
        self.dead_animation_running: bool = False
        self.dead_animation_frame: int = 0
        self.dead_animation_duration: float = 0.0


class FastEnemy(Enemy):
    """Быстрый враг"""

    def __init__(self, center_x: int | float, center_y: int | float, way: tuple, difficulty: float, scene):
        super().__init__(center_x=center_x, center_y=center_y, scale=ENEMY_SCALING)
        # Привязка к уровню
        self.scene = scene

        # Загрузка текстур
        self.idle_texture: arcade.Texture = arcade.load_texture("resources/assets/images/enemies/fast_enemy/idle.png")
        self.dead_animation_textures: tuple[arcade.Texture] = tuple(
            arcade.load_texture(f"resources/assets/images/enemies/fast_enemy/dead_animation/dead_{i}.png")
            for i in range(1, 6)
        )

        self.texture = self.idle_texture

        # Показатели врага
        self.health: int = 75 * difficulty
        self.armor: int = 0
        self.speed: int = 350
        self.damage: int = 1
        self.kill_reward: int = 15

        # Направление движения
        self.direction_x: int = 0
        self.direction_y: int = 0

        # Путь к базе игрока
        self.way: tuple = way
        self.curr_part: int = 0
        # Пройденное расстояние
        self.way_traveled: float = 0

        # Флаги
        self.is_dead = False

        # Анимации
        # Анимация смерти
        self.dead_animation_running: bool = False
        self.dead_animation_frame: int = 0
        self.dead_animation_duration: float = 0.0


class BigEnemy(Enemy):
    """Большой враг"""

    def __init__(self, center_x: int | float, center_y: int | float, way: tuple, difficulty: float, scene):
        super().__init__(center_x=center_x, center_y=center_y, scale=ENEMY_SCALING)
        # Привязка к уровню
        self.scene = scene

        # Загрузка текстур
        self.idle_texture: arcade.Texture = arcade.load_texture("resources/assets/images/enemies/big_enemy/idle.png")
        self.dead_animation_textures: tuple[arcade.Texture] = tuple(
            arcade.load_texture(f"resources/assets/images/enemies/big_enemy/dead_animation/dead_{i}.png")
            for i in range(1, 6)
        )

        self.texture = self.idle_texture

        # Показатели врага
        self.health: int = 250 * difficulty
        self.armor: int = 0.4
        self.speed: int = 150
        self.damage: int = 2
        self.kill_reward: int = 30

        # Направление движения
        self.direction_x: int = 0
        self.direction_y: int = 0

        # Путь к базе игрока
        self.way: tuple = way
        self.curr_part: int = 0
        # Пройденное расстояние
        self.way_traveled: float = 0

        # Флаги
        self.is_dead = False

        # Анимации
        # Анимация смерти
        self.dead_animation_running: bool = False
        self.dead_animation_frame: int = 0
        self.dead_animation_duration: float = 0.0


class PushEnemy(Enemy):
    """Враг-пушер"""

    def __init__(self, center_x: int | float, center_y: int | float, way: tuple, difficulty: float, scene):
        super().__init__(center_x=center_x, center_y=center_y, scale=ENEMY_SCALING)
        # Привязка к уровню
        self.scene = scene

        # Загрузка текстур
        self.idle_texture: arcade.Texture = arcade.load_texture("resources/assets/images/enemies/push_enemy/idle.png")
        self.dead_animation_textures: tuple[arcade.Texture] = tuple(
            arcade.load_texture(f"resources/assets/images/enemies/push_enemy/dead_animation/dead_{i}.png")
            for i in range(1, 6)
        )

        self.texture = self.idle_texture

        # Показатели врага
        self.health: int = 225 * difficulty
        self.armor: int = 0.25
        self.speed: int = 275
        self.damage: int = 2
        self.kill_reward: int = 40

        # Направление движения
        self.direction_x: int = 0
        self.direction_y: int = 0

        # Путь к базе игрока
        self.way: tuple = way
        self.curr_part: int = 0
        # Пройденное расстояние
        self.way_traveled: float = 0

        # Флаги
        self.is_dead = False

        # Анимации
        # Анимация смерти
        self.dead_animation_running: bool = False
        self.dead_animation_frame: int = 0
        self.dead_animation_duration: float = 0.0

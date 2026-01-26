import arcade
import controls

import enemy

TILE_SIZE = 64
TILEMAP_SCALING = 2.0
LEVELS = {
    "1": {
        "tilemap": "resources/levels/level1.tmx",
        "waves": None,
        "difficulty": 1.0
    },
    "2": {
        "tilemap": "resources/levels/level2.tmx",
        "waves": None,
        "difficulty": 1.1
    },
    "3": {
        "tilemap": "resources/levels/level3.tmx",
        "waves": None,
        "difficulty": 1.2
    },
    "4": {
        "tilemap": "resources/levels/level4.tmx",
        "waves": None,
        "difficulty": 1.3
    },
    "5": {
        "tilemap": "resources/levels/level5.tmx",
        "waves": None,
        "difficulty": 1.5
    }
}
CAMERA_SPEED = 300
CAMERA_SPEED_BOOST = 2.0


class Level(arcade.View):
    """Уровень"""

    def __init__(self, level_name: str):
        super().__init__()
        arcade.set_background_color(arcade.color.Color.from_hex_string("#1A1A1A"))

        # Размеры окна
        self.screen_width: int | None = None
        self.screen_height: int | None = None

        # Карта
        self.tilemap: arcade.TileMap = arcade.load_tilemap(LEVELS[level_name]["tilemap"], scaling=TILEMAP_SCALING)
        self.background_list: arcade.SpriteList | None = None
        self.enemy_base_list: arcade.SpriteList | None = None
        self.player_base_list: arcade.SpriteList | None = None
        self.road_list: arcade.SpriteList | None = None
        self.platforms_list: arcade.SpriteList | None = None
        # Размеры карты
        self.world_width: int | None = None
        self.world_height: int | None = None

        # Сложность
        self.difficulty: float = LEVELS[level_name]["difficulty"]
        # Путь для врагов
        self.enemies_way: list | None = None

        # Игровые объекты
        self.enemies_list: arcade.SpriteList | None = None

        # Камеры
        self.world_camera: arcade.Camera2D | None = None

        # Нажатые клавиши
        self.keys_pressed: set | None = None

    def setup(self):
        # Получение размеров окна
        self.screen_width, self.screen_height = self.width, self.height

        # Создание карты
        self.background_list = self.tilemap.sprite_lists["background"]
        self.enemy_base_list = self.tilemap.sprite_lists["enemy_base"]
        self.player_base_list = self.tilemap.sprite_lists["player_base"]
        self.road_list = self.tilemap.sprite_lists["road"]
        self.platforms_list = self.tilemap.sprite_lists["platforms"]
        # Получение размеров карты
        self.world_width, self.world_height = self.tilemap.width * TILE_SIZE, self.tilemap.height * TILE_SIZE

        # Нахождение пути для противников
        self.find_enemies_way()
        # Создание противников
        self.enemies_list = arcade.SpriteList()

        # Создание камер
        self.world_camera = arcade.camera.Camera2D()
        self.world_camera.position = self.world_width * 0.5, self.world_height * 0.5

        # Обнуляем клавиши
        self.keys_pressed = set()

    def on_draw(self) -> None:
        self.clear()

        # Отрисовка игрового мира
        self.world_camera.use()
        # Отрисовка карты
        self.background_list.draw()
        self.enemy_base_list.draw()
        self.player_base_list.draw()
        self.road_list.draw()
        self.platforms_list.draw()
        # Отрисовка игровых объектов
        self.enemies_list.draw()

    def on_update(self, delta_time: float) -> None:
        # Движение камеры
        self.world_camera_move(delta_time)

        # Движение врагов
        self.enemies_list.update()
        self.enemies_list.update_animation()

    def on_key_press(self, key: int, modifiers: int) -> None:
        self.keys_pressed.add(key)

    def on_key_release(self, key: int, modifiers: int) -> None:
        self.keys_pressed.remove(key)

    def on_resize(self, width: int, height: int) -> None:
        # Получаем новые размеры экрана
        self.screen_width, self.screen_height = width, height

        # Настраиваем камеры под новые размеры
        self.world_camera.match_window()
        self.check_camera_borders(self.world_camera)

    def check_camera_borders(self, camera: arcade.Camera2D) -> None:
        """Проверка камеры на выход за границы экрана"""

        # Обновление позиции камеры при выходе за границы
        camera.position = (
            min(self.world_width - self.screen_width * 0.5, max(self.screen_width * 0.5, camera.position[0])),
            min(self.world_height - self.screen_height * 0.5, max(self.screen_height * 0.5, camera.position[1]))
        )

    def world_camera_move(self, delta_time: float) -> None:
        """Движение игровой камеры"""

        # Определение ускорения камеры
        speed_boost: float = CAMERA_SPEED_BOOST if controls.camera_move_boost in self.keys_pressed else 1.0
        # Движение камеры
        new_position: list[int, int] = list(self.world_camera.position)
        if controls.camera_move_left in self.keys_pressed:
            new_position[0] += -CAMERA_SPEED * speed_boost * delta_time
        if controls.camera_move_right in self.keys_pressed:
            new_position[0] += CAMERA_SPEED * speed_boost * delta_time
        if controls.camera_move_down in self.keys_pressed:
            new_position[1] += -CAMERA_SPEED * speed_boost * delta_time
        if controls.camera_move_up in self.keys_pressed:
            new_position[1] += CAMERA_SPEED * speed_boost * delta_time
        self.world_camera.position = tuple(new_position)
        # Проверка на выход за границы
        self.check_camera_borders(self.world_camera)

    def find_enemies_way(self):
        """Нахождение пути для врагов"""

        # Подготовка данных для алгоритма
        # Размеры поля
        rows: int
        cols: int
        # Координаты базы врага
        start_row: int
        start_col: int
        # Координаты базы игрока
        end_row: int
        end_col: int
        # Список дорог
        road_grid: list[list[int]]

        # Пересоздание списка
        self.enemies_way = []
        # Размер поля
        rows, cols = self.tilemap.height, self.tilemap.width
        # Нахождение базы врагов
        enemy_base_grid = self.tilemap.get_tilemap_layer("enemy_base").data
        start_row, start_col = [
            (row, col) for row in range(rows) for col in range(cols) if enemy_base_grid[row][col] != 0
        ][0]
        # Нахождение базы игрока
        player_base_grid = self.tilemap.get_tilemap_layer("player_base").data
        end_row, end_col = [
            (row, col) for row in range(rows) for col in range(cols) if player_base_grid[row][col] != 0
        ][0]
        # Получение поля с дорогами
        road_grid = self.tilemap.get_tilemap_layer("road").data

        # Алгоритм поиска пути
        parent: tuple[int, int] | None = None  # Предыдущая клетка
        row, col = start_row, start_col  # Текущая клетка
        while True:
            # Добавление клетки в путь
            self.enemies_way.append(((col + 0.5) * TILE_SIZE, (rows - row - 0.5) * TILE_SIZE))

            # Останавливает алгоритм, если нашёл базу игрока
            if (row, col) == (end_row, end_col):
                break

            # Поиск соседних дорог
            neighbors = [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]
            for nh_row, nh_col in neighbors:
                if 0 <= nh_row < rows and 0 <= nh_col < cols:
                    if ((nh_row, nh_col) == (end_row, end_col) or
                            (nh_row, nh_col) != parent and road_grid[nh_row][nh_col] != 0):
                        parent = row, col
                        row, col = nh_row, nh_col
                        break

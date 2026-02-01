# Прочие библиотеки
from inspect import getmembers
# Графика
import arcade
import arcade.gui
from pyglet.graphics import Batch
# Бинды клавиатуры
import controls
# Игровые объекты
import tower
import enemy
import waves
# Импорт прототипов
from resources.prototypes.levels import LEVELS
from resources.prototypes.towers import TOWERS

# Константы
TILEMAP_SCALING = 2.0
TILE_SIZE = 32 * TILEMAP_SCALING
CAMERA_SPEED = 300
CAMERA_SPEED_BOOST = 2.0


class TowerMenu(arcade.gui.UIWidget):
    """Макет меню башен"""

    # Кнопки
    class CloseButton(arcade.gui.UIFlatButton):
        """Кнопка закрытия меню"""

        def on_click(self, event: arcade.gui.UIOnClickEvent):
            # Закрытие меню
            menu: TowerMenu = self.parent
            menu.close()

    # Методы
    def match_window(self) -> None:
        """Настройка координат виджетов под размер экрана"""

        # Заголовок
        self.header_text.right = self.view.screen_width - 20
        self.header_text.top = self.view.screen_height - 20

        # Кнопка закрытия меню
        self.close_button.right = self.header_text.left - 30
        self.close_button.top = self.view.screen_height

        # Кнопки для создания башен
        self.buttons_layout.left = self.header_text.left
        self.buttons_layout.top = self.view.screen_height * 0.875

        # Главный виджет
        self.left = self.close_button.right - 1
        self.bottom = self.buttons_layout.bottom - 20
        self.width = abs(self.view.screen_width - self.close_button.right)
        self.height = abs(self.view.screen_height - self.buttons_layout.bottom) + 21

    def close(self) -> None:
        """Закрытие меню"""

        self.visible = False


class AddTowerMenu(TowerMenu):
    """Меню создания новой башни"""

    # Кнопки
    class AddTowerButton(arcade.gui.UITextureButton):
        """Кнопка создания башни"""

        def __init__(self, adding_tower: tower.Tower, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.adding_tower: tower.Tower = adding_tower

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            menu: AddTowerMenu = self.parent.parent

            # Создание новой башни
            new_tower: tower.Tower = self.adding_tower(
                menu.view.selected_tile[0], menu.view.selected_tile[1], menu.view
            )
            # Проверка на достаточное количество денег
            if menu.view.player_money >= new_tower.price:
                # Вычитание денег у игрока
                menu.view.player_money -= new_tower.price

                # Добавление башни
                menu.view.towers_bases_list.append(new_tower.base)
                menu.view.towers_turrets_list.append(new_tower)

                # Закрытие меню
                menu.close()

    # Методы
    def __init__(self, view: arcade.View):
        super().__init__()
        self.with_background(color=(40, 40, 40))

        # Привязка к уровню
        self.view: arcade.View = view

        # Заголовок
        self.header_text = arcade.gui.UILabel("Create tower", font_name="CGXYZ LCD", font_size=12)
        self.add(self.header_text)

        # Кнопка закрытия меню
        self.close_button = self.CloseButton(
            width=50, height=50, text=">",
            style={
                "normal": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(40, 40, 40)),
                "hover": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(60, 60, 60)),
                "press": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(80, 80, 80)),
                "disabled": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(160, 160, 160))
            }
        )
        self.add(self.close_button)

        # Кнопки для создания башен
        self.buttons_layout = arcade.gui.UIBoxLayout(vertical=False, space_between=10, width=50, height=50)
        self.add(self.buttons_layout)
        for tower_name in TOWERS:
            # Поиск класса башни по названию прототипа
            tower_class: tower.Tower | None = None
            for obj in getmembers(tower):
                try:
                    if obj[1].prototype_name == tower_name:
                        tower_class = obj[1]
                        break
                except AttributeError:
                    continue

            # Создание кнопки
            if tower_class:
                button = self.AddTowerButton(
                    adding_tower=tower_class, width=50, height=50,
                    texture=arcade.load_texture(f"resources/assets/images/towers/{tower_name}/base.png")
                )
                label = arcade.gui.UILabel(text=str(TOWERS[tower_name]["price"]), font_name="CGXYZ LCD", font_size=6)
                button.add(label)
                self.buttons_layout.add(button)

        # Настройка координат виджетов под размер экрана
        self.match_window()


class EditTowerMenu(TowerMenu):
    """Меню изменения башни"""

    # Кнопки
    class UpgradeTowerButton(arcade.gui.UIFlatButton):
        """Кнопка улучшения башни"""

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            menu: EditTowerMenu = self.parent.parent

            # Поиск башни для улучшения
            editing_tower: tower.Tower = arcade.get_sprites_at_point(
                menu.view.selected_tile, menu.view.towers_turrets_list
            )[0]
            # Проверка на возможность удаления
            if editing_tower.upgrade_price <= menu.view.player_money and editing_tower.upgrade_level < 5:
                # Вычитание денег у игрока
                menu.view.player_money -= int(editing_tower.upgrade_price)

                # Улучшение башни
                editing_tower.upgrade()

    class DeleteTowerButton(arcade.gui.UIFlatButton):
        """Кнопка удаления башни"""

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            menu: EditTowerMenu = self.parent.parent

            # Поиск башни для удаления
            deleting_tower: tower.Tower = arcade.get_sprites_at_point(
                menu.view.selected_tile, menu.view.towers_turrets_list
            )[0]

            # Прибавление денег игроку
            menu.view.player_money += int(deleting_tower.price * deleting_tower.upgrade_level * 0.6)
            # Удаление башни
            deleting_tower.base.remove_from_sprite_lists()
            deleting_tower.remove_from_sprite_lists()

            # Закрытие меню
            menu.close()

    # Методы
    def __init__(self, view: arcade.View):
        super().__init__()
        self.with_background(color=(40, 40, 40))

        # Привязка к уровню
        self.view: arcade.View = view

        # Заголовок
        self.header_text = arcade.gui.UILabel("Edit tower", font_name="CGXYZ LCD", font_size=12)
        self.add(self.header_text)

        # Кнопка закрытия меню
        self.close_button = self.CloseButton(
            width=50, height=50, text=">",
            style={
                "normal": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(40, 40, 40)),
                "hover": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(60, 60, 60)),
                "press": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(80, 80, 80)),
                "disabled": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(160, 160, 160))
            }
        )
        self.add(self.close_button)

        # Кнопки для изменения башен
        self.buttons_layout = arcade.gui.UIBoxLayout(vertical=False, space_between=10, width=50, height=50)
        self.add(self.buttons_layout)
        # Кнопка улучшения башни
        upgrade_button = self.UpgradeTowerButton(
            width=90, height=50, text="Upgrade",
            style={
                "normal": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(60, 60, 60)),
                "hover": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(80, 80, 80)),
                "press": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(100, 100, 100)),
                "disabled": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(160, 160, 160))
            }
        )
        self.buttons_layout.add(upgrade_button)
        # Кнопка удаления башни
        delete_button = self.DeleteTowerButton(
            width=90, height=50, text="Delete",
            style={
                "normal": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(60, 60, 60)),
                "hover": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(80, 80, 80)),
                "press": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(100, 100, 100)),
                "disabled": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(160, 160, 160))
            }
        )
        self.buttons_layout.add(delete_button)

        # Настройка координат виджетов под размер экрана
        self.match_window()


class ResultWidget(arcade.gui.UIWidget):
    """Окно с выводом результатов игры"""

    # Кнопки
    class ReturnToMenuButton(arcade.gui.UIFlatButton):
        """Кнопка возвращения в главное меню"""

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            level_view: arcade.View = self.parent.view
            window: arcade.Window = level_view.window

            # Возвращение в главно меню
            level_view.ui_manager.disable()
            main_menu_view: arcade.View = level_view.parent.parent
            main_menu_view.setup()
            window.show_view(main_menu_view)

    # Методы
    def __init__(self, view: arcade.View, game_result: bool):
        super().__init__()
        self.with_background(color=(40, 40, 40))
        self.size = 500, 300

        # Привязка к уровню
        self.view: arcade.View = view

        # Заголовок
        self.header_text = arcade.gui.UILabel(
            text="VICTORY" if game_result else "DEFEAT",
            text_color=arcade.color.GREEN if game_result else arcade.color.RED,
            font_name="CGXYZ LCD", font_size=20
        )
        self.add(self.header_text)

        # Кнопка возвращения в главное меню
        self.return_to_menu_button = self.ReturnToMenuButton(
            width=300, height=50, text="Return to Menu",
            style={
                "normal": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=12, bg=(60, 60, 60)),
                "hover": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=12, bg=(80, 80, 80)),
                "press": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=12, bg=(100, 100, 100)),
                "disabled": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=12, bg=(160, 160, 160))
            }
        )
        self.add(self.return_to_menu_button)

        # Настройка координат виджетов под размер экрана
        self.match_window()

    def match_window(self) -> None:
        """Настройка координат виджетов под размер экрана"""

        # Заголовок
        self.header_text.center_x = self.view.screen_width * 0.5
        self.header_text.center_y = self.view.screen_height * 0.5 + self.height * 0.25

        # Кнопка возвращения в главное меню
        self.return_to_menu_button.center_x = self.view.screen_width * 0.5
        self.return_to_menu_button.center_y = self.view.screen_height * 0.5 - self.height * 0.25

        # Главный виджет
        self.center_x = self.view.screen_width * 0.5
        self.center_y = self.view.screen_height * 0.5


class Level(arcade.View):
    """Уровень"""

    def __init__(self, level_name: str, parent: arcade.View):
        super().__init__()
        arcade.set_background_color(arcade.color.Color.from_hex_string("#1A1A1A"))
        self.level_name = level_name
        self.parent: arcade.View = parent

        # Размеры окна
        self.screen_width: int | None = None
        self.screen_height: int | None = None

        # Карта
        self.tilemap: arcade.TileMap | None = None
        self.background_list: arcade.SpriteList | None = None
        self.enemy_base_list: arcade.SpriteList | None = None
        self.player_base_list: arcade.SpriteList | None = None
        self.road_list: arcade.SpriteList | None = None
        self.platforms_list: arcade.SpriteList | None = None
        # Размеры карты
        self.world_width: int | None = None
        self.world_height: int | None = None

        # Волны
        self.waves: waves.Waves | None = None

        # Игровые объекты
        self.enemies_list: arcade.SpriteList | None = None
        self.towers_bases_list: arcade.SpriteList | None = None
        self.towers_turrets_list: arcade.SpriteList | None = None
        self.enemy_bullets_list: arcade.SpriteList | None = None
        self.bullets_list: arcade.SpriteList | None = None

        # Камеры
        self.world_camera: arcade.Camera2D | None = None
        self.gui_camera: arcade.Camera2D | None = None

        # Атрибуты для логики игры
        self.player_health: int | None = None
        self.player_money: int | None = None
        self.game_status: bool | None = None  # None - игра не закончена, False - поражение, True - победа

        # Атрибуты интерфейса
        # Текст
        self.batch: Batch | None = None
        self.health_text: arcade.Text | None = None
        self.wave_number_text: arcade.Text | None = None
        self.time_left_text: arcade.Text | None = None
        self.skip_text: arcade.Text | None = None
        # Виджеты
        self.ui_manager: arcade.gui.UIManager | None = None
        # Выделенный тайл
        self.selected_tile: tuple | None = None

        # Нажатые клавиши
        self.keys_pressed: set | None = None

    def setup(self):
        # Получение размеров окна
        self.screen_width, self.screen_height = self.width, self.height

        # Создание карты
        self.tilemap = arcade.load_tilemap(LEVELS[self.level_name]["tilemap"], scaling=TILEMAP_SCALING)
        self.background_list = self.tilemap.sprite_lists["background"]
        self.enemy_base_list = self.tilemap.sprite_lists["enemy_base"]
        self.player_base_list = self.tilemap.sprite_lists["player_base"]
        self.road_list = self.tilemap.sprite_lists["road"]
        self.platforms_list = self.tilemap.sprite_lists["platforms"]
        # Получение размеров карты
        self.world_width, self.world_height = self.tilemap.width * TILE_SIZE, self.tilemap.height * TILE_SIZE

        # Создание противников
        self.enemies_list = arcade.SpriteList()

        # Создание волн
        self.waves = waves.Waves(
            LEVELS[self.level_name]["waves"],
            LEVELS[self.level_name]["wave_rate"],
            self.find_enemies_way(),
            LEVELS[self.level_name]["difficulty"],
            self
        )

        # Создание пуль
        self.bullets_list = arcade.SpriteList()
        self.enemy_bullets_list = arcade.SpriteList()

        # Создание башен
        self.towers_bases_list = arcade.SpriteList()
        self.towers_turrets_list = arcade.SpriteList()

        # Создание камер
        self.world_camera = arcade.camera.Camera2D()
        self.world_camera.position = self.world_width * 0.5, self.world_height * 0.5
        self.gui_camera = arcade.camera.Camera2D()

        # Обновление атрибутов логики игры до значений по умолчанию
        self.player_health = 20
        self.player_money = 200
        self.game_status = None

        # Создание интерфейса:
        # Текст
        self.batch = Batch()
        self.health_text = arcade.Text(
            f"Health: {max(0, self.player_health)}",
            20, self.screen_height - 20, arcade.color.WHITE,
            font_name="CGXYZ LCD", anchor_x="left", anchor_y="top", batch=self.batch
        )
        self.money_text = arcade.Text(
            f"Money: {max(0, self.player_health)}",
            260, self.screen_height - 20, arcade.color.WHITE,
            font_name="CGXYZ LCD", anchor_x="left", anchor_y="top", batch=self.batch
        )
        self.wave_number_text = arcade.Text(
            f"Wave: {max(0, len(LEVELS[self.level_name]["waves"]) - len(self.waves.waves))}",
            20, 20, arcade.color.WHITE,
            font_name="CGXYZ LCD", anchor_x="left", anchor_y="bottom", batch=self.batch
        )
        self.time_left_text = arcade.Text(
            f"Time left: {int(max(0, self.waves.wave_rate - self.waves.wave_timer))}",
            200, 20, arcade.color.WHITE,
            font_name="CGXYZ LCD", anchor_x="left", anchor_y="bottom", batch=self.batch
        )
        self.skip_text = arcade.Text(
            f"SKIP",
            470, 20, arcade.color.WHITE,
            font_name="CGXYZ LCD", anchor_x="left", anchor_y="bottom", batch=self.batch
        )

        # Виджеты
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager._pixelated = True
        self.ui_manager.enable()
        # Меню создания башен
        self.add_tower_menu = AddTowerMenu(self)
        self.add_tower_menu.visible = False
        self.ui_manager.add(self.add_tower_menu)
        # Меню изменения башен
        self.edit_tower_menu = EditTowerMenu(self)
        self.edit_tower_menu.visible = False
        self.ui_manager.add(self.edit_tower_menu)
        # Окно с выводом результатов игры
        self.result_widget: ResultWidget | None = None

        # Выделение выбранного тайла
        self.selected_tile = None

        # Обнуление клавиш
        self.keys_pressed = set()

    def on_draw(self) -> None:
        self.clear()

        # Отрисовка игрового мира
        self.world_camera.use()
        # Отрисовка карты
        self.background_list.draw(pixelated=True)
        self.enemy_base_list.draw(pixelated=True)
        self.player_base_list.draw(pixelated=True)
        self.road_list.draw(pixelated=True)
        self.platforms_list.draw(pixelated=True)
        # Отрисовка игровых объектов
        self.enemies_list.draw(pixelated=True)
        self.towers_bases_list.draw(pixelated=True)
        self.towers_turrets_list.draw(pixelated=True)
        self.enemy_bullets_list.draw(pixelated=True)
        self.bullets_list.draw(pixelated=True)
        # Отрисовка выбранного тайла
        if self.selected_tile:
            arcade.draw_lbwh_rectangle_outline(
                self.selected_tile[0] - 0.5 * TILE_SIZE, self.selected_tile[1] - 0.5 * TILE_SIZE, TILE_SIZE, TILE_SIZE,
                arcade.color.WHITE, 2 * TILEMAP_SCALING
            )

        # Отрисовка интерфейса
        self.gui_camera.use()
        # Отрисовка текста
        self.batch.draw()
        # Отрисовка виджетов
        self.ui_manager.draw()

    def on_update(self, delta_time: float) -> None:
        # Проверка на конец игры
        if self.game_status is not None:
            return
        self.check_game_status()

        # Движение камеры
        self.world_camera_move(delta_time)

        # Обновление волн
        if controls.skip_wave in self.keys_pressed:
            if not self.waves.running:
                self.waves.running = True
            else:
                self.waves.skip_wave()
        self.waves.update(delta_time)

        # Движение врагов
        self.enemies_list.update()
        self.enemies_list.update_animation()

        # Обновление пуль
        self.enemy_bullets_list.update()
        self.bullets_list.update()

        # Обновление башен
        self.towers_turrets_list.update()

        # Обновление интерфейса
        # Текст
        self.health_text.text = f"Health: {max(0, self.player_health)}"
        self.money_text.text = f"Money: {self.player_money}"
        self.wave_number_text.text = f"Wave: {max(0, len(LEVELS[self.level_name]["waves"]) - len(self.waves.waves))}"
        self.time_left_text.text = f"Time left: {int(max(0, self.waves.wave_rate - self.waves.wave_timer))}"
        self.skip_text.batch = self.batch if self.waves.can_skip_wave() else None

    def on_resize(self, width: int, height: int) -> None:
        # Получаем новые размеры экрана
        self.screen_width, self.screen_height = width, height

        # Настройка камер под новые размеры
        self.world_camera.match_window()
        self.check_camera_borders(self.world_camera)
        self.gui_camera.match_window()
        self.gui_camera.position = (
            self.screen_width * 0.5,
            self.screen_height * 0.5
        )

        # Настройка интерфейса под новые размеры
        self.health_text.y = self.screen_height - 20
        self.money_text.y = self.screen_height - 20

        self.add_tower_menu.match_window()
        self.edit_tower_menu.match_window()
        if self.result_widget:
            self.result_widget.match_window()

    def on_mouse_press(self, x: int, y: int, key: int, modifiers: int) -> None:
        # Проверка на конец игры
        if self.game_status is not None:
            return

        # Нахождение координат клика относительно тайлов игрового мира
        world_x: float = ((self.world_camera.position[0] - self.screen_width * 0.5 + x) // TILE_SIZE + 0.5) * TILE_SIZE
        world_y: float = ((self.world_camera.position[1] - self.screen_height * 0.5 + y) // TILE_SIZE + 0.5) * TILE_SIZE

        # Выделение клетки
        self.selected_tile = world_x, world_y

        # Изменение башен
        if key == arcade.MOUSE_BUTTON_LEFT:
            self.edit_tower(world_x, world_y)

    def on_key_press(self, key: int, modifiers: int) -> None:
        self.keys_pressed.add(key)

    def on_key_release(self, key: int, modifiers: int) -> None:
        self.keys_pressed.remove(key)

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

    def find_enemies_way(self) -> list:
        """Нахождение пути для врагов"""

        # Подготовка данных для алгоритма
        enemies_way: list = []
        # Размер поля
        rows: int = self.tilemap.height
        cols: int = self.tilemap.width
        # Координаты базы врагов
        start_row: int = int(rows - 1 - self.enemy_base_list[0].center_y // TILE_SIZE)
        start_col: int = int(self.enemy_base_list[0].center_x // TILE_SIZE)
        # Координаты базы игрока
        end_row: int = int(rows - 1 - self.player_base_list[0].center_y // TILE_SIZE)
        end_col: int = int(self.player_base_list[0].center_x // TILE_SIZE)
        # Поле с дорогами
        road_grid: list = self.tilemap.get_tilemap_layer("road").data

        # Алгоритм поиска пути
        parent: tuple | None = None  # Предыдущая клетка
        row, col = start_row, start_col  # Текущая клетка
        while True:
            # Добавление клетки в путь
            enemies_way.append(((col + 0.5) * TILE_SIZE, (rows - row - 0.5) * TILE_SIZE))

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

        return enemies_way

    def edit_tower(self, world_x: int, world_y: int) -> None:
        """Создание и изменение башен"""

        # Закрытие всех меню
        self.add_tower_menu.visible = False
        self.edit_tower_menu.visible = False
        self.ui_manager.disable()

        # Проверка на клик по платформе
        if arcade.get_sprites_at_point((world_x, world_y), self.platforms_list):
            self.ui_manager.enable()
            # Проверка на нахождение башни на платформе
            if arcade.get_sprites_at_point((world_x, world_y), self.towers_turrets_list):
                # Открытие меню изменения башни
                self.edit_tower_menu.visible = True
            else:
                # Открытие меню создания новой башни
                self.add_tower_menu.visible = True

    def check_game_status(self):
        """Проверка на завершение игры"""

        if self.player_health <= 0:  # Проверка на поражение
            self.game_status = False
        elif (not self.enemies_list) and (not self.waves.waves) and (not self.waves.enemy_queue):  # Проверка на победу
            self.game_status = True
        else:
            return
        # Создание окна результатов игры
        self.result_widget = ResultWidget(self, self.game_status)
        self.ui_manager.add(self.result_widget)

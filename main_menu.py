# Графика
import arcade
import arcade.gui
# Звуки
import pyglet.media
# Меню уровней
from levels_menu import LevelsMenu
# Стили
import styles

# Константы
TILEMAP_SCALING = 2.0
TILE_SIZE = 32 * TILEMAP_SCALING
BACKGROUND_SPEED = 100


class MainMenu(arcade.View):
    """Главное меню"""

    # Виджеты
    class PlayButton(arcade.gui.UIFlatButton):
        """Кнопка Play"""

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            window: arcade.Window = arcade.get_window()
            main_menu_view: arcade.View = window.current_view

            # Отключение процессов главного меню
            main_menu_view.background_soundtrack.stop(main_menu_view.background_soundtrack_player)
            main_menu_view.ui_manager.disable()

            # Переключение на меню уровней
            levels_menu_view: arcade.View = LevelsMenu(main_menu_view)
            levels_menu_view.setup()
            window.show_view(levels_menu_view)

    class ExitButton(arcade.gui.UIFlatButton):
        """Кнопка Exit"""

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            window: arcade.Window = arcade.get_window()

            # Закрытие окна
            window.close()

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.Color.from_hex_string("#1A1A1A"))

        # Загружаем шрифты
        arcade.load_font("resources/assets/fonts/CGXYZLCD/CGXYZLCD-Regular.otf")
        # Загружаем текстуры
        self.logo_texture: arcade.Texture = arcade.load_texture("resources/assets/images/logo/logo_text.png")
        # Загружаем саундтреки
        self.background_soundtrack: arcade.Sound = arcade.load_sound(
            "resources/assets/sounds/soundtracks/main_menu.mp3"
        )

        # Размер окна
        self.screen_width: int | None = None
        self.screen_height: int | None = None

        # Размер мира
        self.world_width: int | None = None
        self.world_height: int | None = None

        # Задний фон
        self.background_list: arcade.SpriteList | None = None

        # Камеры
        self.world_camera: arcade.Camera2D | None = None
        self.gui_camera: arcade.Camera2D | None = None

        # Менеджер интерфейса
        self.ui_manager: arcade.gui.UIManager | None = None

        # Саундтреки
        self.background_soundtrack_player: pyglet.media.Player | None = None

    def setup(self) -> None:
        # Получение размеров окна
        self.screen_width: int = self.width
        self.screen_height: int = self.height

        # Создание виджетов
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager._pixelated = True
        self.ui_manager.enable()
        # Кнопка Play
        self.play_button = self.PlayButton(
            x=self.screen_width * 0.5 - 123, y=self.screen_height * 0.7 - 125 - 32,
            width=256, height=64, text="PLAY", style=styles.uiflatbutton_basic
        )
        self.ui_manager.add(self.play_button)
        # Кнопка Exit
        self.exit_button = self.ExitButton(
            x=self.screen_width * 0.5 - 123, y=self.screen_height * 0.7 - 200 - 32,
            width=256, height=64, text="EXIT", style=styles.uiflatbutton_basic
        )
        self.ui_manager.add(self.exit_button)

        # Загрузка карты
        tilemap: arcade.TileMap = arcade.load_tilemap("resources/levels/menu.tmx", scaling=TILEMAP_SCALING)
        self.background_list = tilemap.sprite_lists["background"]
        # Получение размеров карты
        self.world_width, self.world_height = tilemap.width * TILE_SIZE, tilemap.height * TILE_SIZE

        # Создание камер
        self.gui_camera = arcade.camera.Camera2D()
        self.world_camera = arcade.camera.Camera2D()
        self.world_camera.position = self.screen_width * 0.5, self.screen_height * 0.5
        self.world_camera.move_direction = 1  # Аттрибут камеры для направления движения

        # Запуск саундтрека
        self.background_soundtrack_player = pyglet.media.Player()
        self.background_soundtrack_player = self.background_soundtrack.play(loop=True)

    def on_draw(self) -> None:
        self.clear()

        # Отрисовка игрового мира
        self.world_camera.use()
        self.background_list.draw(pixelated=True)

        # Отрисовка интерфейса
        self.gui_camera.use()
        arcade.draw_texture_rect(
            self.logo_texture,
            arcade.Rect(0, 0, 0, 0, 620, 64, self.screen_width * 0.5, self.screen_height * 0.7), pixelated=True
        )
        self.ui_manager.draw()

    def on_update(self, delta_time: float) -> None:
        # Движение камеры
        self.world_camera.position = (
            self.world_camera.position[0] + BACKGROUND_SPEED * self.world_camera.move_direction * delta_time,
            self.screen_height * 0.5
        )
        # Смена направления движения камеры
        if not (self.screen_width * 0.5 < self.world_camera.position[0] < self.world_width - self.screen_width * 0.5):
            self.world_camera.move_direction = -self.world_camera.move_direction

    def on_resize(self, width: int, height: int) -> None:
        # Получение новых размеров окна
        self.screen_width, self.screen_height = width, height

        # Настройка камер под новые размеры
        self.world_camera.match_window()
        self.world_camera.position = (
            min(self.world_width - self.screen_width * 0.5,
                max(self.screen_width * 0.5, self.world_camera.position[0])),
            min(self.world_height - self.screen_height * 0.5,
                max(self.screen_height * 0.5, self.world_camera.position[1]))
        )
        self.gui_camera.match_window()
        self.gui_camera.position = (
            self.screen_width * 0.5,
            self.screen_height * 0.5
        )
        # Настройка кнопок под новые размеры
        self.play_button.center_x, self.play_button.center_y = self.screen_width * 0.5, self.screen_height * 0.7 - 125
        self.exit_button.center_x, self.exit_button.center_y = self.screen_width * 0.5, self.screen_height * 0.7 - 200

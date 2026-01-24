import arcade
import arcade.gui
from arcade.gui.widgets.buttons import UIFlatButtonStyle

# Константы
TILE_SIZE = 64
TILEMAP_SCALING = 2.0
BACKGROUND_SPEED = 100


class PlayButton(arcade.gui.UIFlatButton):
    """Кнопка Play"""

    pass


class ExitButton(arcade.gui.UIFlatButton):
    """Кнопка Exit"""

    def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
        # Закрываем окно
        self.parent.window.close()


class MainMenu(arcade.View):
    """Главное меню"""

    def __init__(self):
        super().__init__()

        # Загружаем шрифты
        arcade.load_font("resources/assets/fonts/CGXYZLCD/CGXYZLCD-Regular.otf")
        # Загружаем текстуры
        self.logo_texture = arcade.load_texture("resources/assets/images/logo/logo_text.png")

        # Аттрибуты игрового мира:
        # Камера
        self.world_camera: arcade.Camera2D = arcade.camera.Camera2D()
        # Задний фон
        self.background_list: arcade.SpriteList | None = None
        # Размер мира
        self.world_width: int | None = None
        self.world_height: int | None = None

        # Аттрибуты интерфейса:
        # Камера
        self.gui_camera: arcade.Camera2D = arcade.camera.Camera2D()
        # Размер окна
        self.screen_width: int = self.window.screen.width
        self.screen_height: int = self.window.screen.height
        # Создание виджетов
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        # Общий стиль кнопок
        button_style = {
            "normal": UIFlatButtonStyle(font_name="CGXYZ LCD", font_size=16, bg=(60, 60, 60)),
            "hover": UIFlatButtonStyle(font_name="CGXYZ LCD", font_size=16, bg=(80, 80, 80)),
            "press": UIFlatButtonStyle(font_name="CGXYZ LCD", font_size=16, bg=(100, 100, 100)),
            "disabled": UIFlatButtonStyle(font_name="CGXYZ LCD", font_size=16, bg=(160, 160, 160))
        }
        # Кнопка Play
        self.play_button = PlayButton(
            x=self.screen_width * 0.5, y=self.screen_height * 0.7 - 125,
            width=256, height=64, text="PLAY", style=button_style
        )
        self.ui_manager.add(self.play_button)
        # Кнопка Exit
        self.exit_button = ExitButton(
            x=self.screen_width * 0.5, y=self.screen_height * 0.7 - 200,
            width=256, height=64, text="EXIT", style=button_style
        )
        self.ui_manager.add(self.exit_button)

    def setup(self) -> None:
        # Загрузка карты
        tilemap: arcade.TileMap = arcade.load_tilemap("resources/levels/menu.tmx", scaling=TILEMAP_SCALING)
        self.background_list = tilemap.sprite_lists["background"]
        # Получение размеров карты
        self.world_width, self.world_height = tilemap.width * TILE_SIZE, tilemap.height * TILE_SIZE

        # Перемещение камеры в начальную позицию
        self.world_camera.position = self.screen_width * 0.5, self.screen_height * 0.5
        self.world_camera.move_direction = 1  # Аттрибут камеры для направления движения

    def on_draw(self) -> None:
        self.clear()

        # Отрисовка игрового мира
        self.world_camera.use()
        self.background_list.draw()

        # Отрисовка интерфейса
        self.gui_camera.use()
        arcade.draw_texture_rect(
            self.logo_texture,
            arcade.Rect(0, 0, 0, 0, 620, 64, self.screen_width * 0.5, self.screen_height * 0.7)
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
        self.gui_camera.match_window()
        self.gui_camera.position = self.screen_width * 0.5, self.screen_height * 0.5

        # Настройка кнопок под новые размеры
        self.play_button.center_x, self.play_button.center_y = self.screen_width * 0.5, self.screen_height * 0.7 - 125
        self.exit_button.center_x, self.exit_button.center_y = self.screen_width * 0.5, self.screen_height * 0.7 - 200

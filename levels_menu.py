import arcade
import arcade.gui
from pyglet.graphics import Batch
from arcade.gui.widgets.buttons import UIFlatButtonStyle


class BackButton(arcade.gui.UIFlatButton):
    """Кнопка Back"""

    def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
        # Возвращаемся в главное меню
        main_menu_view = self.parent.window.current_view.parent
        main_menu_view.setup()
        self.parent.window.show_view(main_menu_view)


class LevelsMenu(arcade.View):
    def __init__(self, parent):
        super().__init__()
        arcade.set_background_color(arcade.color.Color.from_hex_string("#1A1A1A"))
        self.parent = parent

        # Загружаем шрифты
        arcade.load_font("resources/assets/fonts/CGXYZLCD/CGXYZLCD-Regular.otf")

        # Аттрибуты интерфейса:
        # Камера
        self.gui_camera: arcade.Camera2D | None = None
        # Размер окна
        self.screen_width: int | None = None
        self.screen_height: int | None = None
        # Контейнер для текста
        self.batch: Batch | None = None
        # Менеджер интерфейса
        self.ui_manager: arcade.gui.UIManager | None = None

    def setup(self) -> None:
        # Получение размеров окна
        self.screen_width: int = self.width
        self.screen_height: int = self.height

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
        # Кнопка Back
        self.back_button = BackButton(
            x=self.screen_width - 133, y=self.screen_height - 70,
            width=128, height=64, text="BACK", style=button_style
        )
        self.ui_manager.add(self.back_button)

        # Создание текста
        self.batch = Batch()
        # Заголовок
        self.header_text = arcade.Text(
            "Levels",
            20, self.screen_height - 20,
            arcade.color.WHITE, 20, font_name="CGXYZ LCD",
            anchor_y="top", batch=self.batch
        )

        # Создание камеры
        self.gui_camera = arcade.camera.Camera2D()

    def on_draw(self) -> None:
        self.clear()

        # Отрисовка интерфейса
        self.gui_camera.use()
        arcade.draw_line(
            0, self.screen_height - self.header_text.font_size * 4,
            self.screen_width, self.screen_height - self.header_text.font_size * 4,
            arcade.color.Color.from_hex_string("#2A2A2A"), 4
        )
        self.batch.draw()
        self.ui_manager.draw()

    def on_resize(self, width: int, height: int) -> None:
        # Получение новых размеров окна
        self.screen_width, self.screen_height = width, height

        # Настройка камеры под новые размеры
        self.gui_camera.match_window()
        self.gui_camera.position = self.screen_width * 0.5, self.screen_height * 0.5
        # Настройка заголовка под новые размеры
        self.header_text.x = 20
        self.header_text.y = self.screen_height - 20
        # Настройка кнопок под новые размеры
        self.back_button.left = self.screen_width - 133
        self.back_button.bottom = self.screen_height - 70

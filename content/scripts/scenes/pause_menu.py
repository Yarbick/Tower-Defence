"""Сцена меню паузы"""

# Графика
import arcade
import arcade.gui
# Бинды клавиатуры
import player_data.settings.controls.controls as controls
# Стили
import content.scripts.styles.styles as styles


class PauseMenu(arcade.View):
    """Меню при паузе на уровне"""

    # Виджеты
    class ContinueButton(arcade.gui.UIFlatButton):
        """Кнопка для возвращения на уровень"""

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            window: arcade.Window = arcade.get_window()
            pause_menu_view: arcade.View = window.current_view

            # Переключение на уровень
            level_view: arcade.View = pause_menu_view.parent
            level_view.ui_manager.enable()
            level_view.background_soundtrack_player.play()
            window.show_view(level_view)

    class ReturnToMainMenuButton(arcade.gui.UIFlatButton):
        """Кнопка для возвращения на уровень"""

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            window: arcade.Window = arcade.get_window()
            pause_menu_view: arcade.View = window.current_view

            # Переключение в главное меню
            main_menu_view: arcade.View = pause_menu_view.parent.parent.parent
            main_menu_view.setup()
            window.show_view(main_menu_view)

    def __init__(self, parent: arcade.View):
        super().__init__()
        arcade.set_background_color(arcade.color.Color.from_hex_string("#1A1A1A"))
        self.parent: arcade.View = parent

        # Размер окна
        self.screen_width: int | None = None
        self.screen_height: int | None = None

        # Камеры
        self.gui_camera: arcade.Camera2D | None = None

        # Виджеты
        self.ui_manager: arcade.gui.UIManager | None = None

    def setup(self) -> None:
        # Создание камер
        self.gui_camera = arcade.camera.Camera2D()

        # Создание виджетов
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager._pixelated = True
        self.ui_manager.enable()
        # Заголовок
        self.header_label = arcade.gui.UILabel(
            text="PAUSE", font_name="CGXYZ LCD", font_size=24
        )
        self.ui_manager.add(self.header_label)
        # Кнопка возвращения на предыдущую сцену
        self.continue_button = self.ContinueButton(
            width=320, height=64, text="Continue", style=styles.uiflatbutton_basic
        )
        self.ui_manager.add(self.continue_button)
        # Кнопка возвращения в главное меню
        self.return_to_main_menu_button = self.ReturnToMainMenuButton(
            width=320, height=64, text="Main Menu", style=styles.uiflatbutton_basic
        )
        self.ui_manager.add(self.return_to_main_menu_button)

        # Подстраивание под размеры
        self.on_resize(self.width, self.height)

    def on_draw(self) -> None:
        self.clear()

        # Отрисовка интерфейса
        # Камеры
        self.gui_camera.use()
        # Виджеты
        self.ui_manager.draw()

    def on_resize(self, width: int, height: int) -> None:
        # Получение новых размеров экрана
        self.screen_width, self.screen_height = width, height

        # Настройка камер под новые размеры
        self.gui_camera.match_window()
        self.gui_camera.position = (
            self.screen_width * 0.5,
            self.screen_height * 0.5
        )
        # Настройка виджетов
        self.header_label.center_x = self.screen_width * 0.5
        self.header_label.center_y = self.screen_height * 0.7

        self.continue_button.center_x = self.header_label.center_x
        self.continue_button.center_y = self.header_label.bottom - 80

        self.return_to_main_menu_button.center_x = self.continue_button.center_x
        self.return_to_main_menu_button.top = self.continue_button.bottom - 15

    def on_hide_view(self) -> None:
        # Отключение прогрессов меню паузы
        self.ui_manager.disable()

    def on_key_press(self, key: int, modifiers: int) -> None:
        # Окно на весь экран
        if key == controls.fullscreen:
            window: arcade.Window = arcade.get_window()
            window.set_fullscreen(not window.fullscreen)
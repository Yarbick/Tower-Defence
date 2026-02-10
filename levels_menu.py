# Графика
import arcade
import arcade.gui
from pyglet.graphics import Batch
# Уровни
from level import Level
# Прототипы
from resources.prototypes.levels import LEVELS
# Данные игрока
import player_data
# Стили
import styles


class LevelsMenu(arcade.View):
    """Меню выбора уровня"""

    # Виджеты
    class BackButton(arcade.gui.UIFlatButton):
        """Кнопка Back"""

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            window: arcade.Window = arcade.get_window()
            levels_menu_view: arcade.View = window.current_view

            # Возвращение в главное меню
            main_menu_view: arcade.View = levels_menu_view.parent
            main_menu_view.setup()
            window.show_view(main_menu_view)

    class LevelButton(arcade.gui.UIFlatButton):
        """Кнопка переключения на уровень"""

        def __init__(self, level_name: str, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.level_name: str = level_name

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            window: arcade.Window = arcade.get_window()
            levels_menu_view: arcade.View = window.current_view

            # Переключение на уровень
            level_view: arcade.View = Level(self.level_name, levels_menu_view)
            level_view.setup()
            window.show_view(level_view)

    def __init__(self, parent: arcade.View):
        super().__init__()
        arcade.set_background_color(arcade.color.Color.from_hex_string("#1A1A1A"))
        self.parent: arcade.View = parent

        # Загружаем шрифты
        arcade.load_font("resources/assets/fonts/CGXYZLCD/CGXYZLCD-Regular.otf")

        # Размер окна
        self.screen_width: int | None = None
        self.screen_height: int | None = None

        # Камера
        self.gui_camera: arcade.Camera2D | None = None

        # Контейнер для текста
        self.batch: Batch | None = None

        # Менеджер интерфейса
        self.ui_manager: arcade.gui.UIManager | None = None

    def setup(self) -> None:
        # Обновление данных об игроке
        player_data.get_available_towers()
        player_data.get_available_levels()

        # Получение размеров окна
        self.screen_width: int = self.width
        self.screen_height: int = self.height

        # Создание камер
        self.gui_camera = arcade.camera.Camera2D()

        # Создание текста
        self.batch = Batch()
        # Заголовок
        self.header_text = arcade.Text(
            x=0, y=0,
            text="Levels", color=arcade.color.WHITE, font_size=20, font_name="CGXYZ LCD",
            anchor_y="top", batch=self.batch
        )
        # Создание виджетов
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager._pixelated = True
        self.ui_manager.enable()
        # Кнопка Back
        self.back_button = self.BackButton(
            width=128, height=64, text="BACK", style=styles.uiflatbutton_basic
        )
        self.ui_manager.add(self.back_button)
        # Layout для кнопок уровней
        self.levels_layout = arcade.gui.UIBoxLayout(
            vertical=True, space_between=10
        )
        # Добавление кнопок
        for level_name in LEVELS:
            level_button = self.LevelButton(
                level_name,
                width=self.screen_width - self.levels_layout.left * 2, text=level_name, style=styles.uiflatbutton_basic
            )
            level_button.disabled = level_name not in player_data.levels.keys()
            self.levels_layout.add(level_button)
        self.levels_layout.fit_content()
        self.ui_manager.add(self.levels_layout)

        # Подстраивание под размеры
        self.on_resize(self.width, self.height)

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
        # Настройка виджетов под новые размеры
        self.header_text.x = 20
        self.header_text.y = self.screen_height - 20

        self.back_button.left = self.screen_width - 133
        self.back_button.bottom = self.screen_height - 70

        self.levels_layout.left = 20
        self.levels_layout.top = self.screen_height - self.header_text.font_size * 4 - 20
        for level_button in self.levels_layout.children:
            level_button.width = self.screen_width - self.levels_layout.left * 2
        self.levels_layout.width = self.screen_width - self.levels_layout.left * 2

    def on_hide_view(self) -> None:
        # Отключение процессов меню уровней
        self.ui_manager.disable()

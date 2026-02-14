"""Сцена меню настроек"""

# Csv
import csv
# Графика
import arcade
import arcade.gui
# Стили
import content.scripts.styles.styles as styles
# Бинды клавиатуры
import player_data.settings.controls.controls as controls
# Звуки
import player_data.settings.sounds.sounds_volume as sounds_volume


class SettingsMenu(arcade.View):
    """Меню для настроек"""

    # Виджеты
    class KeySelectButton(arcade.gui.UIFlatButton):
        """Кнопка для выбора бинда для действия"""

        def __init__(self, action: str, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.action: str = action

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            window: arcade.Window = arcade.get_window()
            settings_menu_view: arcade.View = window.current_view

            if settings_menu_view.selected_action is None:
                # Привязка бинда
                settings_menu_view.selected_action = self

                # Смена текста
                self.text = "..."

    class SoundVolumeSlider(arcade.gui.UISlider):
        """Слайдер для смены громкости звука"""

        def __init__(self, sound_type: str, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.sound_type = sound_type

        def on_change(self, event: arcade.gui.UIOnChangeEvent) -> None:
            # Получение родителей
            window: arcade.Window = arcade.get_window()
            settings_menu_view: arcade.View = window.current_view

            # Запись нового значения
            settings_menu_view.sounds_parameters[self.sound_type] = self.value / 100

    class ConfirmButton(arcade.gui.UIFlatButton):
        """Кнопка Confirm"""

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            window: arcade.Window = arcade.get_window()
            settings_menu_view: arcade.View = window.current_view

            # Запись изменений биндов в файл
            controls.set_controls(settings_menu_view.controls_parameters)
            with open("player_data/settings/controls/controls.csv", mode="w", encoding="UTF-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["action", "key"])

                writer.writerows(
                    [(action, settings_menu_view.controls_parameters[action])
                     for action in settings_menu_view.controls_parameters.keys()]
                )
            # Запись изменений звуков в файл
            sounds_volume.set_volumes(settings_menu_view.sounds_parameters)
            with open("player_data/settings/sounds/sounds_volume.csv", mode="w", encoding="UTF-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["sound_type", "volume"])

                writer.writerows(
                    [(sound_type, settings_menu_view.sounds_parameters[sound_type])
                     for sound_type in settings_menu_view.sounds_parameters.keys()]
                )

    class BackButton(arcade.gui.UIFlatButton):
        """Кнопка Back"""

        def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
            # Получение родителей
            window: arcade.Window = arcade.get_window()
            settings_menu_view: arcade.View = window.current_view

            # Возвращение в главное меню
            main_menu_view: arcade.View = settings_menu_view.parent
            main_menu_view.setup()
            window.show_view(main_menu_view)

    def __init__(self, parent: arcade.View) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.Color.from_hex_string("#1A1A1A"))
        self.parent: arcade.View = parent

        # Размер окна
        self.screen_width: int | None = None
        self.screen_height: int | None = None

        # Параметры настроек
        self.controls_parameters: dict | None = None
        self.sounds_parameters: dict | None = None

        # Текущее действие для привязки бинда
        self.selected_action: arcade.gui.UIFlatButton | None = None

        # Камеры
        self.gui_camera: arcade.Camera2D | None = None

        # Виджеты
        self.ui_manager: arcade.gui.UIManager | None = None

    def setup(self) -> None:
        # Получение текущих параметров
        self.controls_parameters = controls.controls_data.copy()
        self.sounds_parameters = sounds_volume.sounds_volume_data.copy()

        # Сброс привязки биндов
        self.selected_action = None

        # Создание камер
        self.gui_camera = arcade.camera.Camera2D()

        # Создание виджетов
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager._pixelated = True
        self.ui_manager.enable()

        # Заголовок
        self.header_label = arcade.gui.UILabel(
            text="SETTINGS", font_name="CGXYZ LCD", font_size=24
        )
        self.ui_manager.add(self.header_label)

        # Параметры биндов
        # Заголовок
        self.controls_header_label = arcade.gui.UILabel(
            text="Controls:", font_name="CGXYZ LCD", font_size=16
        )
        self.ui_manager.add(self.controls_header_label)
        # Layout для изменения параметров
        self.controls_layout = arcade.gui.UIBoxLayout(
            vertical=False, space_between=30, align="left"
        )
        self.ui_manager.add(self.controls_layout)
        action_layout = arcade.gui.UIBoxLayout(
            vertical=True, space_between=10, align="left"
        )
        self.controls_layout.add(action_layout)
        key_layout = arcade.gui.UIBoxLayout(
            vertical=True, space_between=10, align="left"
        )
        self.controls_layout.add(key_layout)
        for action in self.controls_parameters.keys():
            # Название действия
            action_label = arcade.gui.UILabel(
                text=action, font_name="CGXYZ LCD", font_size=11, align="left"
            )
            action_layout.add(action_label)

            # Кнопка для привязки клавиши
            key_button = self.KeySelectButton(
                action,
                width=96, height=24, style=styles.uiflatbutton_tower_menu,
                text=
                [key for key in controls.all_keys.keys() if controls.all_keys[key] == self.controls_parameters[action]][
                    0]
            )
            key_layout.add(key_button)
        # Подстраивание под виджеты
        action_layout.fit_content()
        key_layout.fit_content()
        self.controls_layout.fit_content()

        # Параметры звука
        # Заголовок
        self.sounds_header_label = arcade.gui.UILabel(
            text="Sounds:", font_name="CGXYZ LCD", font_size=16
        )
        self.ui_manager.add(self.sounds_header_label)
        # Layout для изменения параметров
        self.sounds_layout = arcade.gui.UIBoxLayout(
            vertical=False, space_between=30, align="left"
        )
        self.ui_manager.add(self.sounds_layout)
        sound_type_layout = arcade.gui.UIBoxLayout(
            vertical=True, space_between=10, align="left"
        )
        self.sounds_layout.add(sound_type_layout)
        sound_volume_layout = arcade.gui.UIBoxLayout(
            vertical=True, space_between=10, align="left"
        )
        self.sounds_layout.add(sound_volume_layout)
        for sound_type in self.sounds_parameters.keys():
            # Название типа звука
            sound_type_label = arcade.gui.UILabel(
                text=sound_type, font_name="CGXYZ LCD", font_size=11, align="left"
            )

            sound_type_layout.add(sound_type_label)
            # Слайдер для настройки громкости
            sound_volume_slider = self.SoundVolumeSlider(
                sound_type,
                width=96, height=24,
                min_value=0, max_value=200, value=self.sounds_parameters[sound_type] * 100
            )
            sound_volume_layout.add(sound_volume_slider)
        # Подстраивание под виджеты
        sound_type_layout.fit_content()
        sound_volume_layout.fit_content()
        self.sounds_layout.fit_content()

        # Кнопки
        self.buttons_layout = arcade.gui.UIBoxLayout(
            vertical=False, space_between=10
        )
        self.ui_manager.add(self.buttons_layout)
        # Кнопка Confirm
        self.confirm_button = self.ConfirmButton(
            width=256, height=64, text="CONFIRM", style=styles.uiflatbutton_basic
        )
        self.buttons_layout.add(self.confirm_button)
        # Кнопка Back
        self.back_button = self.BackButton(
            width=256, height=64, text="BACK", style=styles.uiflatbutton_basic
        )
        self.buttons_layout.add(self.back_button)
        self.buttons_layout.fit_content()

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
        # Заголовок
        self.header_label.center_x = self.screen_width * 0.5
        self.header_label.center_y = self.screen_height * 0.9

        # Параметры управления
        self.controls_header_label.left = self.screen_width * 0.05
        self.controls_header_label.top = self.header_label.bottom - 40

        self.controls_layout.fit_content()
        self.controls_layout.left = self.controls_header_label.left + 10
        self.controls_layout.top = self.controls_header_label.bottom - 20

        # Параметры звуков
        self.sounds_header_label.left = self.screen_width * 0.6
        self.sounds_header_label.top = self.header_label.bottom - 40

        self.sounds_layout.fit_content()
        self.sounds_layout.left = self.sounds_header_label.left + 10
        self.sounds_layout.top = self.sounds_header_label.bottom - 20

        # Кнопки
        self.buttons_layout.center_x = self.screen_width * 0.5
        self.buttons_layout.bottom = 30

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # Проверка на наличие смены бинда
        if self.selected_action is not None:
            # Запись новой клавиши в параметры биндов
            self.controls_parameters[self.selected_action.action] = symbol

            # Отрисовка новой клавиши на кнопке
            self.selected_action.text = [
                key for key in controls.all_keys.keys() if controls.all_keys[key] == symbol
            ][0]

            # Удаление режима смены бинда у клавиши
            self.selected_action = None

    def on_hide_view(self) -> None:
        # Отключение процессов меню настроек
        self.ui_manager.disable()

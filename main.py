"""Запуск"""

# Графика
import arcade
from pyglet.image import load as load_image
# Главное меню
from scripts.scenes.main_menu import MainMenu


def main() -> None:
    # Окно
    window: arcade.Window = arcade.Window(1000, 800, "Tower Defence", resizable=True)
    window.set_minimum_size(800, 600)
    window.set_maximum_size(1920, 1080)
    # Иконка
    icon_image = load_image("resources/assets/images/logo/logo_icon.png")
    window.set_icon(icon_image)

    # Главное меню
    main_menu_view: MainMenu = MainMenu()
    main_menu_view.setup()
    window.show_view(main_menu_view)

    # Запуск
    arcade.run()


if __name__ == "__main__":
    main()

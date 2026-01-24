import arcade

from main_menu import MainMenu


def main():
    window = arcade.Window(1000, 900, "Tower Defence", resizable=True)
    window.set_maximum_size(1920, 1080)
    main_menu_view = MainMenu()
    main_menu_view.setup()
    window.show_view(main_menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

import arcade
import arcade.gui


class LevelsMenu(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.Color.from_hex_string("#1A1A1A"))

    def setup(self):
        pass

    def on_draw(self) -> None:
        self.clear()

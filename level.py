import arcade


class Level(arcade.View):
    def __init__(self, level_name: str):
        super().__init__()
        arcade.set_background_color(arcade.color.Color.from_hex_string("#1A1A1A"))

    def setup(self):
        pass

    def on_draw(self) -> None:
        self.clear()

import arcade
import arcade.gui
from arcade.gui import UIOnClickEvent, UIFlatButton
from arcade.gui.widgets.buttons import UIFlatButtonStyle

TILE_SIZE = 64
TILEMAP_SCALING = 2.0
BACKGROUND_SPEED = 100


class PlayButton(arcade.gui.UIFlatButton):
    pass


class ExitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: UIOnClickEvent) -> None:
        self.parent.window.close()


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.load_font("resources/assets/fonts/CGXYZLCD/CGXYZLCD-Regular.otf")
        self.logo_texture = arcade.load_texture("resources/assets/images/logo/logo_text.png")

        self.world_camera: arcade.Camera2D = arcade.camera.Camera2D()
        self.background_list: arcade.SpriteList | None = None
        self.world_width: int | None = None
        self.world_height: int | None = None

        self.gui_camera: arcade.Camera2D = arcade.camera.Camera2D()
        self.screen_width: int = self.window.screen.width
        self.screen_height: int = self.window.screen.height
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        button_style = {
            "normal": UIFlatButtonStyle(font_name="CGXYZ LCD", font_size=16, bg=(60, 60, 60)),
            "hover": UIFlatButtonStyle(font_name="CGXYZ LCD", font_size=16, bg=(80, 80, 80)),
            "press": UIFlatButtonStyle(font_name="CGXYZ LCD", font_size=16, bg=(100, 100, 100)),
            "disabled": UIFlatButtonStyle(font_name="CGXYZ LCD", font_size=16, bg=(160, 160, 160))
        }
        self.play_button = PlayButton(
            x=self.screen_width * 0.5, y=self.screen_height * 0.7 - 125,
            width=256, height=64, text="PLAY", style=button_style
        )
        self.ui_manager.add(self.play_button)
        self.exit_button = ExitButton(
            x=self.screen_width * 0.5, y=self.screen_height * 0.7 - 200,
            width=256, height=64, text="EXIT", style=button_style
        )
        self.ui_manager.add(self.exit_button)

    def setup(self) -> None:
        tilemap: arcade.TileMap = arcade.load_tilemap("resources/levels/menu.tmx", scaling=TILEMAP_SCALING)
        self.background_list = tilemap.sprite_lists["background"]
        self.world_width, self.world_height = tilemap.width * TILE_SIZE, tilemap.height * TILE_SIZE

        self.world_camera.position = self.screen_width * 0.5, self.screen_height * 0.5
        self.world_camera.move_direction = 1

    def on_draw(self) -> None:
        self.clear()

        self.world_camera.use()
        self.background_list.draw()

        self.gui_camera.use()
        arcade.draw_texture_rect(
            self.logo_texture,
            arcade.Rect(0, 0, 0, 0, 620, 64, self.screen_width * 0.5, self.screen_height * 0.7)
        )
        self.ui_manager.draw()

    def on_update(self, delta_time: float) -> None:
        self.world_camera.position = (
            self.world_camera.position[0] + BACKGROUND_SPEED * self.world_camera.move_direction * delta_time,
            self.screen_height * 0.5
        )
        if not (self.screen_width * 0.5 < self.world_camera.position[0] < self.world_width - self.screen_width * 0.5):
            self.world_camera.move_direction = -self.world_camera.move_direction

    def on_resize(self, width: int, height: int) -> None:
        self.screen_width, self.screen_height = width, height

        self.world_camera.match_window()
        self.gui_camera.match_window()
        self.gui_camera.position = self.screen_width * 0.5, self.screen_height * 0.5

        self.play_button.center_x, self.play_button.center_y = self.screen_width * 0.5, self.screen_height * 0.7 - 125
        self.exit_button.center_x, self.exit_button.center_y = self.screen_width * 0.5, self.screen_height * 0.7 - 200

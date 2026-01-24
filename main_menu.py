import arcade


TILE_SIZE = 64
TILEMAP_SCALING = 2.0
BACKGROUND_SPEED = 100


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_list: arcade.SpriteList | None = None
        self.screen_width: int = self.window.screen.width
        self.screen_height: int = self.window.screen.height
        self.world_width: int | None = None
        self.world_height: int | None = None

        self.world_camera: arcade.Camera2D = arcade.camera.Camera2D()
        self.gui_camera: arcade.Camera2D = arcade.camera.Camera2D()

        self.logo_texture: arcade.Texture = arcade.load_texture("resources/assets/logo/logo_text.png")

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
            arcade.Rect(0, 0, 0, 0, 620, 64, self.screen_width * 0.5, self.world_height * 0.5)
        )

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

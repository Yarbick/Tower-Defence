"""Стили для виджетов"""

import arcade.gui

uiflatbutton_basic: dict = {
    "normal": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=16, bg=(60, 60, 60)),
    "hover": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=16, bg=(80, 80, 80)),
    "press": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=16, bg=(100, 100, 100)),
    "disabled": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=16, bg=(120, 120, 120))
}
uiflatbutton_tower_menu: dict = {
    "normal": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(60, 60, 60)),
    "hover": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(80, 80, 80)),
    "press": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(100, 100, 100)),
    "disabled": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=7, bg=(120, 120, 120))
}
uiflatbutton_close_tower_menu: dict = {
    "normal": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(40, 40, 40)),
    "hover": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(60, 60, 60)),
    "press": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(80, 80, 80)),
    "disabled": arcade.gui.UIFlatButton.UIStyle(font_name="CGXYZ LCD", font_size=25, bg=(120, 120, 120))
}

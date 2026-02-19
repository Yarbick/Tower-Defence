"""Загрузка биндов"""

# Прочие библиотеки
from inspect import getmembers
# Csv
import csv
# Клавиши
import arcade.key

# Получение всех клавиш в виде словаря
all_keys: dict = {key: code for key, code in getmembers(arcade.key) if "MOTION" not in key and "MOD" not in key}


def set_controls(new_controls_data: dict) -> None:
    """Назначение биндов"""
    global controls_data, camera_move_left, camera_move_right, camera_move_down, camera_move_up, camera_move_boost, \
        skip_wave, pause, fullscreen

    controls_data = new_controls_data.copy()
    camera_move_left = controls_data["camera_move_left"]
    camera_move_right = controls_data["camera_move_right"]
    camera_move_down = controls_data["camera_move_down"]
    camera_move_up = controls_data["camera_move_up"]
    camera_move_boost = controls_data["camera_move_boost"]
    skip_wave = controls_data["skip_wave"]
    pause = controls_data["pause"]
    fullscreen = controls_data["fullscreen"]


# Получение биндов из файла
with open("player_data/settings/controls/controls.csv", mode="r", encoding="UTF-8") as file:
    # Назначение биндов
    set_controls({action: int(key) for action, key in tuple(csv.reader(file))[1:]})

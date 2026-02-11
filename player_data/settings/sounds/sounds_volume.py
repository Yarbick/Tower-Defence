"""Загрузка громкости звука"""

# Csv
import csv


def set_volumes(new_volume_data: dict) -> None:
    """Назначение громкости звуков"""
    global sounds_volume_data, game_over, soundtracks, towers, enemies, others

    sounds_volume_data = new_volume_data.copy()
    game_over = sounds_volume_data["game_over"]
    soundtracks = sounds_volume_data["soundtracks"]
    towers = sounds_volume_data["towers"]
    enemies = sounds_volume_data["enemies"]
    others = sounds_volume_data["others"]


# Получение громкости звуков из файла
with open("player_data/settings/sounds/sounds_volume.csv", mode="r", encoding="UTF-8") as file:
    # Назначение громкости звуков
    set_volumes({sound_type: float(volume) for sound_type, volume in tuple(csv.reader(file))[1:]})

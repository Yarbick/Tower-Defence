"""Загрузка данных игрока"""

# Csv
import csv
# Прототипы
from content.resources.prototypes.level_prototypes import LEVEL_PROTOTYPES
from content.resources.prototypes.tower_prototypes import TOWER_PROTOTYPES


def get_available_levels() -> None:
    """Получение доступных уровней"""
    global levels

    # Загрузка данных из файла
    with open("player_data/saves/available_levels.csv", mode="r", encoding="UTF-8") as file:
        available_levels: dict = list(csv.DictReader(file))[0]
        levels = {level_name: LEVEL_PROTOTYPES[level_name]
                  for level_name in LEVEL_PROTOTYPES.keys() if available_levels[level_name] == "1"}


def get_available_towers() -> None:
    """Получение доступных башен"""
    global towers

    # Загрузка данных из файла
    with open("player_data/saves/available_towers.csv", mode="r", encoding="UTF-8") as file:
        available_towers: dict = list(csv.DictReader(file))[0]
        towers = {tower_name: TOWER_PROTOTYPES[tower_name]
                  for tower_name in TOWER_PROTOTYPES.keys() if available_towers[tower_name] == "1"}


# Получение данных об игроке
get_available_levels()
get_available_towers()

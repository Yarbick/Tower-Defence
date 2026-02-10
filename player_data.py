# Прочие библиотеки
import csv
# Прототипы
from resources.prototypes.levels import LEVELS
from resources.prototypes.towers import TOWERS


def get_available_levels() -> None:
    """Получение доступных уровней"""
    global levels

    # Загрузка данных из файла
    with open("player_data/saves/available_levels.csv", mode="r", encoding="UTF-8") as file:
        available_levels: dict = list(csv.DictReader(file))[0]
        levels = {level_name: LEVELS[level_name] for level_name in LEVELS.keys() if available_levels[level_name] == "1"}


def get_available_towers() -> None:
    """Получение доступных башен"""
    global towers

    # Загрузка данных из файла
    with open("player_data/saves/available_towers.csv", mode="r", encoding="UTF-8") as file:
        available_towers: dict = list(csv.DictReader(file))[0]
        towers = {tower_name: TOWERS[tower_name] for tower_name in TOWERS.keys() if available_towers[tower_name] == "1"}


# Получение данных об игроке
get_available_levels()
get_available_towers()

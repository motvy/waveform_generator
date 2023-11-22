import pathlib
import os

root_path = pathlib.Path(__file__).parent

start_icon_path = os.path.join(root_path, r"icons\start.svg")
stop_icon_path = os.path.join(root_path, r"icons\stop.svg")
add_icon_path = os.path.join(root_path, r"icons\add.svg")
delete_icon_path = os.path.join(root_path, r"icons\delete.svg")

parameters_path = os.path.join(root_path, "parameters.json")

frequency_dict = {
    0: 10,
    1: 100,
    2: 500,
    3: 1000,
    4: 5000,
    5: 10000,
    6: 20000,
    7: 30000,
}

forms = {
    1: "Треугольный",
    2: "Пилообразный",
    3: "Прямоугольный",
    4: "Шумоподобный"
}

default = {
    "amplitude": 21,
    "frequency": 3,
    "form": 2
}

max_free_form_graphs = 4

display = (1600, 1000)
from gui import main_window

from PyQt5.QtWidgets import QApplication

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

app = QApplication(sys.argv)

window = main_window.MainWindow()
window.show()

app.exec()

"""
1) Добавить таблицу произвольного сигнала
2) Сохранять в json параметры
{
    "single_values": {
        "amplitude": int,
        "frequency": int
    },
    "table_values": {
        1: {
            "amplitude": int,
            "frequency": int
        },
        2: {
            "amplitude": int,
            "frequency": int
        },
        ...
    }
}
3) Построить графики
"""
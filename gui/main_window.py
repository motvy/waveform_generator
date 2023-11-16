
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWidget, QMessageBox

import datetime
import qtawesome as qta

from gui.control_panel import ControlPanel
from gui.graph_canvas import GraphCanvas
import config


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # self.db = SettingsDb()

        stylesheet = """
        QLabel {
            font-size: 12pt;
        }

        QRadioButton {
            font-size: 12pt;
        }

        QLineEdit {
            font-size: 12pt;
        }
        """
        self.setStyleSheet(stylesheet)

        self.setWindowTitle("Функциональный генератор сигналов")
        # self.setFixedSize(QSize(1440, 810))
        self.setFixedSize(QSize(1000, 800))

        # self.setWindowIcon(QIcon(config.app_icon_path))

        self.initUI()
        self.initData()

    def initUI(self):
        self.control_panel = ControlPanel(self)
        self.graph_canvas = GraphCanvas()

        # self.start_btn = QLabel()
        # start_icon = qta.icon('ei.play', color="green")
        # self.start_btn.setPixmap(start_icon.pixmap(QSize(40,40)))
        self.start_btn = QPushButton()
        self.start_btn.setFixedSize(40, 40)
        self.start_btn.setIcon(QIcon(config.start_icon_path))
        self.start_btn.setIconSize(QSize(40, 40))
        self.start_btn.setStyleSheet('background: rgb(240, 240, 240); border: 0px;')

        self.stop_btn = QPushButton()
        # stop_icon = qta.icon('ei.stop', color="red")
        # self.stop_btn.setPixmap(stop_icon.pixmap(QSize(40,40)))
        self.stop_btn = QPushButton()
        self.stop_btn.setFixedSize(50, 40)
        self.stop_btn.setIcon(QIcon(config.stop_icon_path))
        self.stop_btn.setIconSize(QSize(75, 75))
        self.stop_btn.setStyleSheet('background: rgb(240, 240, 240); border: 0px;')

        self.timer_lb = QLabel(str(datetime.timedelta(seconds=0)))
        # self.timer_lb.setStyleSheet('font-size: 12pt;')
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.timer_lb)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.control_panel.layout)
        main_layout.addWidget(self.graph_canvas.frame)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def initData(self):
        pass
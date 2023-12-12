from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QMessageBox

import datetime
import serial

from gui.control_panel import ControlPanel
from gui.graph_canvas import GraphCanvas
import config, utils


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

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
        QTableWidget {
            border: 0px;
            background-color: #F0F0F0;
        }
        QHeaderView::section {
            background-color: transparent;
            font-size: 12pt;
            border: 0px;
        }
        QHeaderView {
            background-color: transparent;
        }

        """
        self.width = int(0.67*config.display[0])
        self.height = int(0.83*config.display[1])

        self.setStyleSheet(stylesheet)

        self.setWindowTitle("Функциональный генератор сигналов")

        self.setFixedSize(QSize(self.width, self.height))

        # self.setWindowIcon(QIcon(config.app_icon_path))

        self.initUI()
        self.initData()

        self.serial_port = serial.Serial('COM1', 9600, timeout=1)
        # self.control_panel.setEnabled(False)
        # self.start_btn.setEnabled(False)
        # self.start_wait_signal()

    def initUI(self):
        self.graph_canvas = GraphCanvas(self)
        self.control_panel = ControlPanel(self)

        self.start_btn = QPushButton()
        self.start_btn.setFixedSize(int(self.width*0.04), int(self.width*0.04))
        self.start_btn.setIcon(QIcon(config.start_icon_path))
        self.start_btn.setIconSize(QSize(int(self.width*0.04), int(self.width*0.04)))
        self.start_btn.setStyleSheet('background: rgb(240, 240, 240); border: 0px;')
        self.start_btn.clicked.connect(self.start_generate)

        # self.stop_btn = QPushButton()
        # self.stop_btn = QPushButton()
        # self.stop_btn.setFixedSize(int(self.width*0.04), int(self.width*0.04))
        # self.stop_btn.setIcon(QIcon(config.stop_icon_path))
        # self.stop_btn.setIconSize(QSize(int(self.width*0.075), int(self.width*0.075)))
        # self.stop_btn.setStyleSheet('background: rgb(240, 240, 240); border: 0px;')

        self.status_lb = QLabel()
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_btn)
        # button_layout.addWidget(self.stop_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.status_lb)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.control_panel.layout)
        main_layout.addWidget(self.graph_canvas.frame)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def initData(self):
        self.manager = utils.ParametersManager()
        self.wait_flag = False
        # timer = QTimer(self)
        # timer.timeout.connect(self.check_uart)
        # timer.start(1000)

    def start_generate(self):
        # self.start_btn.clicked.disconnect()
        # self.control_panel.setEnabled(False)
        # self.start_btn.setEnabled(False)

        frequency = self.graph_canvas.current_frequency
        
        data = self.graph_canvas.getPlotData() + [frequency]
        print(data, len(data))

        # data = [0, 10, 20, 30, 40, 50, 60, 70]
        data_arr = bytearray(data)
        self.serial_port.write(data_arr)

        # line = self.serial_port.readline()
        # if line:
        #     # self.start_wait_signal()
        #     self.control_panel.setEnabled(True)
        #     self.start_btn.setEnabled(True)
        #     self.start_btn.clicked.connect(self.start_generate)
        # else:
        #     QMessageBox.critical(self, 'Функциональный генератор сигналов', 'МК не отвечает. Попробуйте снова.')
        #     self.control_panel.setEnabled(True)
        #     self.start_btn.setEnabled(True)
        #     self.start_btn.clicked.connect(self.start_generate)

    def stop_generate(self):
        self.stop_timer()
        self.start_btn.clicked.connect(self.start_generate)
        self.control_panel.setEnabled(True)

    def check_uart(self):
        if self.wait_flag:
            line = self.serial_port.readline()
            if line:
                self.stop_timer()

    def start_wait_signal(self):
        self.wait_flag = True
        self.status_lb.setText("Для задания/редактирования сигнала воспользуйтесь кнопкой на МК")
 
    def stop_timer(self):
        self.wait_flag = False
        self.status_lb.setText("")
        self.start_btn.clicked.connect(self.start_generate)
        self.control_panel.setEnabled(True)
        self.start_btn.setEnabled(True)
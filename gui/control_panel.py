from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame, QRadioButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import sip

from gui import parameters_editor
import utils


class ControlPanel():
    def __init__(self, widget):
        self.widget = widget

        self.single_values_layout = None
        self.table_values_layout = None
        self.waveworm_frame = None
        self.values_frame = None

        self.initUI()
        self.initData()

    @property
    def layout(self):
        return self.__main_layout
    
    @property
    def frame(self):
        self.__main_frame = QFrame()
        self.__main_frame.setLayout(self.__main_layout)
        self.__main_frame.setFrameShape(QFrame.Panel)

        return self.__main_frame
    
    def initUI(self):
        self.waveworm_frame = self.get_waveworm_frame()
        self.values_frame = self.get_values_frame()
        
        self.__main_layout = QHBoxLayout()
        self.__main_layout.addWidget(self.waveworm_frame)
        self.__main_layout.addWidget(self.values_frame)

    def initData(self):
        pass

    def get_waveworm_frame(self):
        waveworm_lb = QLabel("Форма сигнала")
        rbtn1 = QRadioButton("Треугольный")
        rbtn2 = QRadioButton("Пилообразный")
        rbtn3 = QRadioButton("Прямоугольный")
        rbtn4 = QRadioButton("Шумоподобный")
        rbtn5 = QRadioButton("Произвольный")

        rbtn1.toggled.connect(self.change_waveform)
        rbtn2.toggled.connect(self.change_waveform)
        rbtn3.toggled.connect(self.change_waveform)
        rbtn4.toggled.connect(self.change_waveform)
        rbtn5.toggled.connect(self.change_waveform)

        rbtn2.setChecked(True)

        v_layout = QVBoxLayout()
        v_layout.addWidget(waveworm_lb)
        v_layout.addWidget(rbtn1)
        v_layout.addWidget(rbtn2)
        v_layout.addWidget(rbtn3)
        v_layout.addWidget(rbtn4)
        v_layout.addWidget(rbtn5)
        v_layout.addStretch()

        waveform_layout = QHBoxLayout()
        waveform_layout.addStretch()
        waveform_layout.addLayout(v_layout)
        waveform_layout.addStretch()

        waveworm_frame = QFrame()
        waveworm_frame.setLayout(waveform_layout)
        waveworm_frame.setFrameShape(QFrame.Panel)
        waveworm_frame.setFixedSize(486, 200)

        return waveworm_frame

    def get_values_frame(self):
        values_frame = QFrame()
        values_frame.setLayout(self.get_single_values_layout())
        values_frame.setFrameShape(QFrame.Panel)
        values_frame.setFixedSize(486, 200)

        return values_frame

    def get_single_values_layout(self):
        amplitude_lb = QLabel("Амплитуда")
        amplitude_input = utils.MyLineEdit()
        amplitude_input.setReadOnly(True)
        amplitude_input.setFixedSize(250, 30)
        amplitude_input.setText("4.8 В")
        amplitude_input.setAlignment(Qt.AlignRight) 
        amplitude_input.clicked.connect(self.change_values)

        frequency_lb = QLabel("Частота")
        frequency_input = utils.MyLineEdit()
        frequency_input.setReadOnly(True)
        frequency_input.setFixedSize(250, 30)
        frequency_input.setText("1000 Гц")
        frequency_input.setAlignment(Qt.AlignRight)
        frequency_input.clicked.connect(self.change_values)

        h_layout = QVBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(amplitude_lb)
        h_layout.addWidget(amplitude_input)
        h_layout.addStretch()
        h_layout.addWidget(frequency_lb)
        h_layout.addWidget(frequency_input)
        h_layout.addStretch()

        self.single_values_layout = QHBoxLayout()
        self.single_values_layout.addStretch()
        self.single_values_layout.addLayout(h_layout)
        self.single_values_layout.addStretch()

        return self.single_values_layout

    def get_table_values_layout(self):
        lb = utils.MyLabel("Таблица")
        lb.clicked.connect(self.change_values)

        h_layout = QVBoxLayout()
        h_layout.addWidget(lb)

        self.table_values_layout = QHBoxLayout()
        self.table_values_layout.addStretch()
        self.table_values_layout.addLayout(h_layout)
        self.table_values_layout.addStretch()

        return self.table_values_layout

    def change_waveform(self):
        if not self.waveworm_frame:
            return

        rbtn = self.widget.sender()
        if rbtn.isChecked():
            if rbtn.text() == "Произвольный":
                self.deleteLayout(self.values_frame.layout())
                self.values_frame.setLayout(self.get_table_values_layout())
            elif self.values_frame.layout() == self.table_values_layout:
                self.deleteLayout(self.values_frame.layout())
                self.values_frame.setLayout(self.get_single_values_layout())

    def change_values(self):
        if self.values_frame.layout() == self.table_values_layout:
            editot_title = "Параметры сигнала 1"
        else:
            editot_title = "Параметры сигнала"

        editor = parameters_editor.Editor(editot_title)

        editor.run()

    def deleteLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            sip.delete(layout)
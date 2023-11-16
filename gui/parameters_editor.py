from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWidget, QMessageBox, QDialog, QSlider, QLineEdit, QRadioButton

from config import frequency_dict


class Editor(QDialog):
    def __init__(self, editot_title):
        super().__init__()

        self.setWindowTitle(editot_title)
        # self.setFixedSize(QSize(1440, 810))
        self.setFixedSize(QSize(400, 250))

        self.need_waveforms = False if editot_title == "Параметры сигнала" else True
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

        QPushButton {
            border: 1px solid black;
            background-color: #FFFFFF;
            font-size: 12pt;
        }
        QPushButton:hover {
        /*    border: 2px solid black;   Change border color to red when hovered */
            background-color: #F0F0F0;
        }
        QPushButton:pressed {
            border: 2px solid black;  /* Change border color to blue when pressed */
        }
        """
        self.setStyleSheet(stylesheet)

        # self.setWindowIcon(QIcon(config.app_icon_path))

        self.initUI()
        self.initData()
    
    def initUI(self):
        amplitude_layout = self.get_amplitude_layout()
        frequency_layout = self.get_frequency_layout()

        parameters_layout = QHBoxLayout()
        parameters_layout.addLayout(amplitude_layout)
        parameters_layout.addLayout(frequency_layout)

        if self.need_waveforms:
            self.waveforms_layout = self.get_waveworm_layout()
            parameters_layout.addLayout(self.waveforms_layout)

        parameters_frame = QFrame()
        parameters_frame.setLayout(parameters_layout)
        parameters_frame.setFrameShape(QFrame.Panel)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setFixedHeight(30)
        cancel_btn.clicked.connect(self.stop)
        apply_btn = QPushButton("Применить")
        apply_btn.setFixedHeight(30)
        apply_btn.clicked.connect(self.apply)

        button_layout = QHBoxLayout()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(apply_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(parameters_frame)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def get_amplitude_layout(self):
        slider = QSlider(Qt.Orientation.Vertical)
        slider.setRange(11, 48)
        slider.setValue(11)
        slider.setSingleStep(1)
        slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        slider.valueChanged.connect(self.update_amplitude)

        self.amplitude_input = QLineEdit()
        self.amplitude_input.setReadOnly(True)
        self.amplitude_input.setFixedSize(70, 30)
        self.amplitude_input.setText(f"{slider.value() / 10.0} В")
        self.amplitude_input.setAlignment(Qt.AlignCenter) 

        h_lb_layout = QHBoxLayout()
        h_lb_layout.addStretch()
        h_lb_layout.addWidget(QLabel("Амплитуда"))
        h_lb_layout.addStretch()

        h_slider_layout = QHBoxLayout()
        h_slider_layout.addStretch()
        h_slider_layout.addWidget(slider)
        h_slider_layout.addStretch()

        h_input_layout = QHBoxLayout()
        h_input_layout.addStretch()
        h_input_layout.addWidget(self.amplitude_input)
        h_input_layout.addStretch()

        amplitude_layout = QVBoxLayout()
        amplitude_layout.addLayout(h_lb_layout)
        amplitude_layout.addLayout(h_slider_layout)
        amplitude_layout.addLayout(h_input_layout)

        return amplitude_layout

    def update_amplitude(self, value):
        self.amplitude_input.setText(f"{value / 10.0} В")

    def get_frequency_layout(self):
        self.frequency_list = list(frequency_dict)

        slider = QSlider(Qt.Orientation.Vertical)
        slider.setRange(self.frequency_list[0], self.frequency_list[-1])
        slider.setValue(self.frequency_list[0])
        slider.setSingleStep(1)
        slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        slider.valueChanged.connect(self.update_frequency)

        self.frequency_input = QLineEdit()
        self.frequency_input.setReadOnly(True)
        self.frequency_input.setFixedSize(70, 30)
        self.frequency_input.setText(f"{frequency_dict[slider.value()]} Гц")
        self.frequency_input.setAlignment(Qt.AlignCenter) 

        h_lb_layout = QHBoxLayout()
        h_lb_layout.addStretch()
        h_lb_layout.addWidget(QLabel("Частота"))
        h_lb_layout.addStretch()

        h_slider_layout = QHBoxLayout()
        h_slider_layout.addStretch()
        h_slider_layout.addWidget(slider)
        h_slider_layout.addStretch()

        h_input_layout = QHBoxLayout()
        h_input_layout.addStretch()
        h_input_layout.addWidget(self.frequency_input)
        h_input_layout.addStretch()

        frequency_layout = QVBoxLayout()
        frequency_layout.addLayout(h_lb_layout)
        frequency_layout.addLayout(h_slider_layout)
        frequency_layout.addLayout(h_input_layout)

        return frequency_layout

    def update_frequency(self, value):
        value = frequency_dict[value]
        if value >= 1000:
            value = value / 1000.0
            lb = "КГц"
        else:
            lb = "Гц"

        self.frequency_input.setText(f"{value} {lb}")

    def get_waveworm_layout(self):
        waveworm_lb = QLabel("Форма сигнала")
        rbtn1 = QRadioButton("Треугольный")
        rbtn2 = QRadioButton("Пилообразный")
        rbtn3 = QRadioButton("Прямоугольный")
        rbtn4 = QRadioButton("Шумоподобный")

        # rbtn1.toggled.connect(self.change_waveform)
        # rbtn2.toggled.connect(self.change_waveform)
        # rbtn3.toggled.connect(self.change_waveform)
        # rbtn4.toggled.connect(self.change_waveform)
        # rbtn5.toggled.connect(self.change_waveform)

        rbtn2.setChecked(True)

        v_layout = QVBoxLayout()
        v_layout.addWidget(waveworm_lb)
        v_layout.addStretch()
        v_layout.addWidget(rbtn1)
        v_layout.addWidget(rbtn2)
        v_layout.addWidget(rbtn3)
        v_layout.addWidget(rbtn4)
        v_layout.addStretch()

        waveform_layout = QHBoxLayout()
        waveform_layout.addStretch()
        waveform_layout.addLayout(v_layout)
        waveform_layout.addStretch()

        return waveform_layout


    def initData(self):
        pass

    def run(self):
        self.exec_()

    def stop(self):
        self.accept()
    
    def apply(self):
        self.stop()

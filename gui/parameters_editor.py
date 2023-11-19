from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWidget, QMessageBox, QDialog, QSlider, QLineEdit, QRadioButton

import config


class Editor(QDialog):
    def __init__(self, control_panel, editot_title, indx=None):
        super().__init__()

        self.setWindowTitle(editot_title)
        # self.setFixedSize(QSize(1440, 810))
        self.setFixedSize(QSize(400, 250))

        self.control_panel = control_panel
        self.indx = indx
        self.current_waveform = config.default["form"]
        self.need_waveforms = True if indx else False
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
        self.amplitude_slider = QSlider(Qt.Orientation.Vertical)
        self.amplitude_slider.setRange(11, 48)
        self.amplitude_slider.setValue(11)
        self.amplitude_slider.setSingleStep(1)
        self.amplitude_slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.amplitude_slider.valueChanged.connect(self.update_amplitude)

        self.amplitude_input = QLineEdit()
        self.amplitude_input.setReadOnly(True)
        self.amplitude_input.setFixedSize(70, 30)
        self.amplitude_input.setText(f"{self.amplitude_slider.value() / 10.0} В")
        self.amplitude_input.setAlignment(Qt.AlignCenter) 

        h_lb_layout = QHBoxLayout()
        h_lb_layout.addStretch()
        h_lb_layout.addWidget(QLabel("Амплитуда"))
        h_lb_layout.addStretch()

        h_slider_layout = QHBoxLayout()
        h_slider_layout.addStretch()
        h_slider_layout.addWidget(self.amplitude_slider)
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
        self.frequency_list = list(config.frequency_dict)

        self.frequency_slider = QSlider(Qt.Orientation.Vertical)
        self.frequency_slider.setRange(self.frequency_list[0], self.frequency_list[-1])
        self.frequency_slider.setValue(self.frequency_list[0])
        self.frequency_slider.setSingleStep(1)
        self.frequency_slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.frequency_slider.valueChanged.connect(self.update_frequency)

        self.frequency_input = QLineEdit()
        self.frequency_input.setReadOnly(True)
        self.frequency_input.setFixedSize(70, 30)
        self.frequency_input.setText(f"{config.frequency_dict[self.frequency_slider.value()]} Гц")
        self.frequency_input.setAlignment(Qt.AlignCenter) 

        h_lb_layout = QHBoxLayout()
        h_lb_layout.addStretch()
        h_lb_layout.addWidget(QLabel("Частота"))
        h_lb_layout.addStretch()

        h_slider_layout = QHBoxLayout()
        h_slider_layout.addStretch()
        h_slider_layout.addWidget(self.frequency_slider)
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
        value = config.frequency_dict[value]
        if value >= 1000:
            value = value / 1000.0
            lb = "КГц"
        else:
            lb = "Гц"

        self.frequency_input.setText(f"{value} {lb}")

    def get_waveworm_layout(self):
        waveworm_lb = QLabel("Форма сигнала")

        self.waveworm_layout = QVBoxLayout()
        self.waveworm_layout.addWidget(waveworm_lb)

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addLayout(self.waveworm_layout)
        h_layout.addStretch()

        return h_layout
    
    def change_waveform(self):
        item = self.sender()
        if not item or not item.isChecked():
            return

        for indx, val in config.forms.items():
            if item.text() == val:
                self.current_waveform = indx
                break

    def initData(self):
        if self.need_waveforms:
            table_values = self.control_panel.manager.get_table()
            single_values = table_values[str(self.indx)]

            self.waveworm_layout.addStretch()
            for i, val in config.forms.items():
                rbtn = QRadioButton(val)
                if i == single_values['form']:
                    rbtn.setChecked(True)
                    self.current_waveform = i
                rbtn.toggled.connect(self.change_waveform)
                self.waveworm_layout.addWidget(rbtn)

            self.waveworm_layout.addStretch()
        else:
            single_values = self.control_panel.manager.get_single()

        frequency = config.frequency_dict[single_values['frequency']]
        if frequency >= 1000:
            frequency = frequency / 1000.0
            lb = "КГц"
        else:
            lb = "Гц"

        self.frequency_slider.setValue(single_values['frequency'])
        self.frequency_input.setText(f"{frequency} {lb}")

        amplitude = single_values['amplitude'] / 10.0
        self.amplitude_slider.setValue(single_values['amplitude'])
        self.amplitude_input.setText(f"{amplitude} В")


    def run(self):
        self.exec_()

    def stop(self):
        self.accept()
    
    def apply(self):
        if self.need_waveforms:
            self.control_panel.manager.set_table_row(self.indx, self.amplitude_slider.value(), self.frequency_slider.value(), self.current_waveform)
            self.control_panel.initTableData()
        else:
            self.control_panel.manager.set_single(self.amplitude_slider.value(), self.frequency_slider.value())
            self.control_panel.initSingleData()

        self.stop()

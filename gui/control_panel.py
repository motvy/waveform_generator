from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame, QRadioButton, QTableWidget, QPushButton
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5 import sip, QtWidgets

from gui import parameters_editor
import utils
import config


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

    def setEnabled(self, a0: bool):
        self.waveworm_frame.setEnabled(a0)
        self.values_frame.setEnabled(a0)

    def initUI(self):
        self.waveworm_frame = self.get_waveworm_frame()
        self.values_frame = self.get_values_frame()
        
        self.__main_layout = QHBoxLayout()
        self.__main_layout.addWidget(self.waveworm_frame)
        self.__main_layout.addWidget(self.values_frame)

    def initData(self):
        self.manager = utils.ParametersManager()
        self.current_form = 1
        self.initSingleData()

    def initSingleData(self):
        single_values = self.manager.get_single()
        amplitude = single_values['amplitude'] / 10.0
        self.amplitude_input.setText(f"{amplitude} В")

        frequency = config.frequency_dict[single_values['frequency']]
        if frequency >= 1000:
            frequency = frequency / 1000.0
            lb = "КГц"
        else:
            lb = "Гц"
        self.frequency_input.setText(f"{frequency} {lb}")

    def initTableData(self):
        table_values = self.manager.get_table()

        if len(table_values) >= config.max_free_form_graphs or len(table_values) < 2:
            self.table_valaues.setColumnCount(4)
        else:
            self.table_valaues.setColumnCount(5)
            self.table_valaues.setHorizontalHeaderLabels(['Амплитуда', 'Частота', 'Форма', '', ''])
            hheader = self.table_valaues.horizontalHeader()
            hheader.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        
        self.table_valaues.setRowCount(0)

        for indx in sorted(table_values):
            self.table_valaues.setRowCount(self.table_valaues.rowCount() + 1)

            amplitude_input = utils.MyLineEdit()
            amplitude_input.setReadOnly(True)
            amplitude_input.setAlignment(Qt.AlignRight) 
            amplitude_input.clicked.connect(self.change_row_values)
            amplitude = table_values[indx]['amplitude'] / 10.0
            amplitude_input.setText(f"{amplitude} В")

            frequency_input = utils.MyLineEdit()
            frequency_input.setReadOnly(True)
            frequency_input.setAlignment(Qt.AlignRight)
            frequency_input.clicked.connect(self.change_row_values)
            frequency = config.frequency_dict[table_values[indx]['frequency']]
            if frequency >= 1000:
                frequency = frequency / 1000.0
                lb = "КГц"
            else:
                lb = "Гц"
            frequency_input.setText(f"{frequency} {lb}")

            form_input = utils.MyLineEdit()
            form_input.setReadOnly(True)
            form_input.setAlignment(Qt.AlignRight) 
            form_input.clicked.connect(self.change_row_values)
            form = table_values[indx]['form']
            form_input.setText(config.forms.get(form))

            self.table_valaues.setCellWidget(int(indx) - 1, 0, amplitude_input)
            self.table_valaues.setCellWidget(int(indx) - 1, 1, frequency_input)
            self.table_valaues.setCellWidget(int(indx) - 1, 2, form_input)

            if len(table_values) < 4:
                add_btn = QPushButton()
                add_btn.setIcon(QIcon(config.add_icon_path))
                add_btn.setIconSize(QSize(int(self.widget.width*0.04), int(self.widget.width*0.04)))
                add_btn.setStyleSheet('background: rgb(240, 240, 240); border: 0px;')
                add_btn.clicked.connect(self.add_row_value)
                self.table_valaues.setCellWidget(int(indx) - 1, 3, add_btn)

            if len(table_values) > 1:
                datete_btn = QPushButton()
                datete_btn.setIcon(QIcon(config.delete_icon_path))
                datete_btn.setIconSize(QSize(int(self.widget.width*0.04), int(self.widget.width*0.04)))
                datete_btn.setStyleSheet('background: rgb(240, 240, 240); border: 0px;')
                datete_btn.clicked.connect(self.del_row_value)
                self.table_valaues.setCellWidget(int(indx) - 1, 3 if len(table_values) >= config.max_free_form_graphs else 4, datete_btn)

    
    def add_row_value(self):
        btn = self.widget.sender()
        if not btn:
            return

        indx = self.get_table_item_indx(btn, 3)
        self.manager.add_table_row(indx)
        self.initTableData()

    def del_row_value(self):
        btn = self.widget.sender()
        if not btn:
            return

        indx = self.get_table_item_indx(btn, 4 if self.table_valaues.columnCount() == 5 else 3)
        self.manager.del_table_row(indx)
        self.initTableData()
    
    def change_row_values(self):
        item = self.widget.sender()

        indx = 1
        for i in range(self.table_valaues.rowCount()):
            if item in [self.table_valaues.cellWidget(i, col) for col in range(3)]:
                indx = i + 1
                for el in [self.table_valaues.cellWidget(i, col) for col in range(3)]:
                    el.setEnabled(False)
                break

        editot_title = f"Параметры сигнала {indx}"
        editor = parameters_editor.Editor(self, editot_title, indx)
        editor.run()
        for el in [self.table_valaues.cellWidget(indx-1, col) for col in range(3)]:
            el.setEnabled(True)

    def get_table_item_indx(self, item, col):
        indx = 0
        for i in range(self.table_valaues.rowCount()):
            if item == self.table_valaues.cellWidget(i, col):
                indx = i + 1
                break
        
        return indx

    def change_values(self):
        editot_title = "Параметры сигнала"
        editor = parameters_editor.Editor(self, editot_title)
        editor.run()

    def get_waveworm_frame(self):
        waveworm_lb = QLabel("Форма сигнала")

        afont = QFont()
        afont.setBold(True)
        waveworm_lb.setFont(afont)
  
        rbtn1 = QRadioButton("Треугольный")
        rbtn2 = QRadioButton("Пилообразный")
        rbtn3 = QRadioButton("Прямоугольный")
        rbtn4 = QRadioButton("Шумоподобный")
        # rbtn5 = QRadioButton("Произвольный")

        rbtn1.toggled.connect(self.change_waveform)
        rbtn2.toggled.connect(self.change_waveform)
        rbtn3.toggled.connect(self.change_waveform)
        rbtn4.toggled.connect(self.change_waveform)
        # rbtn5.toggled.connect(self.change_waveform)

        rbtn2.setChecked(True)

        v_layout = QVBoxLayout()
        v_layout.addStretch()
        v_layout.addWidget(waveworm_lb)
        v_layout.addWidget(rbtn1)
        v_layout.addWidget(rbtn2)
        v_layout.addWidget(rbtn3)
        v_layout.addWidget(rbtn4)
        # v_layout.addWidget(rbtn5)
        v_layout.addStretch()

        waveform_layout = QHBoxLayout()
        waveform_layout.addStretch()
        waveform_layout.addLayout(v_layout)
        waveform_layout.addStretch()

        waveworm_frame = QFrame()
        waveworm_frame.setLayout(waveform_layout)
        waveworm_frame.setFrameShape(QFrame.Panel)
        waveworm_frame.setMaximumHeight(int(0.2*self.widget.width))

        return waveworm_frame

    def get_values_frame(self):
        values_frame = QFrame()
        values_frame.setLayout(self.get_single_values_layout())
        values_frame.setFrameShape(QFrame.Panel)
        values_frame.setMaximumHeight(int(0.2*self.widget.width))

        return values_frame

    def get_single_values_layout(self):
        afont = QFont()
        afont.setBold(True)

        amplitude_lb = QLabel("Амплитуда")
        amplitude_lb.setFont(afont)
        self.amplitude_input = utils.MyLineEdit()
        self.amplitude_input.setReadOnly(True)
        self.amplitude_input.setFixedSize(int(0.25*self.widget.width), int(0.04*self.widget.height))
        self.amplitude_input.setAlignment(Qt.AlignRight) 
        self.amplitude_input.clicked.connect(self.change_values)

        frequency_lb = QLabel("Частота")
        frequency_lb.setFont(afont)
        self.frequency_input = utils.MyLineEdit()
        self.frequency_input.setReadOnly(True)
        self.frequency_input.setFixedSize(int(0.25*self.widget.width), int(0.04*self.widget.height))
        self.frequency_input.setAlignment(Qt.AlignRight)
        self.frequency_input.clicked.connect(self.change_values)

        h_layout = QVBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(amplitude_lb)
        h_layout.addWidget(self.amplitude_input)
        h_layout.addStretch()
        h_layout.addWidget(frequency_lb)
        h_layout.addWidget(self.frequency_input)
        h_layout.addStretch()

        self.single_values_layout = QHBoxLayout()
        self.single_values_layout.addStretch()
        self.single_values_layout.addLayout(h_layout)
        self.single_values_layout.addStretch()

        return self.single_values_layout

    def get_table_values_layout(self):
        afont = QFont()
        afont.setPointSize(12)
        afont.setBold(True)

        self.table_valaues = QTableWidget()
        self.table_valaues.setColumnCount(5)
        self.table_valaues.setHorizontalHeaderLabels(['Амплитуда', 'Частота', 'Форма', '', ''])

        self.table_valaues.verticalHeader().setVisible(False)
        hheader = self.table_valaues.horizontalHeader()
        hheader.setFont(afont)
        hheader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        hheader.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        hheader.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        hheader.setFocusPolicy(Qt.NoFocus)

        self.table_valaues.setFixedWidth(int(0.45*self.widget.width))

        item3 = self.table_valaues.horizontalHeaderItem(2)
        item3.setBackground(QColor(255, 0, 255))

        self.table_valaues.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_valaues.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.table_valaues.setFocusPolicy(Qt.NoFocus)

        v_layout = QVBoxLayout()
        v_layout.addStretch()
        v_layout.addWidget(self.table_valaues)
        v_layout.addStretch()

        self.table_values_layout = QHBoxLayout()
        self.table_values_layout.addStretch()
        self.table_values_layout.addLayout(v_layout)
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
                self.initTableData()
            elif self.values_frame.layout() == self.table_values_layout:
                self.deleteLayout(self.values_frame.layout())
                self.values_frame.setLayout(self.get_single_values_layout())
                self.initSingleData()
            
            for key, val in config.forms.items():
                if val == rbtn.text():
                    self.current_form = key
                    break
            else:
                self.current_form = 5
            
            self.widget.graph_canvas.doPlot(self.current_form)


    def change_values(self):
        if self.values_frame.layout() == self.table_values_layout:
            editot_title = "Параметры сигнала 1"
        else:
            editot_title = "Параметры сигнала"

        editor = parameters_editor.Editor(self, editot_title)

        editor.run()

        self.widget.graph_canvas.doPlot(self.current_form)

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
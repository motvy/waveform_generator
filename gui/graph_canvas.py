from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWidget, QMessageBox

import pyqtgraph as pg

class GraphCanvas():
    def __init__(self):
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
        self.__main_frame.setFixedHeight(520)

        return self.__main_frame
    
    def setEnabled(self, a0):
        self.__main_frame.setEnabled(a0)

    def initUI(self):
        self.__main_layout = QHBoxLayout()

        plot_graph = pg.PlotWidget()
        plot_graph.setBackground('#F0F0F0')
        plot_graph.getPlotItem().hideAxis('bottom')

        plot_graph.setLimits(xMin = -1, yMin = 0, xMax=257, yMax=5.2)

        plot_graph.plot([0, 50, 100, 150, 200, 256, 256], [0, 1, 2, 3, 4, 5, 0], pen={'color':'#59a83d', 'width': 2})

        self.__main_layout.addWidget(plot_graph)

    def initData(self):
        pass

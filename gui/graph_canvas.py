from PyQt5.QtWidgets import QHBoxLayout, QFrame

import pyqtgraph as pg
import numpy as np

import utils, config


class GraphCanvas():
    def __init__(self, widget):
        self.widget = widget
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
        # self.__main_frame.setFixedHeight(int(0.68*self.widget.height))

        return self.__main_frame
    
    def setEnabled(self, a0):
        self.__main_frame.setEnabled(a0)

    def initUI(self):
        self.__main_layout = QHBoxLayout()

        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setBackground('#F0F0F0')
        self.plot_graph.setMouseEnabled(x=False, y=False)
        self.plot_graph.getPlotItem().hideAxis('bottom')

        self.plot_graph.setLimits(xMin = -1, yMin = -0.1, xMax=255, yMax=5.1)

        self.__main_layout.addWidget(self.plot_graph)

    def initData(self):
        self.manager = utils.ParametersManager()

        self.current_plot = None
        self.doPlot(2)
    
    def doPlot(self, form):
        if self.current_plot:
            self.plot_graph.removeItem(self.current_plot)
        
        settings = self.manager.get_single()
        x_data = [i for i in range(0, 256)]
        
        form_name = config.forms.get(form, "Произвольный")
        if form_name == "Шумоподобный":
            self.plot_data = self.get_noise()
        elif form_name == "Прямоугольный":
            self.plot_data = self.get_rectangular()   
        elif form_name == "Пилообразный":
            self.plot_data = self.get_sawtooth()
        elif form_name == "Треугольный":
            self.plot_data = self.get_triangular()
        else:
            x_data = [0, 1, 2, 3, 4, 5, 5]
            self.plot_data = [0, 50, 100, 150, 200, 255, 0]

        self.plot_data = [int(y * (settings["amplitude"] / 50)) for y in self.plot_data]
        y_data = [y * 5 / 256 for y in self.plot_data]

        self.current_plot = self.plot_graph.plot(x_data, y_data, pen={'color':'#59a83d', 'width': 2})
    
    def getPlotData(self):
        return self.plot_data
    
    def get_noise(self):
        y = [0]
        for i in np.random.normal(0, 128, 255):
            if i < 0:
                i = -i
            if i > 256:
                i = 255
            
            y.append(i)
        
        return y

    def get_random(self):
        pass

    def get_triangular(self):
        return [i * 2 if i <= 127 else (255 - i)*2 for i in range(0, 256)]

    def get_rectangular(self):
        return [0 if i <= 127 else 255 for i in range(0, 256)]

    def get_sawtooth(self):
        return [i for i in range(0, 255)] + [0]


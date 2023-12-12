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

        self.plot_graph.setLimits(xMin = -1, yMin = -0.1, xMax=255.1, yMax=5.1)

        self.__main_layout.addWidget(self.plot_graph)

    def initData(self):
        self.manager = utils.ParametersManager()

        self.current_plot = None
        self.plot_data = 0
        self.current_frequency = None
        self.doPlot(1)
    
    def doPlot(self, form):
        if self.current_plot:
            self.plot_graph.removeItem(self.current_plot)

        self.form_dict = {
            1: self.get_triangular,
            2: self.get_sawtooth,
            3: self.get_rectangular,
            4: self.get_noise,
            5: self.get_free,
        }
        
        settings = self.manager.get_single()
        x_data = [i for i in range(0, 256)]
        
        form_name = config.forms.get(form, "Произвольный")
        if form == 5:
            settings = self.manager.get_table()
            self.current_frequency = settings['1']['frequency']
            self.plot_data = self.get_free(settings, x_data)
        else:
            self.current_frequency = settings['frequency']
            self.plot_data = self.form_dict.get(form)()
            self.plot_data = [int(y * (settings["amplitude"] / 50)) for y in self.plot_data]

        # if form_name == "Шумоподобный":
        #     self.plot_data = self.get_noise()
        #     self.plot_data = [int(y * (settings["amplitude"] / 50)) for y in self.plot_data]

        #     print(len(self.plot_data))
        # elif form_name == "Прямоугольный":
        #     self.plot_data = self.get_rectangular()  
        #     self.plot_data = [int(y * (settings["amplitude"] / 50)) for y in self.plot_data] 
        # elif form_name == "Пилообразный":
        #     self.plot_data = self.get_sawtooth()
        #     self.plot_data = [int(y * (settings["amplitude"] / 50)) for y in self.plot_data]
        # elif form_name == "Треугольный":
        #     self.plot_data = self.get_triangular()
        #     self.plot_data = [int(y * (settings["amplitude"] / 50)) for y in self.plot_data]
        # else:
        #     settings = self.manager.get_table()
        #     self.plot_data = self.get_free(settings, x_data)
        #     # x_data = [0, 1, 2, 3, 4, 5, 5]
        #     # self.plot_data = [0, 50, 50, 50, 50, 50, 0]

        y_data = [y * 5 / 256 for y in self.plot_data]

        self.current_plot = self.plot_graph.plot(x_data, y_data, pen={'color':'#59a83d', 'width': 2})
    
    def getPlotData(self):
        return self.plot_data
    
    def get_noise(self, length=256):
        y = [0]
        for i in np.random.normal(0, length // 2, length-1):
            if i < 0:
                i = -i
            if i > length:
                i = length
            
            y.append(i)
        
        return y

    def get_triangular(self, length=256):
        return [i * 2 if i <= length//2-1 else (length - 1 - i)*2 for i in range(0, length)]

    def get_rectangular(self, length=256):
        return [0 if i <= length//2-1 else length-1 for i in range(0, length)]

    def get_sawtooth(self, length=256):
        return [i for i in range(0, length-1)] + [0]
    
    def get_free(self, settings, x_data):
        l = len(settings)
        splited_x_data = np.array_split(np.array(x_data), l)
        result_y_data = []

        for key, val in settings.items():
            y_data = self.form_dict.get(val["form"])(len(splited_x_data[int(key)-1]))
            curr = [int(y * (val["amplitude"] / 50)) for y in y_data]
            result_y_data.extend(curr)
        # for i in range(l):
        #     y_data = self.form_dict.get(int(settings[str(i+1)]["form"]))(len(splited_x_data[i]))
        #     result_y_data.extend([int(y * (settings[str(i+1)]["amplitude"] / 50)) for y in y_data])

        return result_y_data



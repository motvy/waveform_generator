from PyQt5.QtWidgets import QLineEdit, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

import os
import json
import io

import config


class MyLineEdit(QLineEdit):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button()==Qt.LeftButton:
            self.clicked.emit()


class MyLabel(QLabel):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button()==Qt.LeftButton:
            self.clicked.emit()


class ParametersManager():
    __parameters_path = config.parameters_path

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super(ParametersManager, cls).__new__(cls, *args, **kwargs)
            cls.__instance()
        return cls.__instance

    def __call__(self):
        self.__parameters_conf = self.read(self.__parameters_path)
        self.__default_parameters = {
            "single_values": {
                "amplitude": config.default['amplitude'],
                "frequency": config.default['frequency']
            },
            "table_values": {
                "1": {
                    "amplitude": config.default['amplitude'],
                    "frequency": config.default['frequency'],
                    "form": config.default['form']
                }
            }
        }

        if not self.__parameters_conf:
            self.__parameters_conf = self.__default_parameters

    def __del__(self):
        self.save_parameters()

    def write(self, data):
        if data is None or self.__parameters_path is None: return False

        outtext = json.dumps(data)
        with io.open(self.__parameters_path, mode = 'w') as f:
            f.write(outtext)

        return True

    def read(self, jfile):
        result = dict()

        if self.__parameters_path is not None and os.path.exists(jfile):
            try:
                with io.open(jfile, mode = 'r') as f:
                    result = json.loads(f.read())
            except:
                pass

        return result

    def set_single(self, amplitude, frequency):
        self.__parameters_conf['single_values'] = {"amplitude": amplitude, "frequency": frequency}

    def set_table_row(self, indx, amplitude, frequency, form):
        self.__parameters_conf['table_values'][str(indx)] = {"amplitude": amplitude, "frequency": frequency, "form": form}
        for key, val in self.__parameters_conf['table_values'].items():
            self.__parameters_conf['table_values'][key][ "frequency"] = frequency

    
    def add_table_row(self, indx):
        if indx > len(self.__parameters_conf["table_values"]):
            indx = len(self.__parameters_conf["table_values"])

        for i in range(len(self.__parameters_conf["table_values"])+1, indx+1, -1):
            prev_vals = self.__parameters_conf['table_values'][str(i-1)]
            self.__parameters_conf['table_values'][str(i)] = {"amplitude": prev_vals["amplitude"], "frequency": prev_vals["frequency"], "form": prev_vals["form"]}
        
        self.__parameters_conf['table_values'][str(indx+1)] = self.__default_parameters['table_values']["1"]

    def del_table_row(self, indx):
        if str(indx) not in self.__parameters_conf['table_values']:
            raise Exception('Row with indx {} not exists in the table'.format(indx))
        
        for i in range(indx, len(self.__parameters_conf["table_values"])):
            self.__parameters_conf['table_values'][str(i)] = self.__parameters_conf['table_values'][str(i+1)]
        
        del self.__parameters_conf['table_values'][str(len(self.__parameters_conf["table_values"]))]

    def get_single(self):
        return self.__parameters_conf.get('single_values', self.__default_parameters.get('single_values'))

    def get_table(self):
        return self.__parameters_conf.get('table_values', self.__default_parameters.get('table_values'))

    def save_parameters(self):
        self.write(self.__parameters_conf)

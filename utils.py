from PyQt5.QtWidgets import QLineEdit, QAbstractSlider, QLabel
from PyQt5.QtCore import Qt, pyqtSignal


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

class MySlider(QAbstractSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lst = []
        self.indx= 0
        self._value = 0

    def stepEnabled(self):
        if self.indx == 0:
            return QAbstractSlider.StepUpEnabled
        elif self.indx == len(self.lst)-1:
            return QAbstractSlider.StepDownEnabled
        else:
            return QAbstractSlider.StepUpEnabled | QAbstractSlider.StepDownEnabled

    def stepBy(self, p_int):
        num = self.indx + p_int
        if num < len(self.lst):
            self.indx = num
            self.value = self.lst[self.indx]
        else:
            pass

    def setRange(self, lst):
        self.lst = lst
        self.indx = 0
        self.value = self.lst[self.indx]
        # self.lineEdit().setText(str(lst[self.indx]))
    
    def value(self):
        return self.value

    def setValue(self, value):
        self.indx = self.lst.index(value) if value in self.lst else 0
        self.value = self.lst[self.indx]
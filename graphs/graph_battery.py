import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

class graph_battery(pg.PlotItem):
    
    def __init__(self, parent=None, name=None, labels=None, title='Nivel Bateria', viewBox=None, axisItems=None, enableMenu=True, font = None,**kargs):    
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)

        self.hideAxis('bottom')
        self.hideAxis('left')
        self.invertX(False)
        self.invertY(True)
        self.proxy = QtWidgets.QGraphicsProxyWidget()
        self.label = QLabel()
        self.label.setFont(QFont('Arial', 10))
        self.label.setStyleSheet("width: 100%;margin-right: 5px;margin-left: 5px;color: white;background-color: rgb(33, 33, 33);")
        self.label.setText("100%")
        self.proxy.setWidget(self.label)
        if font != None:
            self.label.setFont(font)
        self.addItem(self.proxy)

    def update(self, value):
        self.label.setText("")
        battery = round(abs(int(value)), 0)        
        self.label.setText(str(battery) + '%')
import pyqtgraph as pg
import numpy as np

class graph_coordinates(pg.PlotItem):
        
    def __init__(self, parent=None, name=None, labels=None, title='Coordenadas', viewBox=None, axisItems=None, enableMenu=True, font = None,**kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)

        self.hideAxis('bottom')
        self.hideAxis('left')
        self.hideButtons()
        self.enableAutoScale()
        self.text = pg.TextItem("lat: 230.9870\nlong: 123.8888", anchor=(0.5, 0.5), color="w")
        if font != None:
            self.text.setFont(font)
        self.addItem(self.text)


    def update(self, value):
        #self.time_text.setText('')
        #self.tiempo = round(abs(int(value)) / 1000, 2)
        #print(self.tiempo)
        self.text.setText('4999')
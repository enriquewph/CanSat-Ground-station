import pyqtgraph as pg
import numpy as np

class graph_co2(pg.PlotItem):

    def __init__(self, parent=None, name=None, labels=None, title='Nivel de CO2', viewBox=None, axisItems=None, enableMenu=True, **kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.co2_plot = self.plot(pen=(29, 185, 84))
        self.co2_data = np.linspace(0, 0, 30)
        self.ptr1 = 0

    def update(self, value):
        self.co2_plot, self.co2_data,  self.ptr1
        self.co2_data[:-1] = self.co2_data[1:]
        self.co2_data[-1] = float(value)
        self.ptr1 += 1
        self.co2_plot.setData(self.co2_data)
        self.co2_plot.setPos(self.ptr1, 0)
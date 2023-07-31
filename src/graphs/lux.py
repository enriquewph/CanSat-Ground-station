import pyqtgraph as pg
import numpy as np

class graph_lux(pg.PlotItem):

    def __init__(self, parent=None, name=None, labels=None, title='Luminosidad [Lux]', viewBox=None, axisItems=None, enableMenu=True, **kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.lux_plot = self.plot(pen=(29, 185, 84))
        self.lux_data = np.linspace(0, 0, 30)
        self.ptr1 = 0

        #disable mouse 
        self.setMouseEnabled(x=False, y=False)
        self.hideButtons()
        
        
    def update(self, value):
        self.lux_plot, self.lux_data,  self.ptr1
        self.lux_data[:-1] = self.lux_data[1:]
        self.lux_data[-1] = float(value)
        self.ptr1 += 1
        self.lux_plot.setData(self.lux_data)
        self.lux_plot.setPos(self.ptr1, 0)
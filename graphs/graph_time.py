import pyqtgraph as pg


class graph_time(pg.PlotItem):
        
    def __init__(self, parent=None, name=None, labels=None, title='Tiempo misión (s)', viewBox=None, axisItems=None, enableMenu=True, font = None,**kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)

        self.hideAxis('bottom')
        self.hideAxis('left')
        self.hideButtons()
        self.enableAutoScale()
        self.time_text = pg.TextItem("0.0", anchor=(0.5, 0.5), color="w")
        if font != None:
            self.time_text.setFont(font)
        self.addItem(self.time_text)


    def update(self, value):
        self.time_text.setText('')
        self.tiempo = round(abs(int(value)) / 1000, 2)
        self.time_text.setText(str(self.tiempo))
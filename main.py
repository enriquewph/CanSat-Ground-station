import sys
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
from PIL import Image
from numpy import angle, asarray
from communication import Communication
from dataBase import data_base
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from graphs.graph_acceleration import graph_acceleration
from graphs.graph_altitude import graph_altitude
from graphs.graph_battery import graph_battery
from graphs.graph_free_fall import graph_free_fall
from graphs.graph_gyro import graph_gyro
from graphs.graph_pressure import graph_pressure
from graphs.graph_speed import graph_speed
from graphs.graph_temperature import graph_temperature
from graphs.graph_time import graph_time


pg.setConfigOption('background', (33, 33, 33))
pg.setConfigOption('foreground', (197, 198, 199))
# Interface variables
app = QtWidgets.QApplication(sys.argv)
view = pg.GraphicsView()
Layout = pg.GraphicsLayout()
view.setCentralItem(Layout)
view.show()
view.setWindowTitle('Monitoreo de misión mCALCAN')
view.resize(1200, 700)

# declare object for serial Communication
ser = Communication()
# declare object for storage in CSV
data_base = data_base()
# Fonts for text items
font = QtGui.QFont()
font.setPixelSize(90)

# buttons style
style = "background-color:rgb(29, 185, 84);color:rgb(0,0,0);font-size:14px;"


# Declare graphs
# Button 1
proxy = QtWidgets.QGraphicsProxyWidget()
save_button = QtWidgets.QPushButton('Guardar datos')
save_button.setStyleSheet(style)
save_button.clicked.connect(data_base.start)
proxy.setWidget(save_button)

# Button 2
proxy2 = QtWidgets.QGraphicsProxyWidget()
end_save_button = QtWidgets.QPushButton('Stop storage')
end_save_button.setStyleSheet(style)
end_save_button.clicked.connect(data_base.stop)
proxy2.setWidget(end_save_button)

# Altitude graph
altitude = graph_altitude()
# Speed graph
speed = graph_speed()
# Acceleration graph
acceleration = graph_acceleration()
# Gyro graph
gyro = graph_gyro()
# Pressure Graph
pressure = graph_pressure()
# Temperature graph
temperature = graph_temperature()
# Time graph
time = graph_time(font=font)
# Battery graph
battery = graph_battery(font=font)
# Free fall graph
free_fall = graph_free_fall(font=font)


## Setting the graphs in the layout 

# Title at top
text = """
Estación terrena de la misión mCALCAN - Desarrollo de<br>
los alumnos del Instituto técnico salesiano Villada 
"""
Layout.addLabel('mCALCAN', colspan=6, size='18pt')
Layout.addLabel(text, colspan=6)
Layout.nextRow()

# Buttons
lb = Layout.addLayout(colspan=21)
lb.addItem(proxy)
lb.nextCol()
lb.addItem(proxy2)
Layout.nextRow()

l1 = Layout.addLayout(colspan=60, rowspan=2)
l11 = l1.addLayout(rowspan=1, border=(83, 83, 83))
l11.addLabel('Misión Primaria', size='15pt', angle=-90)

# Altitude, temperature, pressure 
l11.addItem(temperature)
l11.addItem(altitude)
l11.addItem(pressure)
l1.nextRow()

# Acceleration, gyro, speed 
l12 = l1.addLayout(rowspan=1, border=(83, 83, 83))
l12.addLabel('Misión Secundaria', size='15pt', angle=-90)
l12.addItem(acceleration)
l12.addItem(gyro)
l12.addItem(speed)

# Time, battery and free fall graphs
l2 = Layout.addLayout(border=(83, 83, 83), colspan=1)
l2.setFixedWidth(200)
l2.addItem(time)
l2.nextRow()
l2.addItem(battery)
l2.nextRow()
l2.addItem(free_fall)

# you have to put the position of the CSV stored in the value_chain list
# that represent the date you want to visualize
def update():
    try:
        value_chain = []
        value_chain = ser.getData()
        print(value_chain)
        altitude.update(value_chain[1])
        speed.update(value_chain[8], value_chain[9], value_chain[10])
        time.update(value_chain[0])
        acceleration.update(value_chain[8], value_chain[9], value_chain[10])
        gyro.update(value_chain[5], value_chain[6], value_chain[7])
        pressure.update(value_chain[4])
        temperature.update(value_chain[3])
        free_fall.update(value_chain[2])
        data_base.guardar(value_chain)
    except IndexError:
        print('starting, please wait a moment')


if(ser.isOpen()) or (ser.dummyMode()):
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(500)
else:
    print("something is wrong with the update call")
# Start Qt event loop unless running in interactive mode.

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()

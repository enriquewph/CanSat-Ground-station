from email import header
from email.base64mime import header_length
import sys
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
from PIL import Image
from numpy import angle, asarray
from communication import Communication
from dataBase import data_base
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from graphs.graph_acceleration import graph_acceleration
from graphs.graph_altitude import graph_altitude
from graphs.graph_battery import graph_battery
from graphs.graph_free_fall import graph_free_fall
from graphs.graph_gyro import graph_gyro
from graphs.graph_pressure import graph_pressure
from graphs.graph_speed import graph_speed
from graphs.graph_temperature import graph_temperature
from graphs.graph_time import graph_time
from graphs.graph_humidity import graph_humidity
from graphs.graph_co2 import graph_co2
from graphs.graph_coordinates import graph_coordinates
from pprint import pprint



pg.setConfigOption('background', (33, 33, 33))
pg.setConfigOption('foreground', (197, 198, 199))

# Interface variables
app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet('QLabel{color: #fff;} QPushButton{background-color: #000; color: #fff}')
view = pg.GraphicsView()
main = QtWidgets.QMainWindow()
main.setStyleSheet("background-color: rgb(33, 33, 33);")
main_layout = QVBoxLayout()

# header 
header_layout = QHBoxLayout()
header_title = QLabel()
header_title.setFont(QFont('Arial', 16))
header_title.setText('mCALCAN')
header_subtitle = QLabel()
text = """
Estación terrena de la misión mCALCAN - Desarrollo de<br>
los alumnos del Instituto técnico salesiano Villada 
"""
header_subtitle.setText(text)
header_layout.addWidget(header_title)
header_layout.addWidget(header_subtitle)
header_widget = QWidget()
header_widget.setLayout(header_layout)

# Add main layout widgets 
main_layout.addWidget(header_widget)
main_layout.addWidget(view)
main_widget = QWidget()
main_widget.setLayout(main_layout)
main.setCentralWidget(main_widget)
main.show()
Layout = pg.GraphicsLayout()
view.setCentralItem(Layout)
main.setWindowTitle('Monitoreo de misión mCALCAN')
main.resize(1280, 720)

# declare object for serial Communication
ser = Communication()
# declare object for storage in CSV
data_base = data_base()
# Fonts for text items
font = QtGui.QFont()
font.setPixelSize(50)
font2 = QtGui.QFont()
font2.setPixelSize(30)
font3 = QtGui.QFont()
font3.setPixelSize(18)

# buttons style
style = "background-color:rgb(29, 185, 84);color:rgb(0,0,0);font-size:18px;"
style1 = "background-color:rgb(242, 69, 69);color:rgb(0,0,0);font-size:18px;"
style2 = "background-color:rgb(216, 220, 76);color:rgb(0,0,0);font-size:18px;"

# Declare graphs
# Button Start mission 
proxy0 = QtWidgets.QGraphicsProxyWidget()
start_button = QtWidgets.QPushButton('Iniciar Misión')
start_button.setStyleSheet(style)
start_button.clicked.connect(data_base.mission_start)
proxy0.setWidget(start_button)

# Button End mission 
proxy1 = QtWidgets.QGraphicsProxyWidget()
end_button = QtWidgets.QPushButton('Finalizar Misión')
end_button.setStyleSheet(style1)
end_button.clicked.connect(data_base.mission_stop)
proxy1.setWidget(end_button)

# Button save
proxy2 = QtWidgets.QGraphicsProxyWidget()
save_button = QtWidgets.QPushButton('Guardar datos')
save_button.setStyleSheet(style)
save_button.clicked.connect(data_base.start)
proxy2.setWidget(save_button)

# Button stop
proxy3 = QtWidgets.QGraphicsProxyWidget()
end_save_button = QtWidgets.QPushButton('Detener datos')
end_save_button.setStyleSheet(style1)
end_save_button.clicked.connect(data_base.stop)
proxy3.setWidget(end_save_button)

# Input location
proxy_loc = QtWidgets.QGraphicsProxyWidget()
flo = QFormLayout()
longitude = QLineEdit()
longitude.setStyleSheet("background-color: rgb(33, 33, 33);")
latitude = QLineEdit()
latitude.setStyleSheet("background-color: rgb(33, 33, 33);")
flo.addRow("Longitud", longitude)
flo.addRow("Latitud", latitude)
set_pos_button = QtWidgets.QPushButton('Definir aterrizaje')
set_pos_button.setStyleSheet(style2)
set_pos_button.clicked.connect(data_base.stop)
flo.addRow(set_pos_button)
form = QWidget()
form.setStyleSheet("background-color: rgb(33, 33, 33);")
form.setLayout(flo)
proxy_loc.setWidget(form)

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
# Humidity graph
humidity = graph_humidity()
# CO2 graph
co2 = graph_co2()
# Coordinate graph
coordinates = graph_coordinates(font=font3)


## Setting the graphs in the layout 

# Buttons
lb = Layout.addLayout(colspan=21)
lb.addItem(proxy0)
lb.nextCol()
lb.addItem(proxy1)
lb.nextCol()
lb.addItem(proxy2)
lb.nextCol()
lb.addItem(proxy3)
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
l12.addItem(humidity)
l12.addItem(co2)

# Time, battery and free fall graphs
l2 = Layout.addLayout(border=(83, 83, 83), colspan=1)
l2.setFixedWidth(250)
l2.addItem(proxy_loc)
l2.nextRow()
l2.addItem(battery)
l2.nextRow()
l2.addItem(coordinates)
l2.nextRow()
l2.addItem(time)
l2.nextRow()
l2.addItem(free_fall)

# you have to put the position of the CSV stored in the value_chain list
# that represent the date you want to visualize
def update(data):
    try:
        value_chain = []
        value_chain = data
        print(value_chain)
        altitude.update(value_chain[1])
        speed.update(value_chain[8], value_chain[9], value_chain[10])
        time.update(value_chain[0])
        acceleration.update(value_chain[8], value_chain[9], value_chain[10])
        gyro.update(value_chain[5], value_chain[6], value_chain[7])
        pressure.update(value_chain[4])
        temperature.update(value_chain[3])
        free_fall.update(value_chain[2])
        humidity.update(value_chain[11])
        co2.update(value_chain[12])
        coordinates.update(value_chain[13], value_chain[14])
        battery.update(value_chain[15])
        data_base.guardar(value_chain)
    except IndexError:
        print('starting, please wait a moment')

def getCommand():
    command = ser.getCommand()
    if(command):
        if(command.type == 1 and \
            command.operation == 1 and \
            command.code == 5):
            update(command.data)

if(ser.isOpen()) or (ser.dummyMode()):
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(getCommand)
    timer.start(100)
else:
    print("something is wrong with the update call")
# Start Qt event loop unless running in interactive mode.

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()

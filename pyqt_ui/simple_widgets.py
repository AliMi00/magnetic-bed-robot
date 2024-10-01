import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import(
QApplication, 
QListWidget, 
QMainWindow, 
QLineEdit,       # page 59
QComboBox,
QSpinBox,
QSlider,        # page 61
QDial,          # page 67
) 

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("My App")


    widget = QDial()
    widget.setRange(-10, 100)
    widget.setSingleStep(1)
    widget.valueChanged.connect(self.value_changed)
    widget.sliderMoved.connect(self.slider_position)
    widget.sliderPressed.connect(self.slider_pressed)
    widget.sliderReleased.connect(self.slider_released)



    self.setCentralWidget(widget)


  def value_changed(self, i):  #i is a QListItem
    print(i)

  def slider_position(self, p):
    print("position", p)

  def slider_pressed(self):
    print("Pressed!")

  def slider_released(self):
    print("Released")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
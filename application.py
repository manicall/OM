import sys
from turtle import width
import numpy as np

from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib import pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class FigCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(projection='3d')
        super().__init__(self.figure)

class InputBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('Построение графика')
        self.resize(100, 100)
        self.wparent = parent
        self.main_frame = QtWidgets.QVBoxLayout()
        self.range_box = QtWidgets.QHBoxLayout()
        
        self.rx_line = self.get_r_line("rx")
        self.ry_line = self.get_r_line("ry")
          
        create_button = QtWidgets.QPushButton('Создать график')
        create_button.clicked.connect(self.create_plo)
        self.range_box.addWidget(create_button)
        
        self.main_frame.addLayout(self.range_box)  
        self.main_frame.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
     
        self.setLayout(self.main_frame)
        
    def get_r_line(self, lable_text):
        self.range_box.addWidget(QtWidgets.QLabel(lable_text))
        r_line = QtWidgets.QLineEdit()
        self.range_box.addWidget(r_line)
        
        return r_line
    
    def input_show(self):
        self.show()
        
    def create_plo(self):
        f = ""
        try:
            f = "rx"; rx = int(self.rx_line.text())
            f = "ry"; ry = int(self.ry_line.text())
            self.create_plot(rx, ry)
            self.resize(600, 400)
        except:
            QtWidgets.QMessageBox.critical(self, "Ошибка ввода", f"{f}: Ожидалось число")
    
    def create_plot(self, rx = 50, ry = 50):
        canvas = FigCanvas()
        mpl_toolbar = NavigationToolbar(canvas)
        
        f = lambda x1, x2: (x1 - 3) ** 2 + (5 - x2) ** 2
        x, y = np.meshgrid(np.linspace(-rx, rx, 100), 
                            np.linspace(-ry, ry, 100))
        z = f(x, y)
        canvas.axes.plot_surface(x, y, z)
        
        canvas_layout = QtWidgets.QVBoxLayout()
        canvas_layout.addWidget(mpl_toolbar)
        canvas_layout.addWidget(canvas)
        
        self.main_frame.addLayout(canvas_layout)
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        self.input_box = InputBox(self)
        
        menu_bar = self.menuBar()
        menu_bar.addAction("Создать график", self.input_box.input_show)
        
        self.main_frame = QtWidgets.QWidget()
        self.main_layout = None
        
        
        
        self.setCentralWidget(self.main_frame) 
        self.show()
    
    def create_plot(self, rx = 50, ry = 50):
        
        self.main_frame.setLayout(self.main_layout)

        
class App(QtWidgets.QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = MainWindow()
        self.window.show()
        
if __name__ == "__main__":
    app = App()
    sys.exit(app.exec())
    
    
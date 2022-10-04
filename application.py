import sys
import numpy as np
import sympy as sp
import equals as e
import traceback

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from matplotlib import pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from fastest_descent import FastDescent

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
        
        self.init_UI()          

    def init_UI(self):     
        self.main_frame = QtWidgets.QVBoxLayout()
        
        self.main_frame.addLayout(self.get_range_box())  
        self.main_frame.addLayout(self.get_canvas_layout())
        self.main_frame.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.main_frame)
    
    def get_range_box(self):
        range_box = QtWidgets.QHBoxLayout()

        self.rx_line = QtWidgets.QLineEdit('50')
        self.ry_line = QtWidgets.QLineEdit('50')
        
        range_box.addWidget(QtWidgets.QLabel('rx'))
        range_box.addWidget(self.rx_line)
        
        range_box.addWidget(QtWidgets.QLabel('ry'))
        range_box.addWidget(self.ry_line)
        
        create_button = QtWidgets.QPushButton('Создать график')
        create_button.clicked.connect(self.init_plot)
        range_box.addWidget(create_button)
        
        return range_box
    
    def get_canvas_layout(self):
        canvas_layout = None
        self.canvas = FigCanvas()
        mpl_toolbar = NavigationToolbar(self.canvas)
        
        canvas_layout = QtWidgets.QVBoxLayout()
        canvas_layout.addWidget(mpl_toolbar)
        canvas_layout.addWidget(self.canvas)
        
        return canvas_layout
    
    def init_plot(self):
        f = ""
        try:
            f = "rx"; rx = float(self.rx_line.text())
            f = "ry"; ry = float(self.ry_line.text())
            self.create_plot(rx, ry)
            self.resize(600, 400)
        except Exception as err:
            print(f"ErrorMessage: {err}")
            QtWidgets.QMessageBox.critical(self, "Ошибка ввода", f"{f}: Ожидалось число")
    
    def create_plot(self, rx = 50, ry = 50):
        equal = self.wparent.get_equal()
        f = sp.lambdify(['x1', 'x2'], equal)
        x, y = np.meshgrid(np.linspace(-rx, rx, 100), np.linspace(-ry, ry, 100))
        z = f(x, y)
        
        plt.cla()
        self.canvas.axes.plot_surface(x, y, z)
        self.canvas.draw()

    def ishow(self): 
        self.init_plot()
        self.show()
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Построение графика')
        self.resize(600, 400)
        
        self.init_UI()
        
    def init_UI(self):
        self.input_box = InputBox(self)
        self.table_view = QtWidgets.QTableView()
        
        self.create_menu()
        
        main_frame = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        
        main_layout.addLayout(self.get_equal_layout())
        main_layout.addWidget(self.table_view)
        
        main_frame.setLayout(main_layout)
        self.setCentralWidget(main_frame) 
        self.show()
  
    def create_menu(self):
        menu_bar = self.menuBar()
        menu_bar.addMenu("Методы оптимизации") \
            .addAction('Наискорейший спуск', self.use_fast_descent)
        menu_bar.addAction("Создать график", self.input_box.ishow)

    def get_equal_layout(self):
        self.cb_equals = QtWidgets.QComboBox()
        self.cb_equals.addItems(e.Equals.equals.values())
        
        self.x1 = QtWidgets.QLineEdit('-2')
        self.x2 = QtWidgets.QLineEdit('-2')
        self.h = QtWidgets.QLineEdit('0.1')
        self.E = QtWidgets.QLineEdit('0.01')
        
        equal_layout = QtWidgets.QHBoxLayout()
        self.add_widget_with_label(equal_layout, self.cb_equals, 'Текущее уравнение')
        self.add_widget_with_label(equal_layout, self.x1, 'x1')
        self.add_widget_with_label(equal_layout, self.x2, 'x2')
        self.add_widget_with_label(equal_layout, self.h, 'h')
        self.add_widget_with_label(equal_layout, self.E, 'E')
        
        equal_layout.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                  Qt.AlignmentFlag.AlignTop)
        
        return equal_layout

    def add_widget_with_label(self, layout, widget, label_text):
        layout.addWidget(QtWidgets.QLabel(label_text))
        layout.addWidget(widget)
    
    def get_model(self):
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(
            ['x', 'y', 'df/dx', 'df/dy', 'h', 'f(x,y)']
        )
        return model
    
    def use_fast_descent(self):
        try:
            f = 'x1'; x1 = float(self.x1.text())
            f = 'x2'; x2 = float(self.x2.text())
            f = 'h'; h = float(self.h.text())
            f = 'E'; E = float(self.E.text())
            result = FastDescent.get_result(self.get_equal(), [[x1], [x2]], h, E)
            self.set_result(result)

        except OverflowError:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(self, "Ошибка переполнения", 
                                           f"Не удалось выполнить оптимизацию")
        except ValueError:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(self, "Ошибка ввода",
                                           f"{f}: Ожидалось число")
            
    def get_equal(self):
        return self.cb_equals.currentText()

    def set_result(self, result):
        model = self.get_model()
        for i in range(len(result)):
            for j in range(len(result[i])):
                model.setItem(i, j, QtGui.QStandardItem(str(result[i][j])))
        self.table_view.setModel(model)

class App(QtWidgets.QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = MainWindow()
        self.window.show()
        
if __name__ == "__main__":
    app = App()
    sys.exit(app.exec())
    
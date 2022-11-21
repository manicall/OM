import sys
import numpy as np
import sympy as sp
from PyQt5 import QtWidgets, QtGui, QtCore
from table_widgets import InputTableWidget, OutputTableWidget
from scipy_solver import ScipySolver
from simplex import simplex
        
class App(QtWidgets.QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = MainWindow()
        self.window.show()

class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        
          
        self.tableInput = InputTableWidget()
        
        self.tableOutput = OutputTableWidget(self.tableInput)    
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.tableInput)
        main_layout.addWidget(self.tableOutput)
        
        self.setLayout(main_layout)


class MainWindow(QtWidgets.QMainWindow):    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение оптимизационной задачи")
        self.resize(900, 400)
        
        self.widget = CentralWidget(self)

        self.initMenu()
        
        self.setCentralWidget(self.widget) 
        
    def initMenu(self):
        menu_bar = self.menuBar()
        solution_menu = menu_bar.addMenu("Решить")
        solution_menu.addAction("Симплексный метод", self.solve_my)
        solution_menu.addAction("SciPy оптимизация", self.solve_scipy)
        
        table_menu = menu_bar.addMenu('Столбец таблицы')
        table_menu.addAction("Добавить столбец", self.widget.tableInput.addCol)
        table_menu.addAction("Удалить столбец", self.widget.tableInput.delCol)
        
        table_menu = menu_bar.addMenu('Строка таблицы')
        table_menu.addAction("Добавить строку", self.widget.tableInput.addRow)
        table_menu.addAction("Удалить строку", self.widget.tableInput.delRow)
        
    def solve_my(self):
        table = self.widget.tableInput
        a, b, c, signs = table.get_A_ub(), table.get_b_ub(), table.get_c(), table.get_signs()
        
        self.widget.tableOutput.fill(simplex(a, b, c, signs), table)
    
    def solve_scipy(self):
        max = True
        ScipySolver.scipy_solve(self.widget.tableInput, max)
    
if __name__ == "__main__":
    app = App()
    app.setStyle("fusion")
    sys.exit(app.exec())
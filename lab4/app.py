import sys

from PyQt5 import QtWidgets
from central_widget import CentralWidget
from frankwolf import frankwolf
   
class App(QtWidgets.QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = MainWindow()
        self.window.show()

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
        menu_bar.addAction("Метод аппроксимации Фогеля", self.solve_my)
        
    def solve_my(self):
        table = self.widget.tableInput
        a, b, c = table.get_A_ub(), table.get_b_ub(), table.get_c(), 
        
        #self.widget.tableOutput.fill(vogel_approximation(a, b, c), table)
    
if __name__ == "__main__":
    app = App()
    app.setStyle("fusion")
    sys.exit(app.exec())
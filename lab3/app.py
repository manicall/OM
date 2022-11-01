from numbers import Rational
import sys
import numpy as np
import sympy as sp
from PyQt5 import QtWidgets, QtGui
from scipy.optimize import linprog	
from vogel_approximation import vogel_approximation

class ScipySolver:
    @classmethod
    def scipy_solve(self, max = False):
        '''решает задачу оптимизации'''
        model = self.model
        
        try:
            c = [-i for i in model.get_c()] if max else model.get_c()
            A_ub = model.get_A_ub()
            b_ub = model.get_b_ub()
        except ValueError:
            mbox = QtWidgets.QMessageBox("Некоректные данные")
            mbox.setText()
            mbox.exec()
            return          
        
        solution = linprog(c, A_ub, b_ub)
       
        mbox = QtWidgets.QMessageBox()  
        text = ""
        try:
            for i in enumerate(solution['x']):
                text += f"x{i[0]} = {(i[1])}\n"
            # оптимальное (минимальное) значение функции
            text += "\nF = " 
            text += str(solution['fun']) if not max else str(-solution['fun'])
            mbox.setText(text)
        except:
            mbox.setText(solution.message)
        mbox.exec()

    @classmethod
    def set_model(self, model):
        self.model = model

class App(QtWidgets.QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = Window()
        self.window.show()

class CentralWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
             
        self.inputModel = InputModel()
        self.outputModel = OutputModel(self.inputModel)
        
        input_table_view = TableView(self.inputModel)
        input_table_view.setMaximumHeight(200)
        
        output_table_view = TableView(self.outputModel)
        
        ScipySolver.set_model(input_table_view.get_model())
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(input_table_view)
        main_layout.addWidget(output_table_view)
        
        self.setLayout(main_layout)

class Window(QtWidgets.QMainWindow):    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение оптимизационной задачи")
        self.resize(1200, 400)
        
        self.widget = CentralWidget()

        self.initMenu()
        
        self.setCentralWidget(self.widget) 
        
    def initMenu(self):
        menu_bar = self.menuBar()
        menu_bar.addAction("Метод аппроксимации Фогеля", self.solve_my)
        #solution_menu.addAction("SciPy оптимизация", self.solve_scipy)
        
        # table_menu = menu_bar.addMenu('Столбец таблицы')
        # table_menu.addAction("Добавить столбец", self.widget.inputModel.addCol)
        # table_menu.addAction("Удалить столбец", self.widget.inputModel.delCol)
        
        # table_menu = menu_bar.addMenu('Строка таблицы')
        # table_menu.addAction("Добавить строку", self.widget.inputModel.addRow)
        # table_menu.addAction("Удалить строку", self.widget.inputModel.delRow)
        
    def solve_my(self):
        model = self.widget.inputModel
        a, b, c = model.get_a(), model.get_b(), model.get_c()
        
        self.widget.outputModel.fill(vogel_approximation(a, b, c), model)

        
class TableView(QtWidgets.QTableView):
    def __init__(self, model):
        super().__init__()
        
        self.model = model
        self.setModel(self.model)
        
        # установка границ для заголовков
        self.horizontalHeader().setStyleSheet(self.get_header_style())               
        self.verticalHeader().setStyleSheet(self.get_header_style())
    
    def get_header_style(self): 
        return '''
        QHeaderView::section {
            border: none;
            border-bottom: 1px solid gray;
            border-right: 1px solid gray;
            background-color: white;
        } '''
    
    def get_model(self): return self.model
    
class InputModel(QtGui.QStandardItemModel):
    def __init__(self):
        super().__init__()

        self.a = np.array([10, 20, 30])
        self.b = np.array([15, 20, 25])
        self.c = np.array(
            [[5,3,1],
            [3,2,4],
            [4,1,2]], np.float64)

        self.setHorizontalHeaderLabels([f"x{i+1}" for i in range(self.c.shape[1])] + ["B"])
        self.setVerticalHeaderLabels([f"{i+1}" for i in range(self.c.shape[0])] + ["C"])
        
        self.fill_a()
        self.fill_b()
        self.fill_c()
        
    # def addCol(self):
    #     if (self.columnCount == 6): return

    # def addRow(self):
    #     pass
    
    # def delCol(self):
    #     pass

    # def delRow(self):
    #     pass
        
   
    def fill_a(self):
        for i, el in enumerate(self.a):
            item = QtGui.QStandardItem(str(el))
            self.setItem(i, self.columnCount() - 1, item)
                         
    def fill_b(self):
        for i, el in enumerate(self.b):
            item = QtGui.QStandardItem(str(el))
            self.setItem(self.rowCount() - 1, i, item)
                    
    def fill_c(self):
        for i in range(len(self.c)):
            for j in range(len(self.c[i])):
                self.setItem(i, j, QtGui.QStandardItem(str(self.c[i][j])))

    def get_a(self):
        a = []
        for i in range(len(self.a)):
            a.append(int(self.item(i, self.columnCount() - 1).text()))
        return a
    
    def get_b(self):
        b = []
        for i in range(len(self.b)):
            b.append(int(self.item(self.rowCount() - 1, i).text()))
        return np.array(b)     
    def get_c(self):
        c = []
        for i in range(len(self.c)):
            c.append([])
            for j in range(len(self.c[i])):
                c[-1].append(float(self.item(i, j).text()))
        return np.array(c)
    
class OutputModel(QtGui.QStandardItemModel):

    def fill(self, vogel_res, iModel):
        self.clear()
        res = vogel_res 
        
        B = [f"\nB{i+1}" for i in range(iModel.c.shape[0])]
        A = [f"\nA{i+1}" for i in range(iModel.c.shape[1])]
        
        self.setHorizontalHeaderLabels([*B, 'Запасы', 'di'])

        vLabels = []
        
        for i in range(len(res)):
            vLabels.extend([*A, 'Потребности', 'dj', ''])
        
        self.setVerticalHeaderLabels(vLabels[:-1])
        
        iLen = iModel.c.shape[0]
        jLen = iModel.c.shape[1]
        for k in range(len(res)):
            for i in range(iModel.c.shape[0]):
                di = 'X' if res[k][1][i] == -1 or res[k][1][i] == np.inf else res[k][1][i]
                row = k*(1 + len(res[k]))
                # запасы
                self.setItem(i + row, jLen, QtGui.QStandardItem(str(res[k][0][i])))
                # разность по столбцам
                self.setItem(row + i, jLen + 1, QtGui.QStandardItem(str(di)))      
                for j in range(iModel.c.shape[1]):
                    # потребности
                    self.setItem(row + iLen, j, QtGui.QStandardItem(str(res[k][2][j])))  
                    # разность по строкам
                    dj = 'X' if res[k][3][j] == -1 or res[k][3][j] == np.inf else res[k][3][j]
                    self.setItem(row + iLen + 1, j, QtGui.QStandardItem(str(dj)))
                    # отправлено запасов
                    self.setItem(row + i, j, QtGui.QStandardItem(str(res[k][-1][i][j])))
        
       
        # x = [.0 for i in range(iModel.A_ub.shape[0])]
        # for i in range(iModel.A_ub.shape[0]):
        #         if int(full_res[-1][i][1][1:]) - 1 < iModel.A_ub.shape[0]:
        #             x[int(full_res[-1][i][1][1:]) - 1] = float(full_res[-1][i][3])
                             
        # text = ""
        # for i, el in enumerate(x):
        #     text += f"x{i} = {(el)}\n"
        # text += f"\nF = {full_res[-1][-1][3]}" 
        
        # mbox = QtWidgets.QMessageBox()
        # mbox.setText(text)
        # mbox.exec()
        
if __name__ == "__main__":
    app = App()
    sys.exit(app.exec())
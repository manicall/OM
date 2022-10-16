from numbers import Rational
import sys
import numpy as np
import sympy as sp
from PyQt5 import QtWidgets, QtGui
from scipy.optimize import linprog	
from simplex import simplex

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
        solution_menu = menu_bar.addMenu("Решить")
        solution_menu.addAction("Симплексный метод", self.solve_my)
        solution_menu.addAction("SciPy оптимизация", self.solve_scipy)
        
        # table_menu = menu_bar.addMenu('Столбец таблицы')
        # table_menu.addAction("Добавить столбец", self.widget.inputModel.addCol)
        # table_menu.addAction("Удалить столбец", self.widget.inputModel.delCol)
        
        # table_menu = menu_bar.addMenu('Строка таблицы')
        # table_menu.addAction("Добавить строку", self.widget.inputModel.addRow)
        # table_menu.addAction("Удалить строку", self.widget.inputModel.delRow)
        
    def solve_my(self):
        model = self.widget.inputModel
        a, b, c = model.get_A_ub(), model.get_b_ub(), model.get_c()
        
        self.widget.outputModel.fill(simplex(a, b, c), model)
    
    @staticmethod
    def solve_scipy():
        max = True
        ScipySolver.scipy_solve(max)
        
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
        # Коэффициенты линейной целевой функции
        self.c = np.array([9, 10, 16])
        
        # коэффициенты при переменных для условий в виде неравенств
        self.A_ub = np.array(
            [[18, 15, 12],
            [6, 4, 8], 
            [5, 3, 3]])

        # вектор ограничения неравенства
        self.b_ub = np.array([360, 192, 180])

        self.setHorizontalHeaderLabels([f"x{i+1}" for i in range(self.A_ub.shape[1])] + ["B"])
        self.setVerticalHeaderLabels([f"{i+1}" for i in range(self.A_ub.shape[0])] + ["C"])
        
        self.fill_A_up()
        self.fill_b_ub()
        self.fill_c()
        
    # def addCol(self):
    #     if (self.columnCount == 6): return

    # def addRow(self):
    #     pass
    
    # def delCol(self):
    #     pass

    # def delRow(self):
    #     pass
        
    def fill_A_up(self):
        for i in range(len(self.A_ub)):
            for j in range(len(self.A_ub[i])):
                self.setItem(i, j, QtGui.QStandardItem(str(self.A_ub[i][j])))
                
    def fill_b_ub(self):
        for i, el in enumerate(self.b_ub):
            item = QtGui.QStandardItem(str(el))
            self.setItem(i, self.columnCount() - 1, item)
            
    def fill_c(self):
        for i, el in enumerate(self.c):
            item = QtGui.QStandardItem(str(el))
            self.setItem(self.rowCount() - 1, i, item)
                    
    def get_A_ub(self):
        A_ub = []
        for i in range(len(self.A_ub)):
            A_ub.append([])
            for j in range(len(self.A_ub[i])):
                A_ub[-1].append(int(self.item(i, j).text()))
        return np.array(A_ub)

    def get_b_ub(self):
        b_ub = []
        for i in range(len(self.b_ub)):
            b_ub.append(int(self.item(i, self.columnCount() - 1).text()))
        return np.array(b_ub)

    def get_c(self):
        c = []
        for i in range(len(self.c)):
            c.append(int(self.item(self.rowCount() - 1, i).text()))
        return c
    
class OutputModel(QtGui.QStandardItemModel):
    def initHeaders(self, iModel):        
        p = [str(el) + f"\nP{i+1}" for i, el in enumerate(iModel.c)]
        
        maxLen = iModel.A_ub.shape[0] + len(iModel.c)
        pb = [str(0) + f"\nP{i+1}" for i in range(len(iModel.c), maxLen)]
        
        self.setHorizontalHeaderLabels(["i", "Базис", "Сб", "P0", *p, *pb])
    
    def fill(self, full_res, iModel):
        self.clear()
        self.initHeaders(iModel)
         
        for i in range(len(full_res)):   
            for j in range(len(full_res[i])):
                for k in range(len(full_res[i][j])):
                    self.setItem(
                        j + i*(1 + len(full_res[i])), k,
                        QtGui.QStandardItem(self.getVal(full_res[i][j][k])))
                
        x = [.0 for i in range(iModel.A_ub.shape[0])]
        for i in range(iModel.A_ub.shape[0]):
                if int(full_res[-1][i][1][1:]) - 1 < iModel.A_ub.shape[0]:
                    x[int(full_res[-1][i][1][1:]) - 1] = float(full_res[-1][i][3])
                             
        text = ""
        for i, el in enumerate(x):
            text += f"x{i} = {(el)}\n"
        text += f"\nF = {full_res[-1][-1][3]}" 
        
        mbox = QtWidgets.QMessageBox()
        mbox.setText(text)
        mbox.exec()

    def getVal(self, param):
        if param == None: param = ""
        return str(sp.Rational(param).limit_denominator(100)) if np.float64 == type(param) else str(param)

if __name__ == "__main__":
    app = App()
    sys.exit(app.exec())
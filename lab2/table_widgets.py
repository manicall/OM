from PyQt5 import QtWidgets, QtGui
from signs import Signs
import numpy as np
import sympy as sp

class InputTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
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

        self.columnHeaders = [f"x{i+1}" for i in range(self.A_ub.shape[1])] + ["Знак", "B"]
        self.rowHeaders = [f"{i+1}" for i in range(self.A_ub.shape[0])] + ["C"]
        
        self.setColumnCount(len(self.columnHeaders))
        self.setRowCount(len(self.rowHeaders))

        self.setHorizontalHeaderLabels(self.columnHeaders)
        self.setVerticalHeaderLabels(self.rowHeaders)
        
        self.fill_A_up()
        self.fill_b_ub()
        self.fill_c()
        self.fill_sign()

        self.setFixedHeight(150)
        
    def addCol(self):
        if (self.columnCount() >= 8): return
        self.insertColumn(self.columnCount() - 2)

    def addRow(self):
        if (self.rowCount() >= 5): return
        self.insertRow(self.rowCount() - 1)
        self.fill_sign()
    
    def delCol(self):
        if (self.columnCount() <= 4): return
        self.removeColumn(self.columnCount() - 3)

    def delRow(self):
        if (self.rowCount() <= 3): return
        self.removeRow(self.rowCount() - 2)
    
    #region функции для управления содержимым таблицы
    def fill_A_up(self):
        for i in range(len(self.A_ub)):
            for j in range(len(self.A_ub[i])):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(str(self.A_ub[i][j])))
                
    def fill_b_ub(self):
        for i, el in enumerate(self.b_ub):
            item = QtWidgets.QTableWidgetItem(str(el))
            self.setItem(i, self.columnCount() - 1, item)
            
    def fill_c(self):
        for i, el in enumerate(self.c):
            item = QtWidgets.QTableWidgetItem(str(el))
            self.setItem(self.rowCount() - 1, i, item)
                    
    def fill_sign(self):
        for i in range(self.rowCount() - 1):
            comboBox = QtWidgets.QComboBox()
            comboBox.addItems(Signs.signs)
            self.setCellWidget(i, self.columnCount() - 2, comboBox)
            
    def get_A_ub(self):
        A_ub = []
        for i in range(len(self.A_ub)):
            A_ub.append([])
            for j in range(len(self.A_ub[i])):
                A_ub[-1].append(float(self.item(i, j).text()))
        return np.array(A_ub)

    def get_b_ub(self):
        b_ub = []
        for i in range(len(self.b_ub)):
            b_ub.append(float(self.item(i, self.columnCount() - 1).text()))
        return np.array(b_ub)

    def get_c(self):
        c = []
        for i in range(len(self.c)):
            c.append(float(self.item(self.rowCount() - 1, i).text()))
        return c
    
    def get_signs(self):
        signs = []
        for i in range(self.rowCount() - 1):
            signs.append(self.cellWidget(i, self.columnCount() - 2).currentText())
        return signs
       
    #endregion
    pass  

class OutputTableWidget(QtWidgets.QTableWidget):
    def initHeaders(self, tInput):        
        p = [str(el) + f"\nP{i+1}" for i, el in enumerate(tInput.c)]
        
        self.maxLen = tInput.A_ub.shape[0] + len(tInput.c)
        pb = [str(0) + f"\nP{i+1}" for i in range(len(tInput.c), self.maxLen)]
        
        constColHeaders = ["i", "Базис", "Сб", "P0"]
        
        self.setColumnCount(len(constColHeaders)+len(p)+len(pb))
        self.setHorizontalHeaderLabels(constColHeaders + p + pb)
        self.setRowCount(0)
    
    def fill(self, full_res, tInput):
        if full_res is None: return
        
        self.clear()
        self.initHeaders(tInput)
        
        self.insertRow(0)
        
        for i in range(len(full_res)):   
            self.appendRow()
            for j in range(full_res[i].getRowLen()):
                self.appendRow()
                for k in range(full_res[i].getColLen()):
                    self.setItem(
                        j + i*(1 + full_res[i].getRowLen()), k,
                        QtWidgets.QTableWidgetItem(self.getVal(full_res[i].getRow(j)[k])))
        
        f, x = full_res[-1].getResult()
        self.setItem(self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem("F=")) 
        self.setItem(self.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(self.getVal(f)))

        self.setItem(self.rowCount() - 1, 3, QtWidgets.QTableWidgetItem("X=")) 
        for j in range(4, len(x) + 4):
            self.setItem(self.rowCount() - 1, j, QtWidgets.QTableWidgetItem(self.getVal(x[j-4])))
                  
        self.resizeColumnsToContents()
        self.resizeRowsToContents()      

    def getVal(self, param):
        if param == None: param = ""
        return str(sp.Rational(param).limit_denominator(100)) if np.float64 == type(param) else str(param)
    
    def appendRow(self):
        self.insertRow(self.rowCount() - 1)

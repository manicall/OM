from PyQt5 import QtWidgets, QtGui
import numpy as np
import sympy as sp

class OutputTableWidget(QtWidgets.QTableWidget):    
    def fill(self, vogel_res, iTable):
        self.clear()
        res = vogel_res 
        
        if res is None: return
        
        B = [f"\nB{i+1}" for i in range(iTable.columnCount() - 1)]
        constColHeaders = ['Запасы', 'di']
        self.setColumnCount(len(B) + len(constColHeaders)) 
        self.setHorizontalHeaderLabels(B + constColHeaders)
        
        A = [f"\nA{i+1}" for i in range(iTable.rowCount() - 1)]
        vLabels = []
        
        for i in range(len(res)):
            vLabels.extend([*A, 'Потребности', 'dj', ''])
        vLabels[-1] = "S"
        
        self.setRowCount(len(vLabels)) 
        self.setVerticalHeaderLabels(vLabels)
        
        outputResult(res, iTable)
                
        self.resizeColumnsToContents()
        self.resizeRowsToContents()      

    def getVal(self, param):
        if param == None: param = ""
        return str(sp.Rational(param).limit_denominator(100)) if np.float64 == type(param) else str(param)
    
    def appendRow(self):
        self.insertRow(self.rowCount() - 1)
        
    def outputResult(self, res, iTable):
        iLen = iTable.rowCount() - 1
        jLen = iTable.columnCount() - 1
        
        for k in range(len(res)):
            for i in range(iTable.rowCount() - 1):
                di = 'X' if res[k][1][i] == -1 or res[k][1][i] == np.inf else res[k][1][i]
                row = k*(len(res[k])) # может привести к ошибкам при изменеии результата возвращаемого функцией фогеля
                # запасы
                self.setItem(i + row, jLen, QtWidgets.QTableWidgetItem(str(res[k][0][i])))
                # разность по столбцам
                self.setItem(row + i, jLen + 1, QtWidgets.QTableWidgetItem(str(di)))      
                for j in range(iTable.columnCount() - 1):
                    # потребности
                    self.setItem(row + iLen, j, QtWidgets.QTableWidgetItem(str(res[k][2][j])))  
                    # разность по строкам
                    dj = 'X' if res[k][3][j] == -1 or res[k][3][j] == np.inf else res[k][3][j]
                    self.setItem(row + iLen + 1, j, QtWidgets.QTableWidgetItem(str(dj)))
                    # отправлено запасов
                    self.setItem(row + i, j, QtWidgets.QTableWidgetItem(str(res[k][4][i][j])))
         
            self.setColours(res, k, row, jLen, iLen)
                       
        S = np.sum(res[k][4] * iTable.get_A_ub())
        self.setItem(self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(S))) 
        
    def setColours(self, res, k, row, jLen, iLen):
        ii, jj = res[k][5][1]
        self.item(ii + row, jj).setBackground(QtGui.QColor(100,100,150))
        if (res[k][5][0] == 'di'):
            self.item(ii + row, jLen).setBackground(QtGui.QColor(0,100,150))
            self.item(ii + row, jLen+1).setBackground(QtGui.QColor(196,53,53))
            self.item(row + iLen, jj).setBackground(QtGui.QColor(0,100,150))
        elif (res[k][5][0] == 'dj'):
            self.item(ii + row, jLen).setBackground(QtGui.QColor(0,100,150))
            self.item(row + iLen, jj).setBackground(QtGui.QColor(0,100,150))
            self.item(row + iLen+1, jj).setBackground(QtGui.QColor(196,53,53))

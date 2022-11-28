from PyQt5 import QtWidgets, QtGui
import numpy as np
import sympy as sp

class InputTableWidget(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
                
        # коэффициенты при переменных для условий в виде неравенств
        self.A_ub = np.array(
            [[5,3,1],
            [3,2,4],
            [4,1,2]], np.float64)

        # вектор ограничения неравенства
        self.b_ub = np.array([10, 20, 30])
        
        # Коэффициенты линейной целевой функции
        self.c = np.array([15, 20, 25])
        
        self.setSettings()
        
    def setSettings(self):
        self.columnHeaders = [f"{i+1}" for i in range(self.A_ub.shape[1])] + ["B"]
        self.rowHeaders = [f"{i+1}" for i in range(self.A_ub.shape[0])] + ["C"]

        self.setColumnCount(len(self.columnHeaders))
        self.setRowCount(len(self.rowHeaders))

        self.setHorizontalHeaderLabels(self.columnHeaders)
        self.setVerticalHeaderLabels(self.rowHeaders)
        
        self.fill_A_up()
        self.fill_b_ub()
        self.fill_c()
        
        self.setFixedHeight(150)
        
    def fromTextFile(self):
        f = open(r"lab3/table.txt")
        text = f.readlines()
        
        l = []
        for i in text:
            l.append(i.split(' '))
        
        self.A_ub = []
        for i in range(len(l) - 1):
            self.A_ub.append([])
            for j in range(len(l[i]) - 1):
                self.A_ub[-1].append(int(l[i][j]))
        self.A_ub = np.array(self.A_ub)
        
        self.b_ub = []
        for i in range(len(l) - 1):
            print(l[-1][i])
            self.b_ub.append(int(l[i][-1]))
        
        self.c = []    
        for j in range(len(l[0]) - 1):
            self.c.append(l[-1][j])
            
        self.setSettings()
        
    def addCol(self):
        if (self.columnCount() >= 8): return
        self.insertColumn(self.columnCount() - 1)

    def addRow(self):
        if (self.rowCount() >= 5): return
        self.insertRow(self.rowCount() - 1)
    
    def delCol(self):
        if (self.columnCount() <= 4): return
        self.removeColumn(self.columnCount() - 2)

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
            
    def get_A_ub(self):
        A_ub = []
        for i in range(self.rowCount() - 1):
            A_ub.append([])
            for j in range(self.columnCount() - 1):
                A_ub[-1].append(float(self.item(i, j).text()))
        return np.array(A_ub)

    def get_b_ub(self):
        b_ub = []
        for i in range(self.rowCount() - 1):
            b_ub.append(float(self.item(i, self.columnCount() - 1).text()))
        return np.array(b_ub)

    def get_c(self):
        c = []
        for i in range(self.columnCount() - 1):
            c.append(float(self.item(self.rowCount() - 1, i).text()))
        return c
       
    #endregion
    pass  

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
        
        self.outputResult(res, iTable)
                
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
                ii, jj = res[k].colored[1]
                diff_b = f"[{res[k].diff}]" if i == ii  else ""
                di = 'X' if res[k].di[i] == -1 else res[k].di[i]
                row = k*(iTable.rowCount() + 2) # может привести к ошибкам при изменеии результата возвращаемого функцией фогеля
                # запасы
                self.setItem(i + row, jLen, QtWidgets.QTableWidgetItem(str(res[k].b[i]) + diff_b))
                # разность по столбцам
                self.setItem(row + i, jLen + 1, QtWidgets.QTableWidgetItem(str(di)))      
                for j in range(iTable.columnCount() - 1):
                    diff_c = f"[{res[k].diff}]" if j == jj  else ""
                    # потребности
                    self.setItem(row + iLen, j, QtWidgets.QTableWidgetItem(str(res[k].c[j]) + diff_c))  
                    # разность по строкам
                    dj = 'X' if res[k].dj[j] == -1 else res[k].dj[j]
                    self.setItem(row + iLen + 1, j, QtWidgets.QTableWidgetItem(str(dj)))
                    # отправлено запасов
                    self.setItem(row + i, j, QtWidgets.QTableWidgetItem(str(iTable.A_ub[i][j]) + f"[{res[k].sended[i][j]}]"))
         
            self.setColours(res, k, row, jLen, iLen)
                       
        S = np.sum(res[k].sended * iTable.get_A_ub())
        self.setItem(self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(S))) 
        
    def setColours(self, res, k, row, jLen, iLen):
        ii, jj = res[k].colored[1]
        self.item(ii + row, jj).setBackground(QtGui.QColor(100,100,150))
        if (res[k].colored[0] == 'di'):
            self.item(ii + row, jLen).setBackground(QtGui.QColor(0,100,150))
            self.item(ii + row, jLen+1).setBackground(QtGui.QColor(196,53,53))
            self.item(row + iLen, jj).setBackground(QtGui.QColor(0,100,150))
        elif (res[k].colored[0] == 'dj'):
            self.item(ii + row, jLen).setBackground(QtGui.QColor(0,100,150))
            self.item(row + iLen, jj).setBackground(QtGui.QColor(0,100,150))
            self.item(row + iLen+1, jj).setBackground(QtGui.QColor(196,53,53))

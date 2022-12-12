from PyQt5 import QtWidgets, QtGui
import numpy as np
import sympy as sp

class OutputTableWidget(QtWidgets.QTableWidget):    
    def fill(self, frankwolf_res):
        if frankwolf_res == "error":
            QtWidgets.QMessageBox.critical(self, "Ошибка симплексного метода", "Невозможно решить задачу")
            return
        
        self.clear()
        res = frankwolf_res.getAll() 
        
        if res is None: return
        
        B = ["X", "C", "Z", "L", "f"]
        self.setColumnCount(len(B)) 
        self.setHorizontalHeaderLabels(B)
        
        self.setRowCount(frankwolf_res.getLen()) 
        
        self.outputResult(res)
                
        self.resizeColumnsToContents()
        self.resizeRowsToContents()      

    def getVal(self, param):
        if param == None: param = ""
        return str(sp.Rational(param).limit_denominator(100)) if np.float64 == type(param) else str(param)
    
    def appendRow(self):
        self.insertRow(self.rowCount() - 1)
        
    def outputResult(self, res):
        for i in range(len(res)):
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(res[i].getX()))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(res[i].getC()))
            self.setItem(i, 2, QtWidgets.QTableWidgetItem(res[i].getZ()))
            self.setItem(i, 3, QtWidgets.QTableWidgetItem(str(res[i].L)))
            self.setItem(i, 4, QtWidgets.QTableWidgetItem(str(res[i].f)))

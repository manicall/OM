from PyQt5 import QtWidgets
from scipy.optimize import linprog

class ScipySolver:
    @classmethod
    def scipy_solve(self, table_input, max = False):
        '''решает задачу оптимизации'''
        table_input
        
        try:
            c = [-i for i in table_input.get_c()] if max else table_input.get_c()
            A_ub = table_input.get_A_ub()
            b_ub = table_input.get_b_ub()
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
                text += f"x{i[0]+1} = {(i[1])}\n"
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
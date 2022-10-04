from tkinter import X
from equals import Equals, MyEnum
import sympy as sp
import math as m

class FastDescent():
    '''
        Свойства:
            ex: уравнение, заданное строковым типом
            x: список точек [x1, x2, ..., xn], где xn список точек,
                найденных в процессе выполнения алгоритма
            h: шаг
            E: точность
    '''
    
    @classmethod 
    def get_result(self, ex = None, x = None, h = None, E = None):
        def get_last_xi(x):
            '''генерирует набор последних точек хранящихся в списке x.
               xi - x1, x2 ... xn'''
            for xi in x: 
                yield xi[-1]
            
        def get_df_dxi(x):
            '''генерирует набор вычисленных производных 
            по точкам x1, x2, ..., xn'''
            for i in range(x_len):
                yield dx[i](*get_last_xi(x)) 
        
        def get_dx():
            '''возвращает список лямбд вычисляющих производную в заданной точке'''
            dx = []
            for i in range(x_len):
                # строка представляющая собой df/dxi
                df = str(sp.diff(ex, f"x{i+1}"))
                # массив функций созданный из df
                dx.append(sp.lambdify(get_xi_with_default(), df)) 
            return dx
        
        def get_xi():
            '''возвращает список строк: 'x1', 'x2', ..., 'xn' '''
            return [f'x{i+1}' for i in range(x_len)]
        
        def get_xi_with_default():
            '''возвращает список строк: 'x1=0', 'x2=0', ..., 'xn=0' '''
            return ['x'+str(i + 1)+'=0' for i in range(x_len)]
    
        def grad(x):
            '''принимает параметром одномерный список 
            координат ([x1, x2, ... xn], где xn - число), возвращает градиент'''
            # sqrt(sum(x1**2, x2**2 ... xn**2))
            return m.sqrt(sum([xi**2 for xi in x]))
        
        ex = Equals.get_ex(2) if ex is None else ex
        x  = [[-2], [-2]] if x is None else x
        h = 0.01 if h is None else h
        E = 0.01 if E is None else E
        x_len = len(x)
        f = sp.lambdify(get_xi(), ex)
        dx = get_dx()

        result = []
        def iter():
            temp_dx = [*get_df_dxi(x)]
            # условие остановки
            if grad(temp_dx) < E: 
                return False
            
            # подстановка (xi -> (xi - d*dxi)), d - шаг
            text = ''
            replaced_ex = ex
            for i in range(x_len):
                text = (str(x[i][-1]) + " - " + str(temp_dx[i]) + "*d")
                text = text.replace('- -', '+ ')
                replaced_ex = replaced_ex.replace(f"x{i+1}", f'({text})')
            
            # вычисление шага для текущей итерации   
            try:
                h = round(float(sp.solve(sp.diff(replaced_ex, 'd'), 'd')[-1]), 3)
            except:
                h = 0.1
            
            for i in range(x_len):
                x[i].append(round(x[i][-1] - h * temp_dx[i], 3))

            result.append([*get_last_xi(x), *get_df_dxi(x), h, f(*get_last_xi(x))])

            return True
        
        n = 100
        result.append([*get_last_xi(x), *get_df_dxi(x), h, f(*get_last_xi(x))]) 
        for i in range(1, n):
            if not iter(): break
            
        return result

    def fastest_descent():
        pass

if __name__ == '__main__':
    print(FastDescent.get_result())
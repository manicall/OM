"""
Методы:
1) покоординатный спуск
2) хука-дживса
3) градиентный спуск
4) сопряженных градиентов
5) тяжелого шарика
6) нелдера - мида
7) наискорейшего спуска
8) случайных направлений
9) слепого поиска

пример f(x, y) = 100*(y - x^2)^2 + (1 - x)^2 
пример f(x, y) = 100*(y2 - x1^2)^2 + (1 - x1)^2 

"""
import sympy as sp
import numpy as np
from scipy import optimize as opt
from equals import Equals

def coordinate_descent():
    E = 0.0001

    Equals.set_equal_1()
    
    Equals.print_ex()


def hook_jeeves():
    Equals.set_equal_1()
    
    ex = Equals.get_ex()
    f1 = Equals.get_f1()
    
    print(ex)
    
    x = [[1.5], [1.5]]
    h = [1]
    a = 0.5
    E = 0.001
    start = 0
    end = 10000
        
    def is_equals(x):
        for i in range(len(x)): 
            if x[i][-2] != x[i][-1]: 
                return False
        return True
    
    while start < end:
        def get_x():
            for i in x:
                yield i[-1]
        
        def get_dx(e, i):
            for j in enumerate(x):
                yield j[1][-1] if j[0] != i else j[1][-1] + e*h[-1]

        def search():
            for i in range(len(x)):
                if f1(*get_x()) > f1(*get_dx(1, i)):
                    x[i].append(x[i][-1] + h[-1])
                else:
                    x[i].append(x[i][-1])
                    
            if is_equals(x):
                for i in range(len(x)):
                    if f1(*get_x()) > f1(*get_dx(-1, i)):
                        x[i].append(x[i][-1] - h[-1])
                    else:
                        x[i].append(x[i][-1])
                
                if is_equals(x): return False              
            
            return True

        if not search():
            if (h[-1] > E): 
                h.append(h[-1] * a)
                continue
            else:
                break
        
        print(*x, sep='\n')
        
        def xp_v1(i):
            return x[i][-1] + (x[i][-1] - x[i][-2])
        
        # по методичке
        def xp_v2(i):
            return x[i][-2] + 2*(x[i][-1] - x[i][-2])
            
        xp = [xp_v2(i) for i in range(len(x))]
        
        if f1(*xp) < f1(*get_x()):
            for i in range(len(x)):
                x[i].append(xp[i])
        else:
            if (h[-1] > E): 
                h.append(h[-1] * a)
            else:
                break

        if (h[-1] <= E):
            break 
                 
        start += 1

    print(f"x{tuple(get_x())}")

    
    pass

hook_jeeves()
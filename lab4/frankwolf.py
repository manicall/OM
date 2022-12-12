import os
import sys
import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '../lab2'))
from simplex import simplex
from frankwolf_result import FullResult, Result

import re
import sympy as sp

from point import Point 
from signs import Signs

def tokenize(expression):
    return re.findall(r"(\b\w*[\.]?\w+\b|\*{2}|[<>=]{1,2}|[\(\)\+\*\-\/])", expression)

def frankwolf(ex, g, X, E):
    E = float(E)
    f = sp.lambdify(("x1", "x2"), ex)
    X = Point(*[int(i) for i in X])
    g = g.split('\n')
    
    # for i in range(len(g)):
    #     g[i] = str(sp.simplify(g[i]))

    a = get_a(g)
    b, signs = get_b_signs(g)
    
    full_res = FullResult()
    #full_res.appendResult(Result(X, c, Z, L, f(*X.getCoord())))
    def iter():  
        nonlocal X, full_res 
        c = grad(ex, X)  
    
        res = simplex(a, b, c, signs)
        # x1 и x2 найденные симплекс методом
        z = res[-1].getResult().X
        Z = Point(z[0], z[1]) 
        
        Z.print()
        
        strX1 = str(sp.simplify(f"{X.x1} + L*({Z.x1}-{X.x1})"))
        strX2 = str(sp.simplify(f"{X.x2} + L*({Z.x2}-{X.x2})"))

        # подстановка (xi -> (strXi)
        replaced_ex = ex
        for i, el in enumerate((strX1, strX2)):
            replaced_ex = replaced_ex.replace(f"x{i+1}", f'({el})')
        
        L = round(float(sp.solve(sp.diff(replaced_ex, 'L'), 'L')[-1]), 2)
        if L > 1: 
            L = 1
        
        newX = Point(X.x1 + L*(Z.x1-X.x1), X.x2 + L*(Z.x2-X.x2))
        print("newX= ", end=" ")
        
        print("diff=", get_difference(f, X, newX))
        if get_difference(f, X, newX) < E:
            full_res.appendResult(Result(newX, c, Z, L, f(*newX.getCoord()))) 
            return False
        
        X = newX
        full_res.appendResult(Result(newX, c, Z, L, f(*newX.getCoord())))
        return True
    
    n = 10
    while iter():
        n -= 1
        if n < 0: break;
    
    return full_res
        
def get_difference(f, X, newX):
    #print(f(X.x1, X.x2), f(newX.x1, newX.x2))
    return abs(f(X.x1, X.x2) - f(newX.x1, newX.x2))
  
def get_b_signs(g):
    b = []
    signs = []
    # поиск знака неравентва 
    for i in range(len(g)):
        token = tokenize(g[i])
        for j in range(len(token)):
            if Signs.isSign(token[j]):
                signs.append(token[j])
                b.append(float("".join(token[j+1:])))
                break
            
    return np.array(b), signs

def get_a(g):
    def index(var):
        return int(var[1:]) - 1
    
    def set_a(a, var):
        if j > 0: # перед xi как минимум один токен
            if token[j - 1] == "*":
                if j-3 >= 0: # перед числом есть знак (например -20*x1..)
                    a[index(var)] = float(token[j-3] + token[j-2])
                else: # перед числом знака нет (например 20*x1..)
                    a[index(var)] = float(token[j-2])
            # перед переменной стоит знак [+-] (например -x1..)      
            elif token[j - 1] == "-" or token[j - 1] == "+":
                a[index(var)] = float("".join((token[j-1], '1')))
            # перед переменной стоит число (например 20x1..)
            elif token[j - 1].isdigit():
                if j-2 >= 0: # перед числом есть знак (например -20x1..)
                    a[index(var)] = float(token[j-2] + token[j-1])
                else: # перед числом знака нет (например 20x1..)
                    a[index(var)] = float(token[j-1])
            else:
                print("ограничение задано некорректно")
                return      
        else: # выражение начинается с переменной (например x1..)
            a[index(var)] = 1
            
    A = []
    for i in range(len(g)):
        token = tokenize(g[i])
        a = [0, 0]
        for j in range(len(token)):
            if token[j] == 'x1':
                set_a(a, 'x1')
            elif token[j] == 'x2':
                set_a(a, 'x2')
        A.append(a)
            
    return np.array(A)


    
    # def insertA(i, temp):
    #     if j == 0: temp = "+"
    #     if temp == "+": temp = "1"
    #     elif temp == "-": temp = "-1"
    #     elif temp == "": temp = "0"
    #     a[-1][i] = int(temp)
                
    # a = []
    # # поиск знака неравентва 
    # for i in range(len(g)):
    #     a.append([0, 0])
    #     token = tokenize(g[i])
    #     temp = ""
    #     for j in range(len(token)):
    #         if (token[j].isdigit() or token[j] == "+" or token[j] == "-") :
    #             temp += token[j]
    #         elif token[j] == "x1":
    #             insertA(0, temp)
    #             temp = ""
    #         elif token[j] == "x2":
    #             insertA(1, temp)
    #             temp = ""
                
    #         if token[j]:
    #             break
            
    # return np.array(a)

def grad(f, p):
    dx1 = sp.lambdify(("x1", "x2"), sp.diff(f, "x1"))
    dx2 = sp.lambdify(("x1", "x2"), sp.diff(f, "x2"))
    
    return [dx1(p.x1, p.x2), dx2(p.x1, p.x2)]

if __name__ == "__main__":
    frankwolf()
    
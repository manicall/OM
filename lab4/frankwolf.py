import os
import sys
import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '../lab2'))
from simplex import simplex

import re
import sympy as sp

from point import Point 

def tokenize(expression):
    return re.findall(r"(\b\w*[\.]?\w+\b|\*{2}|[<>=]{1,2}|[\(\)\+\*\-\/])", expression)

def frankwolf(X = Point(0, 0)):
    E = 0.01
    ex = "2*x1 + 4*x2 - x1**2 - 2*x2**2"
    f = sp.lambdify(("x1", "x2"), ex)
    
    g = [
        "x1 + 2*x2 <= 8\n",
        "2*x1 - x2 <= 12"
    ]
    
    for i in range(len(g)):
        g[i] = str(sp.simplify(g[i]))

    a = get_a(g)
    b = get_b(g)

    def iter():  
        nonlocal X  
        c = grad(ex, X)  
    
        res = simplex(a, b, c)
        # x1 и x2 найденные симплекс методом
        z = res[-1].getResult()[1]
        Z = Point(z[0], z[1]) 
        
        Z.print()
        
        strX1 = str(sp.simplify(f"{X.x1} + L*({Z.x1}-{X.x1})"))
        strX2 = str(sp.simplify(f"{X.x2} + L*({Z.x2}-{X.x2})"))
        
        # print(strX1)
        # print(strX2)

        # подстановка (xi -> (strXi)
        replaced_ex = ex
        for i, el in enumerate((strX1, strX2)):
            replaced_ex = replaced_ex.replace(f"x{i+1}", f'({el})')
        
        #print(str(sp.simplify(replaced_ex)))
        
        L = round(float(sp.solve(sp.diff(replaced_ex, 'L'), 'L')[-1]), 3)
        if L > 1: 
            L = 1
            
        print("L= ", L)
        
        newX = Point(X.x1 + L*(Z.x1-X.x1), X.x2 + L*(Z.x2-X.x2))
        print("newX= ", end=" ")
        newX.print()
        
        print("diff=", get_difference(f, X, newX))
        if get_difference(f, X, newX) < E: 
            return False
        
        X = newX
        return True
    
    n = 10
    while iter():
        n -= 1
        if n < 0: break;
        
def get_difference(f, X, newX):
    #print(f(X.x1, X.x2), f(newX.x1, newX.x2))
    return abs(f(X.x1, X.x2) - f(newX.x1, newX.x2))
  
def get_b(g):
    b = []
    # поиск знака неравентва 
    for i in range(len(g)):
        token = tokenize(g[i])
        for j in range(len(token)):
            if token[j] == "<=" or token[j] == ">=":
                b.append(int(token[j+1]))
                break
            
    return np.array(b)

def get_a(g):
    
    def insertA(i, temp):
        if j == 0: temp = "+"
        if temp == "+": temp = "1"
        elif temp == "-": temp = "-1"
        elif temp == "": temp = "0"
        a[-1][i] = int(temp)
                
    a = []
    # поиск знака неравентва 
    for i in range(len(g)):
        a.append([0, 0])
        token = tokenize(g[i])
        temp = ""
        for j in range(len(token)):
            if (token[j].isdigit() or token[j] == "+" or token[j] == "-") :
                temp += token[j]
            elif token[j] == "x1":
                insertA(0, temp)
                temp = ""
            elif token[j] == "x2":
                insertA(1, temp)
                temp = ""
                
            if token[j] == "<=" or token[j] == ">=":
                break
            
    return np.array(a)

def grad(f, p):
    dx1 = sp.lambdify(("x1", "x2"), sp.diff(f, "x1"))
    dx2 = sp.lambdify(("x1", "x2"), sp.diff(f, "x2"))
    
    return [dx1(p.x1, p.x2), dx2(p.x1, p.x2)]

if __name__ == "__main__":
    frankwolf()
    
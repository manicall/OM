import sympy as sp
import numpy as np

x1 = [0]
x2 = [0]

h = 0.1

f = '(x1 - 3) ** 2 + (5 - x2) ** 2' 

dx1 = sp.lambdify('x1', sp.diff(f, 'x1'))
dx2  = sp.lambdify('x2', sp.diff(f, 'x2'))

grad1 = lambda x1: dx1(x1)
grad2 = lambda x2: dx2(x2)

mgrad = lambda x1, x2: np.sqrt(dx1(x1)**2 + dx2(x2)**2)

def x0(x1, x2):    
    xx1 = x1[-1] - h*grad1(x1[-1])
    xx2 = x2[-1] - h*grad2(x2[-1])
    
    x1.append(xx1)
    x2.append(xx2)

def xi(x1, x2):
    a = mgrad(x1[-1], x2[-1]) ** 2 / mgrad(x1[-2], x2[-2]) ** 2

    xx1 = x1[-1] - h * (grad1(x1[-1]) + a*grad1(x1[-2]))
    xx2 = x2[-1] - h * (grad2(x2[-1]) + a*grad2(x2[-2]))
    
    x1.append(xx1)
    x2.append(xx2)
    
x0(x1, x2)

for i in range(100):
    xi(x1, x2)


print(x1[-1], x2[-1], sep='\n')


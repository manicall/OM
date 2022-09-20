from equals import Equals, MyEnum
import sympy as sp
import math as m

def fastest_descent():
    f = Equals.get_f(MyEnum.fd_first)
    E = 0.1
    x = [[-2], [3]]    
    h = 0.1
    
    grad = lambda x: m.sqrt(sum([xi**2 for xi in x]))
    
    dx = []
    for i in range(len(x)):
        param = ['x'+str(i + 1)+'=0' for i in range(len(x))]
        xi = 'x'+str(i + 1)

        dx.append(sp.lambdify(param, str(sp.diff(Equals.get_ex(), xi))))
    
    temp_dx = []
    for i in range(len(x)):
        temp_x = [xi[-1] for xi in x]
        temp_dx.append(dx[i](*temp_x))

    print(grad(temp_dx))

    if grad(temp_dx) > E: return 
    
if __name__ == '__main__':
    fastest_descent()   
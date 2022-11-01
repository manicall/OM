import sympy as sp
import numpy as np
from equals import Equals, MyEnum

def conjugate_gradients():
    x = [[-0.5], [-1]]
    h = 0.1
    f = Equals.get_f(MyEnum.gr_ex)

    dx = []
    for i in range(len(x)):
        xi = 'x' + str(i + 1)
        dx.append(sp.lambdify(['x1', 'x2'], sp.diff(Equals.get_ex(), xi)))

    def mgrad(list_x):
        # обобщенный аналог np.sqrt(dx1(x1)**2 + dx2(x2)**2)
        grad_list = [dx[i](list_x[0], list_x[1]) ** 2 for i in range(len(list_x))]
        #print(grad_list)
        return np.sqrt(sum(grad_list))

    print("i   x1   x2   dR/dx1   dR/dx2   R")
    # поиск минимума на начальном этапе (методом наискорейшего спуска)
    def x0():    
        temp_x = []
        for i in range(len(x)):
            # X0 = Xi - h*gradR(Xi)
            # *dx = grad 
            temp_x.append(x[i][-1] - h*dx[i](x[0][-1], x[1][-1]))
        
        for i in range(len(x)):
            x[i].append(temp_x[i])

    # поиск минимума методом сопряженных градиентов
    def xi():
        #a = mgrad([xi[-1] for xi in x]) ** 2 / mgrad([xi[-2] for xi in x]) ** 2
        temp_x = []
        for i in range(len(x)):
            # *dx = grad 
            temp_x.append(x[i][-1] - h * (dx[i](x[0][-1], x[1][-1]) + a*dx[i](x[0][-2], x[1][-2])))

        
        for i in range(len(x)):
            x[i].append(temp_x[i])
        
    x0()
    # while round(f(x[0][-1], x[1][-1]), 3) != 0: 
    #     xi()
        
    for i in range(len(x[0])):
       print(f"""{i}) | {round(x[0][i], 3)} | {round(x[1][i], 3)} | {round(dx[0](x[0][i], x[1][i]), 3)} | {round(dx[1](x[0][i], x[1][i]), 3)}| {mgrad([xi[i] for xi in x])} | {round(f(x[0][i], x[1][i]), 3)}""")

    print(f"x{tuple([xi[-1] for xi in x])}", sep='\n')
    
if __name__ == '__main__':
    conjugate_gradients()
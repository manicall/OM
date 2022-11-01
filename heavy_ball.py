import sympy as sp
from equals import Equals, MyEnum

def heavy_ball():
    x = [[-1000], [1000]]
    h = 0.4
    a = 0.3
    f = Equals.get_f(MyEnum.cr_ex)

    dx = []
    for i in range(len(x)):
        xi = 'x' + str(i + 1)
        dx.append(sp.lambdify(['x1', 'x2'], sp.diff(Equals.get_ex(), xi)))

    # поиск минимума на начальном этапе (методом наискорейшего спуска)
    def x0():    
        temp_x = []
        for i in range(len(x)):
            # X0 = Xi - h*gradR(Xi)
            # *dx = grad 
            temp_x.append(x[i][-1] - h*dx[i](x[0][-1], x[1][-1]))
        
        for i in range(len(x)):
            x[i].append(temp_x[i])

    # поиск минимума методом тяжелого шарика
    def xi():
        temp_x = []
        for i in range(len(x)):
            #* dx == grad 
            temp_x.append(x[i][-1] - a * (x[i][-1] - x[i][-2]) - h * dx[i](x[0][-1], x[1][-1]))
        
        for i in range(len(x)):
            x[i].append(temp_x[i])
        
    x0()
    for i in range(40): 
        xi()

    print(f"x{tuple([xi[-1] for xi in x])}", sep='\n')
    
if __name__ == '__main__':
    heavy_ball()
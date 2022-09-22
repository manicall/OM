from equals import Equals, MyEnum
import sympy as sp
import math as m

def fastest_descent():
    f = Equals.get_f(MyEnum.gr_first)
    E = 0.01
    x = [[0.5], [0.5]]    
    
    grad = lambda x: m.sqrt(sum([xi**2 for xi in x]))
    
    dx = []
    for i in range(len(x)):
        # xi=0
        param = ['x'+str(i + 1)+'=0' for i in range(len(x))]
        # xi
        xi = 'x'+ str(i + 1)

        dx.append(sp.lambdify(param, str(sp.diff(Equals.get_ex(), xi))))
    
    def iter():
        temp_dx = []
        for i in range(len(x)):
            temp_x = [xi[-1] for xi in x]
            temp_dx.append(dx[i](*temp_x))
        
        # условие остановки
        if grad(temp_dx) < E: 
            return False
        
        # подстановка (x1)
        text = ''
        ex = Equals.get_ex()
        for i in range(len(x)):
            text = (str(x[i][-1]) + " - " + str(temp_dx[i]) + "*d")
            text = text.replace('- -', '+ ')
            ex = ex.replace(f"x{i+1}", f'({text})')
        
        # вычисление шага для текущей итерации   
        try:
            d = round(float(sp.solve(sp.diff(ex, 'd'), 'd')[-1]), 3)
        except:
            d = 0.1
        
        for i in range(len(x)):
            x[i].append(round(x[i][-1] - d * temp_dx[i], 3))

        for i in range(len(temp_dx)):
            print(f"x{i+1}={x[i][-1]}", end=" ")
        for i in range(len(temp_dx)):
            print(f"df/x{i+1}={temp_dx[i]}", end=" ")
            
        l = [xi[-1] for xi in x]
        print(f"R={f(*l)}")

        return True
    
    n = 100
    for i in range(1, n):
        print(f"------------------------Итерация {i}------------------------")
        if not iter(): break
    
    print([xi[-1] for xi in x])

if __name__ == '__main__':
    fastest_descent()
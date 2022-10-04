import sympy as sp     
import numpy as np
import matplotlib.pyplot as plt
from enum import IntEnum
   
# построение графика поверхности
def create_plot(f, sx = 50, sy = 50):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    
    x, y = np.meshgrid(np.linspace(-sx, sx, 100), np.linspace(-sy, sy, 100))
    z = f(x, y)
    ax.plot_surface(x, y, z)
    plt.show()
   
class MyEnum(IntEnum):
    cr_ex = 1
    cd_ex = 2
    gr_ex = 3
    fd_ex = 4
    web_ex = 5
    rosen = 6
   
class Equals:
    ex = None

    equals = {
        MyEnum.cr_ex  : '(x1 - 3)**2 + (5 - x2)**2',
        MyEnum.cd_ex  : 'x1**2 + 36*x2**2',
        MyEnum.gr_ex  : 'x1**3 + 2*x2**2 - 3*x1 - 4*x2',
        MyEnum.fd_ex  : '3*x1**2+x2**2-x1*x2-4*x1',
        MyEnum.web_ex : '2*x1**2 + x2**2 - x1*x2',
        MyEnum.rosen  : '100 * (x2 - x1**2)**2 + (1 - x1)**2'
    }

    @staticmethod
    def set_ex(param):
        if param is None:   
            param = MyEnum.first
            Equals.ex = Equals.switch(param)
        else:
            Equals.ex = Equals.switch(param)

    @staticmethod
    def get_f(param = None):
        Equals.set_ex(param)
        
        print("Текущее уравнение:", Equals.ex)
        return sp.lambdify(('x1', 'x2'), Equals.ex)
    
    @staticmethod
    def get_ex(param = None): 
        if param is not None: 
            Equals.set_ex(param)
        return Equals.ex    

    @classmethod
    def switch(self, param):
        try:
            return self.equals[param]
        except KeyError:
            return None

if __name__ == '__main__':
    create_plot(lambda x1, x2: (x1 - 3) ** 2 + (5 - x2) ** 2)
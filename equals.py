import sympy as sp     
       
class Equals:
    # region attributes
    ex = None
    f1 = None
    f2 = None
    df_dx = None
    df_dy = None
    # endregion

    # region setters
    @staticmethod
    def set_equal_1():
        Equals.ex = '100 * (y - x**2)**2 + (1 - x)**2'
        Equals.f1 = sp.lambdify(('x', 'y'), Equals.ex)
        Equals.f2 = sp.lambdify(('y', 'x'), Equals.ex)
        Equals.df_dx = sp.lambdify(('x', 'y'), sp.diff(Equals.ex, 'x'))
        Equals.df_dy = sp.lambdify(('x', 'y'), sp.diff(Equals.ex, 'y'))

    @staticmethod
    def set_equal_2():
        Equals.ex = 'x1**2 + 36*x2**2'
        Equals.f1 = sp.lambdify(('x1', 'x2'), Equals.ex)
        Equals.f2 = sp.lambdify(('x1', 'x2'), Equals.ex)
        Equals.df_dx = sp.lambdify(('x1', 'x2'), sp.diff(Equals.ex, 'x1'))
        Equals.df_dy = sp.lambdify(('x1', 'x2'), sp.diff(Equals.ex, 'x2'))

    @staticmethod
    def set_equal_3():
        Equals.ex = '2*x1**2 + x2**2 - x1*x2'
        Equals.f1 = sp.lambdify(('x1', 'x2'), Equals.ex)
        Equals.f2 = sp.lambdify(('x1', 'x2'), Equals.ex)
        Equals.df_dx = sp.lambdify(('x1', 'x2'), sp.diff(Equals.ex, "x1"))
        Equals.df_dy = sp.lambdify(('x1', 'x2'), sp.diff(Equals.ex, "x2"))
    # endregion

    # region getters
    

    @staticmethod
    def get_ex(): 
        return Equals.ex

    @staticmethod
    def get_f1(): return Equals.f1
    
    @staticmethod
    def get_f2(): return Equals.f2

    @staticmethod
    def get_df_dx(): return Equals.df_dx

    @staticmethod
    def get_df_dy(): return Equals.df_dy
    #endregion
    
    @staticmethod
    def print_ex(): print(Equals.ex)

if __name__ == '__main__':
    pass
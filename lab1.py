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


def fastest_descent():
    Equals.set_equal_1()
    f1 = Equals.f1
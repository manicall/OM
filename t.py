import sympy as sp

f = 'x1**3 + 2*x2**2 - 3*x1 - 4*x2'

x1 = [-0.5]
x2 = [-1]

dx1 = sp.lambdify('x1', sp.diff(f, 'x1'))
dx2 = sp.lambdify('x2', sp.diff(f, 'x2'))
R = sp.lambdify(('x1','x2'), f)

print(dx1(x1[-1]))
print(dx2(x2[-1]))

print(R(x1[-1], x2[-1]))
import sympy as sp


print(sp.diff('(x1-2)**2-x2**2', 'x1'))
print(sp.diff('(x1-2)**2-x2**2', 'x2'))

print(sp.diff('-1*((L2-2)^2-M2^2)', 'x1'))
print(sp.diff('-1*((L2-2)^2-M2^2)', 'x2'))

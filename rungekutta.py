import sympy
from math import tan, e, cos, sin
import decimal
from decimal import Decimal
import matplotlib.pyplot as plt


class R4K:
    def __init__(self, h, *functions):
        self.h = h
        self.functions = functions
        self.vars = None
        self.t = 0

    def set_init_vars(self, *args):
        self.t = args[0]
        self.vars = list(args[1:])

    def coeffs(self):
        h = self.h
        ks1 = [f(self.t, *self.vars) for f in self.functions]
        ks2 = [f(self.t + h/2, *[v + h*(k/2) for v, k in zip(self.vars, ks1)]) for f in self.functions]
        ks3 = [f(self.t + h/2, *[v + h*(k/2) for v, k in zip(self.vars, ks2)]) for f in self.functions]
        ks4 = [f(self.t + h, *[v + h*k for v, k in zip(self.vars, ks3)]) for f in self.functions]

        return list(zip(ks1, ks2, ks3, ks4))

    def new_var(self, yn, k1, k2, k3, k4):
        return yn + (1/6)*self.h*(k1 + 2*k2 + 2*k3 + k4)

    def step(self):
        ks = self.coeffs()
        self.t += self.h
        self.vars = [self.new_var(y, *ks) for y, f, ks in zip(self.vars, self.functions, self.coeffs())]

        return [self.t] + self.vars


if __name__ == '__main__':

    f = lambda t, y, yy: yy
    g = lambda t, y, yy: 6*y - yy

    y_0 = 3
    t_0 = 0
    yy_0 = 1
    h = (0.025)

    #rr4k = R4K(0.025, lambda x, y, z: z, lambda x, y, z: 6*y - z)
    #rr4k = R4K(0.025, lambda t, y: tan(y) + 1)
    rr4k = R4K(0.1, lambda t, u1, u2: -4*u1 - 2*u2 + cos(t) + 4*sin(t), lambda t, u1, u2: 3*u1 + u2 - 3*sin(t))


    rr4k.set_init_vars(0, 1, -1)
    class_pts = []
    for _ in range(100):
        n = rr4k.step()
        class_pts.append(tuple(n))

    class_pts = list(zip(*class_pts))
    xs = class_pts[0]
    for i in class_pts[1:]:
        pass


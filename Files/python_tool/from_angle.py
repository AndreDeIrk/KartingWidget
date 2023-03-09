import numpy as np
from matplotlib import pyplot as plt
import math as m

def afin_x(x, y):
    a = 26/60.
    b = 26.8/70.
    c = -15/60.
    d = 22.5/70.
    return a*x + b*y

def afin_y(x, y):
    a = 26/60.
    b = 26.8/70.
    c = -15/60.
    d = 22.5/70.
    return c*x + d*y

X = list([x/10 for x in np.arange(-300, 301, 1)])*2
Y = list([35] * 601) + list([-35] * 601)
angle = np.arange(0, np.pi, 0.01)
Y += list([35 * np.cos(ang) for ang in angle])
X += list([30 + 35 * np.sin(ang) for ang in angle])

Y += list([-35 * np.cos(ang) for ang in angle])
X += list([-30 - 35 * np.sin(ang) for ang in angle])

X_new = list([afin_x(x, y) for x, y in zip(X, Y)])
Y_new = list([afin_y(x, y) for x, y in zip(X, Y)])

Angle = list([((m.atan2(y, x) - m.atan2(-35, 30)) / 3.1415 * 180) % 360 for x, y in zip(X, Y)])

sorted_lists = sorted(zip(Angle, X, Y))

Angle = list([elem[0] for elem in sorted_lists])
X = list([elem[1] for elem in sorted_lists])
Y = list([elem[2] for elem in sorted_lists])

def from_angle(angle):
    x, y = np.interp(angle, Angle, X), np.interp(angle, Angle, Y)
    return afin_x(x, y) * 5, afin_y(x, y) * 5
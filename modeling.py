import numpy as np


def polar(x, y):
    if x == 0:
        if y > 0:
            return np.pi / 2
        else:
            return 3 * np.pi / 2
    else:
        if y > 0:
            if x > 0:
                return np.arctan(y / x)
            else:
                return np.arctan(y/x) + np.pi
        else:
            if x > 0:
                return np.arctan(y / x) + 2*np.pi
            else:
                return np.arctan(y/x) + np.pi


def is_inside(x, v, a, k, T):
    return x < a and -a < x


def has_enough_time_to_enter(x, v, time_left, a, k, T):
    return (x > a and v < 0 and (a-x) / v < time_left) or (x < -a and v > 0 and (-a - x) / v < time_left)


def time_to_enter(x, v, time_left, a, k, T):
    if x > a:
        return (a-x) / v
    else:
        return (-a-x) / v


def is_bounded(x, v, a, k, T):
    return k * a ** 2 > k * x ** 2 + v**2


def exit_point(x, v, a, k, T):
    if v > 0:
        return a, np.power(k * x ** 2 + v**2 - k * a**2, 0.5)
    else:
        return -1 * a, -1 * np.power(k * x ** 2 + v**2 - k * a**2, 0.5)


def enter_point(x, v, time_left, a, k, T):
    if x > 0:
        return a, v
    else:
        return -a, v


def hieght_widht(x, v, a, k, T):
    return np.power(x ** 2 + v**2 / k, 0.5), np.power(k * x ** 2 + v**2, 0.5)


def turning_time_to_exit(x, v, a, k, T):
    x2, v2 = exit_point(x, v, a, k, T)
    w = np.power(k, 0.5)
    v = v / w
    v2 = v2 / w
    a1 = polar(x, v)
    a2 = polar(x2, v2)
    t = (a1 - a2) / w
    return t


def has_enough_time_to_exit(x, v, time_left, a, k, T):
    t = turning_time_to_exit(x, v, a, k, T)
    return time_left > t


def full_rotation(x, v, time_left, a, k, T):
    return time_left > 2 * np.pi / np.power(k, 0.5)


def turn(x, v, t,  a, k, T):
    w = np.power(k, 0.5)
    return x * np.cos(w * t) + (v / w) * np.sin(w * t), - w*x * np.sin(w * t) + v * np.cos(w * t)


def forward(x, v, t, a, k, T):
    return x + t * v, v

def teleport(x,v, val):
    return x, v + val



def exit_time(a, k, T, x, v):
    if is_inside(a, k, T, x, v):
        if is_bounded(a, k, T, x, v):
            return T/2
        else:
            pass
    else:
        return 0

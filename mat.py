import numpy
import math


def translate(x, y, z):
    raw = [[1, 0, 0, x],
           [0, 1, 0, y],
           [0, 0, 1, z],
           [0, 0, 0, 1]]
    return numpy.array(raw, dtype='f4')


def scale(x, y, z):
    raw = [[x, 0, 0, 0],
           [0, y, 0, 0],
           [0, 0, z, 0],
           [0, 0, 0, 1]]
    return numpy.array(raw, dtype='f4')


def rotate(a, x0, y0, z0):
    norm = math.sqrt(x0 ** 2 + y0 ** 2 + z0 ** 2)
    x = x0 / norm
    y = y0 / norm
    z = z0 / norm

    xy = x * y
    yz = y * z
    xz = x * z

    x2 = x * x
    y2 = y * y
    z2 = z * z

    sa = math.sin(a)
    ca = math.cos(a)
    nca = 1 - math.cos(a)
    raw = [[nca * x2 + ca, nca * xy - sa * z, nca * xz + sa * y, 0],
           [nca * xy + sa * z, nca * y2 + ca, nca * yz - sa * x, 0],
           [nca * xz - sa * y, nca * yz + sa * x, nca * z2 + ca, 0],
           [0, 0, 0, 1]]
    return numpy.array(raw, dtype='f4')

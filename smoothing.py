import math
import scipy.optimize.optimize as opt
from scipy.optimize import minimize


def check(x1, y1, x2, y2, x3, y3):
    eps = 1
    _x1 = (x2 - x1)
    _x2 = (x2 - x3)
    _y1 = (y2 - y1)
    _y2 = (y2 - y3)
    pseudoscalar = _x1 * _y2 - _x2 * _y1
    length_1 = math.sqrt(_x1 * _x1 + _y1 * _y1)
    length_2 = math.sqrt(_x2 * _x2 + _y2 * _y2)
    tst = math.asin(abs(pseudoscalar / (length_1 * length_2))) * 180 / math.pi
    return tst > eps


def go(points):
    count = 0
    for j in range(len(points[0])):
        for i in range(1, len(points[0][j]) - 1):
            if ((check(points[0][j][i - 1], points[1][j][i - 1], points[0][j][i], points[1][j][i], points[0][j][i + 1],
                       points[1][j][i + 1]))):
                if (points[2][j][i - 1] < 0):
                    count += 1
                    points[2][j][i - 1] = count
                    points[2][j][i] = count
                    points[2][j][i + 1] = count
                elif (points[2][j][i] > 0):
                    points[2][j][i + 1] = points[2][j][i]
                else:
                    count += 1
                    points[2][j][i] = count
                    points[2][j][i + 1] = count
                if (i > 1):
                    if (points[2][j][i - 2] < 0):
                        points[2][j][i - 2] = 0
            if (points[2][j][len(points[2][j]) - 3] < 0):
                points[2][j][len(points[2][j]) - 3] = 0
            if (points[2][j][len(points[2][j]) - 2] < 0):
                points[2][j][len(points[2][j]) - 2] = 0
            if (points[2][j][len(points[2][j]) - 1] < 0):
                points[2][j][len(points[2][j]) - 1] = 0
    return points


def get_spline(nodes):



def get_points(points, road, start, stop):
    result = []
    for i in range(start=start, stop=stop):
        result.append([points[0][road][i], points[1][road][i]])
    return result


def extract(points):
    result = []
    for i in range(len(points[0])):
        road = []
        j = 0
        while j < len(points[0][i]):
            if points[2][i][j] <= 0:
                road.append(get_spline(get_points(points, i, j, j + 1)))
                j = j + 1
                if i + 1 == len(points[0]):
                    break
            else:
                k = j
                while points[2][i][j] == points[i][k]:
                    if k + 1 == len(points[2][i][j]):
                        break
                    else:
                        k = k + 1
                road.append(get_spline(get_points(points, i, j, k)))
                j = k
        result.append(road)
    return result

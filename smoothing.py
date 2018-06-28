import math
import numpy as np
import genetic
import matplotlib.pyplot as plt


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
                if points[2][j][i - 1] < 0:
                    count += 1
                    points[2][j][i - 1] = count
                    points[2][j][i] = count
                    points[2][j][i + 1] = count
                elif points[2][j][i] > 0:
                    points[2][j][i + 1] = points[2][j][i]
                else:
                    count += 1
                    points[2][j][i] = count
                    points[2][j][i + 1] = count
                if i > 1:
                    if points[2][j][i - 2] < 0:
                        points[2][j][i - 2] = 0
            if points[2][j][len(points[2][j]) - 3] < 0:
                points[2][j][len(points[2][j]) - 3] = 0
            if points[2][j][len(points[2][j]) - 2] < 0:
                points[2][j][len(points[2][j]) - 2] = 0
            if points[2][j][len(points[2][j]) - 1] < 0:
                points[2][j][len(points[2][j]) - 1] = 0
    return points


def e_func(s, p):
    sum = 0
    for i in range(len(p)):
        sum = sum + p[i] * math.pow(s, i)
    return sum


def get_b(nodes):
    p0x = nodes[0][0]
    p0y = nodes[0][1]
    pnx = nodes[len(nodes) - 1][0]
    pny = nodes[len(nodes) - 1][1]
    return [pnx - p0x, pny - p0y]


def get_spline(nodes):
    p0x = nodes[0][0]
    p0y = nodes[0][1]
    sn = get_sn(nodes)
    points = get_random_points(20000)
    points = get_projections(points, [sn, sn], get_b(nodes))
    pVectors = get_PVectors(points)
    best_points = genetic.get_coeff(pVectors, nodes, 100)
    return best_points


def get_projections(points, sn, b):
    for i in range(len(points)):
        for k in range(len(points[i])):
            part = (sn[k] * points[i][k][0] + sn[k] * sn[k] * points[i][k][1] + sn[k] * sn[k] * sn[k] * points[i][k][2])
            if part != 0:
                coeff = b[k] / part
            else:
                coeff = 0
            for j in range(len(points[i][k])):
                if coeff != 0:
                    points[i][k][j] = points[i][k][j] * coeff
    return points


def get_PVectors(points):
    pVectors = []
    for i in range(len(points)):
        pVector = []
        for j in range(len(points[i][0])):
            p = [points[i][0][j], points[i][1][j]]
            pVector.append(p)
        pVectors.append(pVector)
    return pVectors


def get_CommonVectors(points):
    commonVectors = []
    for i in range(len(points)):
        commonVector = []
        common1 = [points[i][0][0], points[i][1][0], points[i][2][0]]
        common2 = [points[i][0][1], points[i][1][1], points[i][2][1]]
        commonVector.append(common1)
        commonVector.append(common2)
        commonVectors.append(commonVector)
    return commonVectors


def get_random_points(length):
    points = []
    for i in range(length):
        point = []
        point.append([np.random.randint(-100, 100), np.random.randint(-100, 100), np.random.randint(-100, 100)])
        point.append([np.random.randint(-100, 100), np.random.randint(-100, 100), np.random.randint(-100, 100)])
        points.append(point)
    return points


def get_sn(way, n=None):
    if n == None:
        n = len(way)
    sn = 0
    for i in range(n - 1):
        sn = sn + get_dist(way[i], way[i + 1])
    return sn


def get_dist(pt1, pt2):
    return math.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)


def get_points(points, road, start, stop):
    result = []
    print("road {2} stop {0} start {1}".format(stop, start, road))
    for i in range(start, stop):
        result.append([points[0][road][i], points[1][road][i]])
    return result


def extract(points):
    result = []
    for i in range(len(points[0])):
        road = []
        j = 0
        while j + 1 < len(points[0][i]):
            if points[2][i][j] <= 0:
                pts = get_points(points, i, j, j + 1)
                spline = get_spline(pts)
                draw_spline(spline, get_sn(pts), 0.01, pts)
                road.append(spline)
                j = j + 1
                if i + 1 == len(points[0]):
                    break
            else:
                k = j
                while points[2][i][j] == points[2][i][k]:
                    if k + 1 == len(points[2][i]):
                        break
                    else:
                        k = k + 1
                pts = get_points(points, i, j, k)
                spline = get_spline(pts)
                draw_spline(spline, get_sn(pts), 0.5, pts)
                road.append(spline)
                j = k
        result.append(road)
    return result


def draw_spline(spline, sn, step, pts=None):
    s0 = 0
    print(sn)

    print(pts)
    while s0 + step <= sn:
        val_x1, val_y1 = get_xy(spline, s0)
        val_x2, val_y2 = get_xy(spline, s0+step)
        s0 = s0 + step
        plt.plot([val_x1,val_x2], [val_y1,val_y2],color="r")
    #print(get_xy(spline, s0))
    if pts != None:
        x = [pt[0] for pt in pts]
        y = [pt[1] for pt in pts]
        print(x)
        print(y)
        plt.plot(x, y)
    plt.show()


def get_xy(spline, s):
    val_x = 0
    val_y = 0
    for i in range(len(spline)):
        val_x = val_x + math.pow(s, i) * spline[i][0]
        val_y = val_y + math.pow(s, i) * spline[i][1]
        # val_y = val_y + 2*spline[0][1]
    print(val_x, val_y)
    return val_x, val_y

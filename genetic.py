import random as rnd
import math
import smoothing
import copy
import matplotlib.pyplot as plt


def e_func(p):
    final_sum = 0
    p_copy = [el for el in p]
    p_copy.insert(0, way_points[0])
    for j in range(1, len(way_points) - 1):
        sum_x = 0
        sum_y = 0
        for i in range(len(p_copy)):
            way_x = [el[0] for el in way_points]
            way_y = [el[1] for el in way_points]
            sum_x = sum_x + p_copy[i][0] * math.pow(smoothing.get_sn(way_points, i), i)
            sum_y = sum_y + p_copy[i][1] * math.pow(smoothing.get_sn(way_points, i), i)
        sumv = abs(sum_x - way_x[j])
        sumv = sumv + abs(sum_y - way_y[j])
        final_sum = final_sum + sumv
    return final_sum


def func(x):
    return e_func(x)


def cross(point1, point2):
    new_points = [[], []]
    new_points[0].append(point2[0])
    new_points[1].append(point1[0])
    new_points[0].append(point1[1])
    new_points[1].append(point2[1])
    new_points[0].append(point2[2])
    new_points[1].append(point1[2])
    return new_points


def selection(values):
    values.sort(key=lambda x: func(x))
    new_arr = values[0:n]
    return new_arr


def mutate1(values):
    new_values = copy.deepcopy(values)
    for i in range(1, len(values)):
        for j in range(len(values[i])):
            for k in range(len(values[i][j])):
                new_values[i][j][k] = new_values[i][j][k] + rnd.uniform(-mutate_coef, mutate_coef)
    new_values = smoothing.get_CommonVectors(new_values)
    new_values = smoothing.get_projections(new_values, [smoothing.get_sn(way_points), smoothing.get_sn(way_points)],
                                           smoothing.get_b(way_points))
    new_values = smoothing.get_PVectors(new_values)
    values.extend(new_values)
    return values


def mutate(values):
    res = [copy.deepcopy(values[0])]
    for i in range(1, len(values)):
        for j in range(len(values[i])):
            for k in range(len(values[i][j])):
                values[i][j][k] = values[i][j][k] + rnd.uniform(-mutate_coef, mutate_coef)

    values = smoothing.get_CommonVectors(values)
    values = smoothing.get_projections(values, [smoothing.get_sn(way_points), smoothing.get_sn(way_points)],
                                       smoothing.get_b(way_points))
    values = smoothing.get_PVectors(values)
    res.extend(values)
    return res


def opt_creacher(dot):
    d = 0.0001  # Дельта для поиска производной
    step = 2

    antiGrad = []

    ans = copy.deepcopy(dot)

    for index in range(len(dot)):
        ant = []
        for j in range(len(dot[index])):
            tmp_dot_left = copy.deepcopy(dot)
            tmp_dot_right = copy.deepcopy(dot)
            tmp_dot_right[index][j] += d
            tmp_dot_left[index][j] -= d
            grad = func(tmp_dot_right) - func(tmp_dot_left)
            grad /= 2.0
            ant.append(-grad)
        antiGrad.append(ant)

    for index in range(len(dot)):
        for j in range(len(dot[index])):
            ans[index][j] += step * antiGrad[index][j]
    return ans


def opt_pop(sample):
    l = len(sample)
    for index in range(l):
        sample.append(opt_creacher(sample[index]))
    return sample


def get_coeff(values, way, mutate_coeff=0.1, iterations_num=10000):
    global mutate_coef, way_points, n
    way_points = way
    mutate_coef = mutate_coeff
    n = len(way_points)
    unchenged_iterations_num = 0
    best = values[0]
    for j in range(iterations_num):
        #for i in range(len(values) - 1):
        #    children = cross(values[i], values[i + 1])
        #    values.append(children[0])
        #    values.append(children[1])
        values=opt_pop(values)
        #values = mutate(values)
        values = smoothing.get_CommonVectors(values)
        values = smoothing.get_projections(values, [smoothing.get_sn(way_points), smoothing.get_sn(way_points)],
                                           smoothing.get_b(way_points))
        values = smoothing.get_PVectors(values)
        values = selection(values)
        if abs(func(best) - func(values[0])) < 1e-20:
            unchenged_iterations_num = unchenged_iterations_num + 1
        else:
            unchenged_iterations_num = 0
            best = copy.deepcopy(values[0])
        if (unchenged_iterations_num == 1000) & (func(best) < 5):
            print(j)
            break
        #draw_spline(values[0], smoothing.get_sn(way_points), 0.1, way_points)
    print("values[0]={0}".format(values[0]))
    print(func(values[0]))
    values[0].insert(0, way_points[0])
    print("values[0]={0}".format(values[0]))
    return values[0]


def draw_spline(spline, sn, step, pts):
    s0 = 0
    print(sn)
    print(pts)
    while s0 + step <= sn:
        val_x1, val_y1 = get_xy(spline, s0)
        val_x2, val_y2 = get_xy(spline, s0 + step)
        s0 = s0 + step
        plt.plot([val_x1, val_x2], [val_y1, val_y2])
    plt.plot([pt[0] for pt in pts], [pt[1] for pt in pts])
    plt.show()


def get_xy(spline, s):
    val_x = 0
    val_y = 0
    print(spline)
    for i in range(len(spline)):
        val_x = val_x + math.pow(s, i) * spline[i][0]
        val_y = val_y + math.pow(s, i) * spline[i][1]
    print(val_x,val_y)
    return val_x, val_y

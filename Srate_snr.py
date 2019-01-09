# coding=utf-8

# Description: None
# todo: Resolve the success rate of downlink pkt using SNR.
#                        ---By Gcj

import xlrd
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize


# 01.打开excel文件,创建一个文件数据对象
data = xlrd.open_workbook('C:/Users/Gu/Desktop/Python/LoRaWANDownload/data.xlsx')

# 02.获取一张表
table = data.sheets()[2]  # 1.通过索引获取

# 03.获取行或者列的值(数组)
x1 = table.row_values(0, start_colx=0, end_colx=11)  # 获取行,限制列
y1 = table.row_values(1, start_colx=0, end_colx=11)
x2 = table.row_values(2, start_colx=0, end_colx=14)  # 获取行,限制列
y2 = table.row_values(3, start_colx=0, end_colx=14)
x3 = table.row_values(4, start_colx=0, end_colx=7)  # 获取行,限制列
y3 = table.row_values(5, start_colx=0, end_colx=7)
x4 = table.row_values(6, start_colx=0, end_colx=8)  # 获取行,限制列
y4 = table.row_values(7, start_colx=0, end_colx=8)
x5 = table.row_values(8, start_colx=0, end_colx=11)  # 获取行,限制列
y5 = table.row_values(9, start_colx=0, end_colx=11)
x6 = table.row_values(10, start_colx=0, end_colx=10)  # 获取行,限制列
y6 = table.row_values(11, start_colx=0, end_colx=10)

# 04.定义指数方程函数
def f_power(x, a, c):
    return a * pow(3.825, -x) + c


# 05.线性回归
def plot_test():
    plt.figure()

    # 拟合点
    #x2 = [-3, -4, -5, -6, -6.5, -7.2720, -7.3489, -7.6211, -7.7013, -8.1077, -8.5275, -9.0053]
    #y2 = [0, 0, 0, 0, 0, 7, 6, 10, 21, 35, 60, 81]

    #x0 = [7.3, 7.4, 7.6, 7.7, 8.1]
    #y0 = [0.07, 0.06, 0.10, 0.21, 0.35]

    #x0 = [1, 2, 3, 4, 5]
    #y0 = [1, 3, 8, 18, 36]
    # 绘制散点
    plt.scatter(x1, y1, 25, "red")
    plt.scatter(x2, y2, 25, "orange")
    plt.scatter(x3, y3, 25, "yellow")
    plt.scatter(x4, y4, 25, "green")
    plt.scatter(x5, y5, 25, "blue")
    plt.scatter(x6, y6, 25, "purple")


    # 直线拟合与绘制
    a1, c1 = optimize.curve_fit(f_power, x1, y1, maxfev=500000)[0]
    print(a1,3.825,c1)
    xx1 = np.arange(-12, 0, 0.1)
    yy1 = a1 * pow(3.825, -xx1) + c1
    plt.plot(xx1, yy1, "red")

    a2, c2 = optimize.curve_fit(f_power, x2, y2, maxfev=500000)[0]
    print(a2,3.825,c2)
    xx2 = np.arange(-12, 0, 0.1)
    yy2 = a2 * pow(3.825, -xx2) + c2
    plt.plot(xx2, yy2, "orange")

    a3, c3 = optimize.curve_fit(f_power, x3, y3, maxfev=500000)[0]
    print(a3,3.825,c3)
    xx3 = np.arange(-14, 0, 0.1)
    yy3 = a3 * pow(3.825, -xx3) + c3
    plt.plot(xx3, yy3, "yellow")

    a4, c4 = optimize.curve_fit(f_power, x4, y4, maxfev=500000)[0]
    print(a4,3.825,c4)
    xx4 = np.arange(-18, 0, 0.1)
    yy4 = a4 * pow(3.825, -xx4) + c4
    plt.plot(xx4, yy4, "green")

    a5, c5 = optimize.curve_fit(f_power, x5, y5, maxfev=500000)[0]
    print(a5,3.825,c5)
    xx5 = np.arange(-18, 0, 0.1)
    yy5 = a5 * pow(3.825, -xx5) + c5
    plt.plot(xx5, yy5, "blue")

    a6, c6 = optimize.curve_fit(f_power, x6, y6, maxfev=500000)[0]
    print(a6,3.825,c6)
    xx6 = np.arange(-22, 0, 0.1)
    yy6 = a6 * pow(3.825, -xx6) + c6
    plt.plot(xx6, yy6, "purple")

    plt.title("test")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(-22, 0)
    plt.ylim(-0.01,1.2)
    plt.show()

    return
plot_test()


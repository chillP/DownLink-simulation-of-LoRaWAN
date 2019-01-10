# coding=utf-8

# Description: None
# Todo:模拟网关与节点，验证多路径下行算法
#                        ---By Gcj

import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from Downlink import test_fun

# ***参数配置表*** #
# |数量定义|
num_node = 1500 # 节点数量
num_gw = 5  # 网关数量

# |随机分布类型|
random_type = 'uniform'  # 随机类型（高斯分布or均匀分布 gaussian/uniform）
algorithm_type = '3'       # 多路径下行算法（1.仅信号质量 2.得分加权求和 3.）

# |网关参数|
gw_para = np.array([[0, 28], [0, 37], [0, 124], [0, 24], [0, 22]], dtype=np.float)  # 网关参数列表[网关负载%, 网络延时ms]

# ******end****** #



gw_x = np.zeros((num_gw, 1))
gw_y = np.zeros((num_gw, 1))
node_x = np.zeros((num_node, 1))
node_y = np.zeros((num_node, 1))
node_SF = np.zeros((num_node, 1))
GwList = np.zeros((num_gw, 2))
NodeList = np.zeros((num_node, 2))
ping = np.zeros((num_gw, 1))
load = np.zeros((num_gw, 1))
score = np.zeros((num_node,num_gw))
P_snr = np.zeros((num_node,num_gw))
color = []
color_dot = ['y.', 'g.', 'm.', 'b.', 'c.']
colors = ['r', 'y', 'g', 'b', 'r', 'y', 'g', 'b', 'r']

# 随机生成网关和节点位置
# 高斯分布
if random_type == 'gaussian':
    node_x = np.random.normal(scale=0.5, size=num_node)*100  # 高斯分布
    node_y = np.random.normal(scale=0.5, size=num_node)*100
    gw_x = np.random.normal(scale=1, size=num_gw)*60
    gw_y = np.random.normal(scale=1, size=num_gw)*60
    # 存储节点到列表
    NodeList[:, 0] = node_x
    NodeList[:, 1] = node_y
    # 存储网关到列表
    GwList[:, 0] = gw_x
    GwList[:, 1] = gw_y

# 均匀分布
if random_type == 'uniform':
    # 生成节点列表
    NodeList = np.random.sample((num_node, 2))  # 生成x行y列的随机数组  均匀分布
    node_x = NodeList[:, 0]  # 取第一列
    node_y = NodeList[:, 1]  # 取第二列
    # 生成网关列表
    GwList = np.random.sample((num_gw, 2))
    gw_x = GwList[:, 0]
    gw_y = GwList[:, 1]


# 创建坐标系
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


# 选择下行的网关
# 算法1：根据信号质量
if algorithm_type == '1':
    for i in range(0, num_node, 1):
        dist = np.sqrt(np.sum(np.square(GwList-NodeList[i]), axis=1))  # 二维坐标距离计算
        dist = dist.tolist()  # 当前节点与所有网关的距离
        mindist = dist.index(min(dist))  # 最短路径列表（数组索引值，即网关编号）
        color.append(color_dot[mindist])  # 生成颜色列表
        ax1.plot(node_x[i], node_y[i], color[i])  # 绘制节点
    # ax1.scatter(node_x, node_y, c=color, label=mindist)  # 绘制节点
    plt.legend()

# 算法2：得分加权求和
if algorithm_type == '2':
    for i in range(0, num_node, 1):
        #                          **** 获取输入参数 ****
        # 信号质量
        dist = np.sqrt(np.sum(np.square(GwList-NodeList[i]), axis=1))  # 二维坐标距离计算
        # 网络延时
        ping = gw_para[:, 1]
        # 网关负载
        load = gw_para[:, 0]
        #                          **** 数据限幅、归一化 ****
        for j in range(0,num_gw,1):
            if(load[j] >= 30): load[j] = 30
            if(ping[j] >= 400): ping[j] = 400
        dist1 = dist/np.sqrt(2)
        ping1 = ping/400
        load1 = load/30

        #                           **** 加权求和 ****
        #score[i] = dist1 + ping1 + load1
        score[i] = dist1 + ping1 +2*load1
        scorelist = score[i].tolist()  # 矩阵先转换为列表才能使用index方法返回索引值
        bestgw = scorelist.index(min(scorelist))
        color.append(color_dot[bestgw])  # 生成颜色列表
        ax1.plot(node_x[i], node_y[i], color[i])  # 绘制节点

        #                       **** 计算动态网关负载 ****
        gw_para[bestgw][0] += 0.1

# 算法3：自创算法
if algorithm_type == '3':
    for i in range(0, num_node, 1):
        #                          **** 获取输入参数 ****
        # 信号质量
        dist = np.sqrt(np.sum(np.square(GwList - NodeList[i]), axis=1))  # 二维坐标距离计算
        # 网络延时
        ping = gw_para[:, 1]
        # 网关负载
        load = gw_para[:, 0]
        #                         **** 数据限幅 ****
        for j in range(0, num_gw, 1):
            if (load[j] >= 100): load[j] = 100
            if (ping[j] >= 5000): ping[j] = 5000

        #                      **** 坐标距离 -> SNR转换 ****
        snr1 = (dist * 30 / np.sqrt(2)) - 15  # 坐标距离转换为SNR,范围[-15，+15]

        #                       **** 分布执行算法 ****
        # 1、通过Ping的限制筛选网关

        # 2、筛选出信号质量优的网关，若无，跳出，直接选相对较优者下行

        # 3、在信号质量优的网关中，上下行占空比相加，择小者下行

        P_snr = 1-(0.00000001046 * pow(3.825, -snr1))  # 带入线性回归曲线

        # 根据Ping计算成功率
        if(ping1 <= 450 ):
            P_ping = 1
        else:
            P_ping = 0

        # 根据Load计算成功率


        P_all = P_snr * 1
        P_all_list = P_all.tolist()  # 矩阵先转换为列表才能使用index方法返回索引值
        bestgw = P_all_list.index(min(P_all_list))
        color.append(color_dot[bestgw])  # 生成颜色列表
        ax1.plot(node_x[i], node_y[i], color[i])  # 绘制节点


        #                       **** 计算动态网关负载 ****
        gw_para[bestgw][0] += 0.1


# 绘制网关
ax1.plot(gw_x, gw_y, 'rD')
for i in range(0, num_gw, 1):
    plt.annotate(gw_para[i], xy=GwList[i], xytext=GwList[i], arrowprops=dict(facecolor='red'), fontsize=15)
plt.show()


# 打印网关参数表
print_table = PrettyTable(["网关编号", "负载(%)", "网络延时(ms)"])  # Title
for i in range(0, 5):
    print_table.add_row([i+1, gw_para[i][0], gw_para[i][1]])
print(print_table)

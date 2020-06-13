#!/usr/bin/env python
# encoding: utf-8
"""
@author: BakerPeril
@contact: bakerperil@163.com
@software: python3.7
@time: 2020-06-12 23:33
"""
import pandas as pd
import networkx as nx
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt


# 数据加载
emails = pd.read_csv("./input/Emails.csv")
# 读取别名文件
file = pd.read_csv("./input/Aliases.csv")
aliases = {}
for index, row in file.iterrows():
    aliases[row['Alias']] = row['PersonId']
# 读取人名文件
file = pd.read_csv("./input/Persons.csv")
persons = {}
for index, row in file.iterrows():
    persons[row['Id']] = row['Name']


# 针对别名进行转换
# --主要有两点针对emails中的MetadataFrom和MetadataTo的数据格式
# --还将别名进行转换成人名
def unify_name(name):
    #  姓名统一小写
    name = str(name).lower()
    #  去掉，和@后面的内容
    name = name.replace(",", "").split("@")[0]
    # 别名转换
    if name in aliases.keys():
        return persons[aliases[name]]
    return name


# 画网络图
def show_graph(graph):
    # 使用Spring Layout布局，类似中心放射状
    positions = nx.spring_layout(graph)
    # 设置网络图中的节点，大小与pager_ank值相关，
    # 因为page_rank值很小所以需要*20000
    node_size = [x['page_rank']*20000 for v, x in graph.nodes(data=True)]
    # 设置网络图中的边长度
    edge_size1 = [np.sqrt(e[2]['weight']) for e in graph.edges(data=True)]
    # 绘制节点
    nx.draw_networkx_nodes(graph, positions, node_size=node_size, alpha=0.4)
    # 绘制边
    nx.draw_networkx_edges(graph, positions, edge_size=edge_size1, alpha=0.2)
    # 绘制节点的label
    nx.draw_networkx_labels(graph, positions, font_size=10)
    # 输出希拉里邮件中所有人物关系图
    plt.show()


# 将寄件人和收件人的姓名进行规范化
emails.MetadataFrom = emails.MetadataFrom.apply(unify_name)
emails.MetadataTo = emails.MetadataTo.apply(unify_name)

# 设置边的权重等于发邮件次数
edges_weights_temp = defaultdict(list)
# 一个新的类似字典的对象。
# defaultdict是内置 dict 类的子类。
# 它重载了一个方法并添加了一个可写的实例变量。其余的功能与 dict 类相同
for row in zip(emails.MetadataFrom, emails.MetadataTo, emails.RawText):
    temp = (row[0], row[1])
    if temp not in edges_weights_temp:
        edges_weights_temp[temp] = 1
    else:
        edges_weights_temp[temp] = edges_weights_temp[temp] + 1

# 转化格式（from, to), weight => from, to, weight
edges_weights = [(key[0], key[1], val) for key, val in edges_weights_temp.items()]

# 创建一个有向图
graph = nx.DiGraph()
# 设置有向图中的路径及权重（from, to, weight）
graph.add_weighted_edges_from(edges_weights)
# 计算每个人(节点)的PR值，并作为节点的pagerank属性
page_rank = nx.pagerank(graph)
# 获取每个节点的page_rank数值
page_rank_list = {node: rank for node, rank in page_rank.items()}
# 将page_rank数值作为节点的属性
nx.set_node_attributes(graph, name='page_rank', values=page_rank_list)
# 画网络图
show_graph(graph)

# 将完整的图谱进行精简
# 设置PR值的阈值，筛选大于阈值的重要核心点
page_rank_threshold = 0.005
# 复制一份计算好的网络图
small_graph = graph.copy()
# 剪掉PR值小于page_rank_threshold的节点
for n, p_rank in graph.nodes(data=True):
    if p_rank['page_rank'] < page_rank_threshold:
        small_graph.remove_node(n)

# 画网络图
show_graph(small_graph)

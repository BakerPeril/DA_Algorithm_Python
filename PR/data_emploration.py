#!/usr/bin/env python
# encoding: utf-8
"""
@author: BakerPeril
@contact: bakerperil@163.com
@software: python3.7
@time: 2020-06-13 9:14
"""
import pandas as pd
import networkx as nx
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

emails = pd.read_csv("./input/Emails.csv")
print(emails.columns)
print(emails.head(10))
print(emails.MetadataFrom[:50])
print(emails.MetadataTo[:50])


# 读取别名文件
file = pd.read_csv("./input/Aliases.csv")
aliases = {}
for index, row in file.iterrows():
    aliases[row['Alias']] = row['PersonId']
    if len(aliases) > 10:
        break
print(aliases)

# 读取人名文件
file = pd.read_csv("./input/Persons.csv")
persons = {}
for index, row in file.iterrows():
    persons[row['Id']] = row['Name']
    if len(persons) > 10:
        break
print(persons)

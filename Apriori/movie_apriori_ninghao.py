#!/usr/bin/env python
# encoding: utf-8
"""
@author: BakerPeril
@contact: bakerperil@163.com
@software: python3.7
@time: 2020-06-30 21:11
"""
from efficient_apriori import apriori
import csv
director = u'宁浩'
file_name = './' + director + '.csv'
lists = csv.reader(open(file_name, 'r', encoding='utf-8-sig'))

# 数据加载
data = []
for names in lists:
    name_new = []
    for name in names:
        # 去掉演员数据中的空格
        name_new.append(name.strip())
    data.append(name_new[1:])

print(data)
# 挖掘频繁项集和关联规则
itemsets, rules = apriori(data, min_support=0.2, min_confidence=1)
print(itemsets)
print('\r')
print(rules)
# 极客时间上项目出现是2019年，今年是2020年，所以相比之前的爬取多了4条数据，这时候是需要调小 一下最小支持度才可能得出相应的结果

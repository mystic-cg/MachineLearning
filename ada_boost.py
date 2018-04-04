#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by PyCharm
# @author  : mystic
# @date    : 2018/4/2 19:10

"""
    AdaBoost
优点:
    泛化错误率低,易编码,可以应用在大部分分类器上,无参数调整
缺点:
    对离群点敏感
适用数据类型:
    数值型和标称型数据

    一般流程
1.收集数据:
    可以使用任意方法
2.准备数据:
    依赖于所使用的弱分类器类型,本章使用的是单层决策树,这种分类器可以处理任何数据类型
    当然也可以使用任意分类器作为弱分类器,作为弱分类器,简单分类器的效果更好
3.分析数据:
    可以使用任意方法
4.训练算法:
    AdaBoost的大部分时间都用在训练上,分类器将多次在同一条数据集上训练弱分类器
5.测试算法:
    计算分类的错误率
6.使用算法:
    同SVM一样,AdaBoost预测两个类别中的一个
    如果应用到多个类别,需要像多类SVM的做法一样,对AdaBoost进行修改
"""
from numpy import mat


def load_simple_data():
    data_mat = mat([[1., 2.1],
                    [2., 1.1],
                    [1.3, 1.],
                    [1., 1.],
                    [2., 1.]])
    class_label_list = [1.0, 1.0, -1.0, -1.0, 1.0]
    return data_mat, class_label_list
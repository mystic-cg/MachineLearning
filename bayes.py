#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by PyCharm
# @author  : mystic
# @date    : 2017/11/21 20:40
"""
    naive bayes classifier
    优点:
        在数据较少的情况下仍然有效,可以处理多类别问题
    缺点:
        对于输入数据的准备方式较为敏感
    适用数据类型:
        标称型数据
"""
import re

from numpy import *


def load_data_set():
    posting_list = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                    ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                    ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                    ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                    ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                    ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    class_vector = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return posting_list, class_vector


def create_vocabulary_list(data_set):
    # 创建一个空集
    vocabulary_set = set([])
    for document in data_set:
        # 创建两个集合的并集
        vocabulary_set = vocabulary_set | set(document)
    return list(vocabulary_set)


def set_words2vector(vocabulary_list, input_set):
    """
        词集模型
    :param vocabulary_list:
    :param input_set:
    :return:
    """
    return_vector = [0] * len(vocabulary_list)
    for word in input_set:
        if word in vocabulary_list:
            return_vector[vocabulary_list.index(word)] = 1
        else:
            print('The word "%s" is not in my vocabulary!' % word)
    return return_vector


def bag_words2vector(vocabulary_list, input_set):
    """
        词袋模型
    :param vocabulary_list:
    :param input_set:
    :return:
    """
    return_vector = [0] * len(vocabulary_list)
    for word in input_set:
        if word in vocabulary_list:
            return_vector[vocabulary_list.index(word)] += 1
    return return_vector


def train_naive_bayes(train_matrix, train_category):
    # 获取第0维长度,相当于获取数组的行数:6
    num_train_docs = len(train_matrix)
    # print(num_train_docs)
    # print(array(train_matrix).shape[0])
    # 获取第1维长度,相当于获取数组每行的元素数:32
    num_words = len(train_matrix[0])
    # print(num_words)
    # 因为1表示abusive,所有求和,表示abusive的总数
    probability_abusive = sum(train_category) / num_train_docs
    # 统计单词出现的频率,为避免乘数为0,初始化使用ones
    p0_num = ones(num_words)
    p1_num = ones(num_words)
    # 统计not abusive的数量
    p0_denominator = 2.0
    # 统计abusive的数量
    p1_denominator = 2.0
    # 遍历训练文档,分别统计abusive和not abusive的总数
    for i in range(num_train_docs):
        if train_category[i] == 1:
            # 统计每个属于abusive单词的出现次数
            p1_num += train_matrix[i]
            p1_denominator += sum(train_matrix[i])
        else:
            # 统计每个属于not abusive单词的出现次数
            p0_num += train_matrix[i]
            p0_denominator += sum(train_matrix[i])
    # 统计每个单词在各自分类中,出现的概率
    # p1_vector = p1_num/p1_denominator
    # p0_vector = p0_num/p0_denominator
    # 为避免下溢出(很多很小的数相乘,程序可能会返回0),取对数
    p1_vector = log(p1_num / p1_denominator)
    p0_vector = log(p0_num / p0_denominator)
    return p0_vector, p1_vector, probability_abusive


def classify_naive_bayes(vector2classify, p0_vector, p1_vector, p_class1):
    """
        朴素的贝叶斯分类器
    :param vector2classify: 用于分类的向量
    :param p0_vector: not abusive的概率
    :param p1_vector: abusive的概率
    :param p_class1:
    :return:
    """
    p1 = sum(vector2classify * p1_vector) + log(p_class1)
    p0 = sum(vector2classify * p0_vector) + log(1.0 - p_class1)
    if p1 > p0:
        return 1
    return 0


def text_parse(big_str):
    list_tokens = re.split(r'\W*', big_str)
    return [token.lower() for token in list_tokens if len(token) > 2]


def spam_test():
    doc_list = []
    class_list = []
    full_text = []
    for i in range(1, 26):
        word_list = text_parse(open('resource/email/spam/%d.txt' % i).read())
        doc_list.append(word_list)
        full_text.append(word_list)
        class_list.append(1)
        word_list = text_parse(open('resource/email/ham/%d.txt' % i).read())
        doc_list.append(word_list)
        full_text.append(word_list)
        class_list.append(0)
    vocabulary_list = create_vocabulary_list(doc_list)
    train_set = range(50)
    test_set = []
    for i in range(10):
        random_index = int(random.uniform(0, len(train_set)))
        test_set.append(train_set[random_index])
        del(train_set[random_index])
    train_matrix = []
    train_classes = []
    for doc_idx in train_set:
        train_matrix.append(set_words2vector(vocabulary_list, doc_list[doc_idx]))
        train_classes.append(class_list[doc_idx])
    p0_vector, p1_vector, p_spam = train_naive_bayes(train_matrix, train_classes)
    error_count = 0
    for doc_idx in test_set:
        word_vector = set_words2vector(vocabulary_list, doc_list[doc_idx])
        if classify_naive_bayes(word_vector, p0_vector, p1_vector, p_spam) != class_list[doc_idx]:
            error_count += 1
    print('The error rate is ', error_count/len(test_set))


if __name__ == '__main__':
    list_post, list_class = load_data_set()
    my_vocabulary_list = create_vocabulary_list(list_post)
    # print(my_vocabulary_list)
    # vec = set_words2vector(my_vocabulary_list, list_post[0])
    # print(vec)
    train_mat = []
    for post_in_doc in list_post:
        train_mat.append(set_words2vector(my_vocabulary_list, post_in_doc))
        # print(train_mat)
        # print(shape(train_mat))
    p0_vec, p1_vec, p_abusive = train_naive_bayes(train_mat, list_class)
    # print('=================================================================')
    # print('p0_vec', p0_vec)
    # print('p1_vec:', p1_vec)
    # print('p_abusive:', p_abusive)
    test_entry = ['love', 'my', 'dalmation']
    # test_entry = ['stupid', 'garbage']
    this_doc = set_words2vector(my_vocabulary_list, test_entry)
    print(test_entry, 'classified as: ', classify_naive_bayes(this_doc, p0_vec, p1_vec, p_abusive))

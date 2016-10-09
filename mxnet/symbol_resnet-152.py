#coding=utf-8
__author__ = 'wac'
modified_date = '16/7/13'

import mxnet as mx


def ConvFactory(data, num_filter, kernel, stride=(1,1), pad=(0, 0), act_type="relu"):
    conv = mx.symbol.Convolution(data=data, num_filter=num_filter, kernel=kernel, stride=stride, pad=pad)
    bn = mx.symbol.BatchNorm(data=conv)
    act = mx.symbol.Activation(data = bn, act_type=act_type)
    return act

def ResidualFactory(data):
    l1 = ConvFactory(data, 32, kernel=(3,3), pad=(1,1))
    l2 = ConvFactory(l1, 32, kernel=(3,3), pad=(1,1))
    return l2 + data


def get_symbol(num_classes = 10):
    data = mx.symbol.Variable(name="data")
    o = ConvFactory(data=data, kernel=(3,3), pad=(1,1), num_filter=32, act_type="relu")
    for i in range(152):
        o = ResidualFactory(o)
    pool = mx.symbol.Pooling(data=o, pool_type="avg", kernel=(8,8), pad=(1, 1), name="global_pool")

    flatten = mx.symbol.Flatten(data=pool, name="flatten1")

    fc = mx.symbol.FullyConnected(data=flatten, num_hidden=num_classes, name="fc1")

    label = mx.symbol.Variable("softmax_label")
    softmax = mx.symbol.SoftmaxOutput(data=fc, name="softmax", label=label)
    return softmax
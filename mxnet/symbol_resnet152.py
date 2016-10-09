"""
For image size of 299*299
References:
Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun. "Deep Residual Learning for Image Recognition"

"""

import find_mxnet
assert find_mxnet
import mxnet as mx

def Conv(data, num_filter, kernel=(1, 1), stride=(1, 1), pad=(0, 0), name=None):
    conv = mx.sym.Convolution(data=data, num_filter=num_filter, kernel=kernel, stride=stride, pad=pad, no_bias=True,
                              name='%s_conv'%name)
    bn = mx.sym.BatchNorm(data=conv, name='%s_batchnorm' %name, fix_gamma=True)
    act = mx.sym.Activation(data=bn, act_type='relu', name='%s_relu' %name)
    return act

def resnet_stage1(input, name=None, stride_flag=False):
    x = input
    conv1 = Conv(input, 64, kernel=(1, 1), name='%s_conv1_1*1'%name)
    conv2 = Conv(conv1, 64, kernel=(3, 3), pad=(1, 1), name='%s_conv2_3*3'%name)
    conv3 = Conv(conv2, 256, kernel=(1, 1), name='%s_conv3_1*1'%name)

    res = conv3 + x
    bn = mx.sym.BatchNorm(data=res, name='%s_batchnorm'%name, fix_gamma=True)
    relu = mx.sym.Activation(data=bn, act_type='relu', name='%s_relu'%name)
    return relu

def resnet_stage2(input, name=None, stride_flag=True):
    x = input
    if stride_flag:
        conv1 = Conv(input, 128, kernel=(1, 1), stride=(2, 2), name='%s_conv2_1*1'%name)
    else:
        conv1 = Conv(input, 128, kernel=(1, 1), name='%s_conv1_1*1'%name)
    conv2 = Conv(conv1, 128, kernel=(3, 3), pad=(1, 1), name='%s_conv2_3*3'%name)
    conv3 = Conv(conv2, 512, kernel=(1, 1), name='%s_conv3_1*1' %name)

    res = conv3 + x
    bn = mx.sym.BatchNorm(data=res, name='%s_batchnorm' % name, fix_gamma=True)
    relu = mx.sym.Activation(data=bn, act_type='relu', name='%s_relu'%name)
    return relu

def resnet_stage3(input, name=None, stride_flag=True):
    x = input
    if stride_flag:
        conv1 = Conv(input, 256, kernel=(1, 1), stride=(2, 2), name='%s_conv1_1*1'%name)
    else:
        conv1 = Conv(input, 256, kernel=(1, 1), name='%s_conv2_1*1'%name)
    conv2 = Conv(conv1, 256, kernel=(3, 3), pad=(1, 1), name='%s_conv_3*3'%name)
    conv3 = Conv(conv2, 1024, kernel=(1, 1), name='%s_conv_1*1'%name)

    res = conv3 + x
    bn = mx.sym.BatchNorm(data=res, name='%s_batchnorm' % name, fix_gamma=True)
    relu = mx.sym.Activation(data=bn, act_type='relu', name='%s_relu'%name)
    return relu

def resnet_stage4(input, name=None, stride_flag=True):
    x = input
    if stride_flag:
        conv1 = Conv(input, 512, kernel=(1, 1), stride=(2, 2), name='%s_conv1_1*1'%name)
    else:
        conv1 = Conv(input, 512, kernel=(1, 1), name='%s_conv1_1*1' %name)
    conv2 = Conv(conv1, 512, kernel=(3, 3), pad=(1, 1), name='%s_conv2_3*3'%name)
    conv3 = Conv(conv2, 2048, kernel=(1, 1), name='%s_conv3_1*1'%name)

    res = conv3 + x
    bn = mx.sym.BatchNorm(data=res, name='%s_batchnorm' % name, fix_gamma=True)
    relu = mx.sym.Activation(data=bn, act_type='relu', name='%s_relu'%name)
    return relu

def get_symbol(num_classes=1000):
    data = mx.symbol.Variable(name="data")

    conv = Conv(data, 64, kernel=(7, 7), stride=(2, 2), pad=(2, 2), name="conv_1")
    x = mx.sym.Pooling(conv, kernel=(3, 3), stride=(2, 2), pool_type="max", name="pool")

    #3*stage1
    for i in range(3):
        x = resnet_stage1(x, name='stage1_step%d' %(i+1), stride_flag=False)

    x = mx.sym.Convolution(data=x, num_filter=512, kernel=(1, 1), stride=(2, 2), pad=(0, 0), no_bias=True,
                       name='stage2_step0_conv')
    x = mx.sym.BatchNorm(data=x, name='stage2_step0_batchnorm', fix_gamma=True)
    x = mx.sym.Activation(data=x, act_type='relu', name='stage2_step0_relu')

    #8*stage2
    for i in range(1, 8):
        if i == 0:
            x = resnet_stage2(x, name='stage2_step1', stride_flag=True)
        else:
            x = resnet_stage2(x, name='stage2_step%d' %(i+1), stride_flag=False)

    x = mx.sym.Convolution(data=x, num_filter=1024, kernel=(1, 1), stride=(2, 2), pad=(0, 0), no_bias=True,
                           name='stage3_step0_conv')
    x = mx.sym.BatchNorm(data=x, name='stage3_step0_batchnorm', fix_gamma=True)
    x = mx.sym.Activation(data=x, act_type='relu', name='stage3_step0_relu')

    #36*stage3
    for i in range(36):
        if i == 0:
            x = resnet_stage3(x, name='stage3_step1', stride_flag=True)
        else:
            x = resnet_stage3(x, name='stage3_step%d' %(i+1), stride_flag=False)

    x = mx.sym.Convolution(data=x, num_filter=2048, kernel=(1, 1), stride=(2, 2), pad=(0, 0), no_bias=True,
                           name='stage4_step0_conv')
    x = mx.sym.BatchNorm(data=x, name='stage4_step0_batchnorm', fix_gamma=True)
    x = mx.sym.Activation(data=x, act_type='relu', name='stage4_step0_relu')

    #3*stage4
    for i in range(3):
        if i == 0:
            x = resnet_stage4(x, name='stage4_step1', stride_flag=True)
        else:
            x = resnet_stage4(x, name='stage4_step%d' %(i+1), stride_flag=False)

    pool = mx.sym.Pooling(data=x, kernel=(8, 8), stride=(1, 1), pool_type="avg", name="global_pool")
    flatten = mx.sym.Flatten(data=pool, name="flatten")
    fc1 = mx.symbol.FullyConnected(data=flatten, num_hidden=num_classes, name="fc1")
    softmax = mx.symbol.SoftmaxOutput(data=fc1, name="softmax")
    return softmax


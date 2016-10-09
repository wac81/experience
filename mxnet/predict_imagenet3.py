#coding=utf-8

import argparse
import os
import os.path
from collections import OrderedDict
import mxnet as mx
import time

from img_preprocess import call_im2rec

train_prefix_path = './img_preprocess/object_train'
test_prefix_path = './img_preprocess/test'
test_img_root_path = './img_preprocess/test/'

test_dir_path = "./img_preprocess/"

# prefix = './erotic_model_5class/imagenet_model_inception-v3'
prefix = './object_model/imagenet_model_inception-v3'
iteration = 135
model_load = mx.model.FeedForward.load(prefix, iteration)

def get_label(lst_path):
    label_dict = {}
    order_label_dict = OrderedDict()
    with open(lst_path + '.lst', 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            if len(line[2].split('/')) > 1:
                name = line[2].split('/')[0]
            else:
                name = "no label"
            if int(float(line[1])) not in label_dict.keys():
                label_dict[int(float(line[1]))] = name
            else:
                pass
    sorted_list = sorted(label_dict.items(), key=lambda x: x[0])
    for item in sorted_list:
        order_label_dict[item[0]] = item[1]
    f.close()
    return order_label_dict

def main(batch_size, data_shape):
    # parser = argparse.ArgumentParser(description='predict an image on imagenet')
    # parser.add_argument('--batch-size', type=int, default=1,
    #                     help='the batch size')
    # parser.add_argument('--data-shape', type=int, default=299,
    #                     help='set image\'s shape')
    # args = parser.parse_args()
    # data_shape = (3, args.data_shape, args.data_shape)
    img_data_shape = (3, data_shape, data_shape)

    #图片格式转换
    if not os.path.exists(test_prefix_path + '.rec'):
        call_im2rec.convert(test_prefix_path, test_img_root_path)

    test = mx.io.ImageRecordIter(
            path_imgrec = test_prefix_path + '.rec',
            rand_crop   = False,
            rand_mirror = False,
            data_shape  = img_data_shape,
            batch_size  = batch_size,
            )

    # predict
    pro, data, label = model_load.predict(test, return_data=True)

    #result process
    pro_list = pro.tolist()
    right_label = [int(x) for x in label.tolist()]
    label_dict = get_label(train_prefix_path)

    right_label_name = []
    for index in right_label:
        right_label_name.append(label_dict[index])

    predict_label = [each_pro.index(max(each_pro)) for each_pro in pro_list]
    predict_label_name = []

    for index in predict_label:
        predict_label_name.append(label_dict[index])

    return pro_list, right_label, right_label_name, predict_label, predict_label_name, label_dict


def write2html(lst_path, fout, pro_list, right_label_name, predict_label_name, img_index_list, label_dict):
    img_dict = {}
    label_name = label_dict.values()
    index = 0
    with open(lst_path + '.lst', 'r') as f:
        for line in f:
            if index in img_index_list:
                line = line.strip().split('\t')
                img_loc = test_img_root_path + line[2]
                # print img_loc
                pro_dict = {}
                for i in xrange(len(pro_list[index])):
                    pro_dict[label_name[i]] = pro_list[index][i]
                if predict_label_name[index] == 'other':
                    img_dict[index] = [{'is_car': 'No'}, {'true': right_label_name[index]}, {'pro': pro_dict}, {'img_loc': img_loc}]
                else:
                    img_dict[index] = [{'is_car': 'Yes'}, {'true': right_label_name[index]}, {'pro': pro_dict}, {'img_loc': img_loc}]
            index += 1
    html = '<html>'
    html += '<head>'
    html += '<meta http-equiv="Content-Type" content="text/html"; charset=utf-8 />'
    html += '</head>'
    html += '<body>'
    for index in img_dict.keys():
        pro_tuple = sorted(img_dict[index][2]['pro'].items(), key=lambda x: x[1], reverse=True)
        html += '<h6 align="center">%s true =  %s \t %s</h6>' % (img_dict[index][0]['is_car'], img_dict[index][1]['true'], pro_tuple)
        html += '<div align="center"><img src=%s width="400" height="300" /></div>' % img_dict[index][3]['img_loc']
    html += '</body>'
    html += '</html>'
    fout.write(html)
    f.close()
    fout.close()

if __name__ == '__main__':
    t1 = time.time()
    pro_list, right_label, right_label_name, predict_label, predict_label_name, label_dict = main(batch_size=1, data_shape=299)
    count = 0
    print predict_label
    for index in xrange(len(right_label_name)):
        if right_label_name[index] != predict_label_name[index]:
            count += 1
            print "第 %d 张图片预测概率及预测标签： " % (index + 1), predict_label_name[index], pro_list[index]
            print "真实标签为： ", right_label_name[index]
        else:
            pass

    print "the number of predict: ", len(predict_label)
    print "the number of predict wrong: ", count

    t2 = time.time()
    print "waste time: ", (t2 - t1)

# -*- coding: utf-8 -*-
import genius
import jieba
text = u"昨天,我和施瓦布先生一起与部分企业家进行了交流,大家对中国经济当前、未来发展的态势、走势都十分关心。"
text = u"这个人很实在"
text = u"乘某路公交车访友新居，称“在蒋王庙前一站下车”，本人在未到达蒋王庙的前一站(蒋王庙-1)下车，结果错了，该人说的是过蒋王庙后的一站(蒋王庙+1)下车。"

seg_list = genius.seg_text(
    text,
    use_combine=True,
    use_pinyin_segment=True,
    use_tagging=True,
    use_break=True
)
print('\n'.join(['%s\t%s' % (word.text, word.tagging) for word in seg_list]))


seg_list = genius.seg_keywords(u'你看过穆赫兰道吗')
print('\n'.join([word.text for word in seg_list]))

seg_list = jieba.cut(u'你看过穆赫兰道吗')  # 默认是精确模式
print(", ".join(seg_list))


seg_list = genius.extract_tag(u'南京市长江大桥')
print('\n'.join(seg_list))
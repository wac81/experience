from image_match.goldberg import ImageSignature
gis = ImageSignature()
a = gis.generate_signature('http://d.hiphotos.baidu.com/image/pic/item/3bf33a87e950352ae53923315a43fbf2b2118baa.jpg')
b = gis.generate_signature('http://g.hiphotos.baidu.com/image/pic/item/83025aafa40f4bfb4dc7986d0a4f78f0f73618f7.jpg')
c = gis.generate_signature('http://g.hiphotos.baidu.com/image/pic/item/83025aafa40f4bfb4dc7986d0a4f78f0f73618f7.jpg')
d = gis.generate_signature('http://g.hiphotos.baidu.com/image/pic/item/83025aafa40f4bfb4dc7986d0a4f78f0f73618f7.jpg')
similar = gis.normalized_distance(a, b)

print a, b, similar

#首先，进行姿势检测和校准：
./util/align-dlib.py ./training-images/ align outerEyesAndNose ./aligned-images/ --size 96
#这将创建一个新./aligned-images/子文件夹，带有每一个测试图像的裁剪过的并且对齐的版本。


#第二，从对齐的图像中生成表征：
./batch-represent/main.lua -outDir ./generated-embeddings/ -data ./aligned-images/
#运行完后，这个./aligned-images/子文件夹会包含一个带有每张图像的嵌入的  csv 文件。


#第三，训练自己的面部检测模型：
./demos/classifier.py train ./generated-embeddings/
#这将产生名为./generated-embeddings/classifier.pkl的新文件名。这个文件有你将用来识别新面部的 SVM 模型。


#predict images
./demos/classifier.py infer ./generated-embeddings/classifier.pkl your_test_image.jpg
### 人脸检测API
参考的是[这里](https://github.com/yeephycho/tensorflow-face-detection)，是一个基于tensorflow ssd mobilenet finetune的人脸检测模型。这里直接
借用了对方的模型文件，并根据它的python inference代码整理成了c++代码，即这个```face_detect.cpp```，并对检测到的人脸进行了扩展，将来可以集成到其它
项目里了
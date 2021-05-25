# cnn_codeIdentified
use cnn recognize captcha by tensorflow. 本项目针对字符型图片验证码，使用tensorflow实现卷积神经网络，进行验证码识别。

项目封装了验证码的生成、校验、训练、验证模块，识别模块还在努力编写中。

# 时间表
## 2021.05.25
初版README.md，加入关于验证码识别的一些说明

# 1 项目介绍

## 1.1 关于验证码识别

验证码识别大多数爬虫会遇到的问题，也可以作为图像识别的入门案例。

传统的图像处理和机器学习算法，涉及多种技术：

1.图像处理

* 前处理（灰度化、二值化）
* 图像分割
* 裁剪（去边框）
* 图像滤波、降噪
* 去背景
* 颜色分离
* 旋转

2.机器学习

* KNN（最近邻分类算法）
* SVN（向量机）

使用该类方法对我来说要求较高，处理方法不够通用，需要花费很多时间去调整整理步骤和相关算法。

而使用卷积神经网络，只需要通过简单的前处理，就可以实现大部分静态字符型验证码的端到端识别，效果很好，通用性很高。

## 1.2目录结构

### 1.2.1 基本配置

| 序号 | 文件名称 | 说明         |
| :--- | :------- | :----------- |
| 1    | sample/  | 数据集目录   |
| 2    | model/   | 模型文件目录 |

### 1.2.2 训练模型

| 序号 | 文件名称                 | 说明                                 |
| ---- | ------------------------ | ------------------------------------ |
| 1    | example.py               | 生成验证码脚本                       |
| 2    | verify_and_split_data.py | 验证数据集、拆分数据为训练集和测试集 |
| 3    | train_model.py           | 训练模型                             |
| 4    | test_batch.py            | 批量验证                             |

## 1.3 依赖

```
pip install captcha
```

```
pip install numpy
```

```
pip install tensorflow==1.12.0
```

注意：我选择的是CPU版本，如果tensorflow网络下载超时，可以通过离线下载包下载。如果有人问我为啥不装GPU版本的，我只能说贫穷限制了我的创造力。

## 1.4 模型结构

| 序号 | 层级                              |
| ---- | --------------------------------- |
| 输入 | input                             |
| 1    | 卷积层 + 池化层 + 降采样层 + ReLU |
| 2    | 卷积层 + 池化层 + 降采样层 + ReLU |
| 3    | 卷积层 + 池化层 + 降采样层 + ReLU |
| 4    | 全连接 + 降采样层 + Relu          |
| 5    | 全连接 + softmax                  |
| 输出 | output                            |

# 2 如何使用

## 2.1 数据集

原始数据集存在在`./sample/origin`目录中。

如果你没有原始数据集，你可以使用`example.py`文件生成原始数据集，生成之前你可以通过修改相关配置（路径、文件后缀、字符集等）。

```
{
  "root_dir": "sample/origin/",  # 验证码保存路径
  "image_suffix": "jpg",         # 验证码图片后缀
  "characters": "0123456789abcdefghijklmnopqrstuvwxyz",    # 生成验证码的可选字符
  "count": 10000,                # 生成验证码的图片数量
  "char_count": 4,               # 每张验证码图片上的字符数量
  "width": 100,                  # 图片宽度
  "height": 60                   # 图片高度
}
```

## 2.2 配置文件

创建新项目前，需要自行修改相关配置文件。

```
{
  "sample_conf.origin_image_dir": "sample/origin/",  # 原始文件
  "sample_conf.train_image_dir": "sample/train/",    # 训练集
  "sample_conf.test_image_dir": "sample/test/",      # 测试集
  "image_width": 100,                    # 图片宽度
  "image_height": 60,                    # 图片高度
  "max_captcha": 4,                      # 验证码字符个数
  "image_suffix": "jpg",                 # 图片文件后缀
  "char_set": "0123456789abcdefghijklmnopqrstuvwxyz",  # 验证码识别结果类别
  "cycle_stop": 3000,                                  # 启动任务后的训练指定次数后停止
  "acc_stop": 0.99,                                    # 训练到指定准确率后停止
  "cycle_save": 500,                                   # 训练指定次数后定时保存模型
  "train_batch_size": 128,                             # 训练时每次使用的图片张数
  "test_batch_size": 100                               # 每批次测试时验证的图片张数，不要超过验证码集的总数
}
```

## 2.3 验证和拆分数据集

此功能会校验原始图片集的尺寸和测试图片是否能打开，并按照19:1的比例拆分出训练集和测试集（有想法的可以通过修改参数更改比例）。

所以需要分别创建和指定三个文件夹：origin， train， test用于存放相关文件。

文件夹创建完毕后执行`verify_and_split_data.py`文件，vscode会有相关提示，如有无效文件，该文件会留在原文件夹（即origin）。

## 2.4 训练模型

创建好训练集和测试集后，就可以开始训练模型了。

训练过程中vs会输出日志，展示当前的训练轮数、准确率和loss。

**此时的准确率是训练集图片的准确率，代表训练集的图片识别情况。**

例如：

```
第60次训练 >>>
[训练集] 字符准确率为 0.16750 图片准确率为 0.00000 >>> loss 0.1215432733
[验证集] 字符准确率为 0.14500 图片准确率为 0.00000 >>> loss 0.1215432733
```

字符准确率和图片准确率的解释：

```
`假如，有100张验证码图片，每张图片有四个字符，即400个字符。也就是说我把任务拆分为需要识别400个字符准确率：识别400个字符中，正确字符的占比。`

`图片准确率：100张验证码图片中，4个字符完全识别准确的图片占比。`
```

执行`train_model.py`文件，就可以漫长的跑训练模型了。**电脑发出嗡嗡的响声请不要惊慌！**

## 2.5 测试识别

在训练模型保存后，可以执行`test_batch.py`文件测试。

**此时的准确率是测试集图片的准确率，代表测试集的图片识别情况。**

例如：

```
测试结果： 40/100
100个样本识别耗时6.118269205093384秒，准确率40.0%
```

**这是我跑的最高的一次，一般都是18%左右的。**

# 3 训练数据统计

由于时间问题，我只能简单测试一下。

训练条件：

* 验证码：本项目自带生成验证码程序，数字+小写英文
* 数量：10000张
* 计算机引擎：CPU

经过训练：

3000次，训练集字符准确率最高可达0.93250，图片准确率最高可达0.79。

5000次，训练集字符准确率最高可达0.97250，图片准确率最高可达0.91。

再往后我不敢跑了，笔记本已经需要两台风扇给他散热了。

# 4 开发说明

2021.05.26

仅仅是为了满足课设，但做完后我觉得还有待优化的地方。




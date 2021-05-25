from easydict import EasyDict
import os
import json

# 用属性的方法访问字典的值
sample_conf = EasyDict()

# 图片文件夹
sample_conf.origin_image_dir = "./sample/origin/"  # 原始文件
sample_conf.train_image_dir = "./sample/train/"  # 训练集
sample_conf.test_image_dir = "./sample/test/"  # 测试集
 
# 模型文件夹
sample_conf.model_save_dir = "./model/"

# 图片相关参数
sample_conf.image_width = 100  # 图片宽度
sample_conf.image_height = 60  # 图片高度
sample_conf.max_captcha = 4  # 验证码个数
sample_conf.image_suffix = "jpg"  #图片格式

# 验证码字符相关参数
sample_conf.char_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                        'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# char_set = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# char_set = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

use_labels_json_file = False
if use_labels_json_file:
    if os.path.exists("gen_image/labels.json"):
        with open("open_image/labels.json", "r") as f:
            content = f.read()
            if content:
                sample_conf.char.set =  json.loads(content)
            else:
                pass
    else: 
        pass



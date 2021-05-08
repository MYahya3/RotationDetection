# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import os
import tensorflow as tf
import math

from dataloader.pretrained_weights.pretrain_zoo import PretrainModelZoo

"""
RetinaNet-H + gwd fix bug + sqrt + tau=2 + data aug. + ms + res152 + 4x
FLOPs: 1689351216;    Trainable params: 67540388
This is your result for task 1:

mAP: 0.7421600828825043
ap of each class:
plane:0.8746987894637671,
baseball-diamond:0.8376646466752732,
bridge:0.5229692567141183,
ground-track-field:0.6823765143956025,
small-vehicle:0.7323565067454257,
large-vehicle:0.6513604479863764,
ship:0.8017917795319636,
tennis-court:0.8962594011987421,
basketball-court:0.8438647203873725,
storage-tank:0.8552598810829213,
soccer-ball-field:0.6578830653179499,
roundabout:0.660232773979747,
harbor:0.695676879209987,
swimming-pool:0.7221396310194939,
helicopter:0.6978669495288252

The submitted information is :

Description: RetinaNet_DOTA_4x_20201217_183.6w_ms
Username: SJTU-Det
Institute: SJTU
Emailadress: yangxue-2019-sjtu@sjtu.edu.cn
TeamMembers: yangxue

single-scale
This is your result for task 1:

mAP: 0.7331694436058974
ap of each class:
plane:0.8905781496189736,
baseball-diamond:0.834845510763441,
bridge:0.4984057147263833,
ground-track-field:0.6533844664498967,
small-vehicle:0.7463740884330602,
large-vehicle:0.6762629627269935,
ship:0.8239344210683832,
tennis-court:0.8839392263017938,
basketball-court:0.8418591690553617,
storage-tank:0.8480155771670074,
soccer-ball-field:0.6374051983231258,
roundabout:0.6132224612301435,
harbor:0.6647031161827364,
swimming-pool:0.7093747500865332,
helicopter:0.6752368419546273

The submitted information is :

Description: RetinaNet_DOTA_4x_20201217_183.6w_s
Username: SJTU-Det
Institute: SJTU
Emailadress: yangxue-2019-sjtu@sjtu.edu.cn
TeamMembers: yangxue
"""

# ------------------------------------------------
VERSION = 'RetinaNet_DOTA_4x_20201217'
NET_NAME = 'resnet152_v1d'  # 'MobilenetV2'

# ---------------------------------------- System
ROOT_PATH = os.path.abspath('../../')
print(20*"++--")
print(ROOT_PATH)
GPU_GROUP = "0,1,2"
NUM_GPU = len(GPU_GROUP.strip().split(','))
SHOW_TRAIN_INFO_INTE = 20
SMRY_ITER = 200
SAVE_WEIGHTS_INTE = 27000 * 4

SUMMARY_PATH = os.path.join(ROOT_PATH, 'output/summary')
TEST_SAVE_PATH = os.path.join(ROOT_PATH, 'tools/test_result')

pretrain_zoo = PretrainModelZoo()
PRETRAINED_CKPT = pretrain_zoo.pretrain_weight_path(NET_NAME, ROOT_PATH)
TRAINED_CKPT = os.path.join(ROOT_PATH, 'output/trained_weights')
EVALUATE_R_DIR = os.path.join(ROOT_PATH, 'output/evaluate_result_pickle/')

# ------------------------------------------ Train and Test
RESTORE_FROM_RPN = False
FIXED_BLOCKS = 1  # allow 0~3
FREEZE_BLOCKS = [True, False, False, False, False]  # for gluoncv backbone
USE_07_METRIC = True
ADD_BOX_IN_TENSORBOARD = True

MUTILPY_BIAS_GRADIENT = 2.0  # if None, will not multipy
GRADIENT_CLIPPING_BY_NORM = 10.0  # if None, will not clip

CLS_WEIGHT = 1.0
REG_WEIGHT = 2.0
REG_LOSS_MODE = 2
ALPHA = 1.0
BETA = 1.0

BATCH_SIZE = 1
EPSILON = 1e-5
MOMENTUM = 0.9
LR = 1e-3
DECAY_STEP = [SAVE_WEIGHTS_INTE*12, SAVE_WEIGHTS_INTE*16, SAVE_WEIGHTS_INTE*20]
MAX_ITERATION = SAVE_WEIGHTS_INTE*20
WARM_SETP = int(1.0 / 8.0 * SAVE_WEIGHTS_INTE)

# -------------------------------------------- Dataset
DATASET_NAME = 'DOTA'  # 'pascal', 'coco'
PIXEL_MEAN = [123.68, 116.779, 103.939]  # R, G, B. In tf, channel is RGB. In openCV, channel is BGR
PIXEL_MEAN_ = [0.485, 0.456, 0.406]
PIXEL_STD = [0.229, 0.224, 0.225]  # R, G, B. In tf, channel is RGB. In openCV, channel is BGR
IMG_SHORT_SIDE_LEN = [800, 500, 640, 700, 900, 1000, 1100, 1200]
IMG_MAX_LENGTH = 1200
CLASS_NUM = 15

IMG_ROTATE = True
RGB2GRAY = True
VERTICAL_FLIP = True
HORIZONTAL_FLIP = True
IMAGE_PYRAMID = True

# --------------------------------------------- Network
SUBNETS_WEIGHTS_INITIALIZER = tf.random_normal_initializer(mean=0.0, stddev=0.01, seed=None)
SUBNETS_BIAS_INITIALIZER = tf.constant_initializer(value=0.0)
PROBABILITY = 0.01
FINAL_CONV_BIAS_INITIALIZER = tf.constant_initializer(value=-math.log((1.0 - PROBABILITY) / PROBABILITY))
WEIGHT_DECAY = 1e-4
USE_GN = False
FPN_CHANNEL = 256
NUM_SUBNET_CONV = 4
FPN_MODE = 'fpn'

# --------------------------------------------- Anchor
LEVEL = ['P3', 'P4', 'P5', 'P6', 'P7']
BASE_ANCHOR_SIZE_LIST = [32, 64, 128, 256, 512]
ANCHOR_STRIDE = [8, 16, 32, 64, 128]
ANCHOR_SCALES = [2 ** 0, 2 ** (1.0 / 3.0), 2 ** (2.0 / 3.0)]
ANCHOR_RATIOS = [1, 1 / 2, 2., 1 / 3., 3., 5., 1 / 5.]
ANCHOR_ANGLES = [-90, -75, -60, -45, -30, -15]
ANCHOR_SCALE_FACTORS = None
USE_CENTER_OFFSET = True
METHOD = 'H'
USE_ANGLE_COND = False
ANGLE_RANGE = 90  # or 180

# -------------------------------------------- Head
SHARE_NET = True
USE_P5 = True
IOU_POSITIVE_THRESHOLD = 0.5
IOU_NEGATIVE_THRESHOLD = 0.4

NMS = True
NMS_IOU_THRESHOLD = 0.1
MAXIMUM_DETECTIONS = 100
FILTERED_SCORE = 0.05
VIS_SCORE = 0.4

# -------------------------------------------- GWD
GWD_TAU = 2.0
GWD_FUNC = tf.sqrt

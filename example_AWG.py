import sys
import time
from crs import *
from ctypes import *
import threading


device = CRSDevice()

# 1.初始化，并连接设备
device.init_device()
succ = device.connect_device()
if succ:
    print("connect succeeded!")
else:
    print("connect failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 2.设置设备参数
param = Params()
param.broadcastMode = 0  # CRS播放模式, 0 连续, 1 Trigger
param.isDDSModeOpen = 0  # 0 关闭DDS, 1 开启DDS
param.isDAQModeOpen = 0  # 0 关闭DAQ, 1 开启DAQ
param.isAWGModeOpen = 1  # 0 关闭AWG, 1 开启AWG
param.ASGChannelState = (c_ushort * 8)(0,0,0,0,0,0,0,0) # 关闭 ASG 8个通道
succ = device.set_CRS_params(param)
if not succ:
    print("params set failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 3.AWG空闲状态偏置, 0~65535
bias1 = 32768
bias2 = 32768
succ = device.set_AWG_biases(bias1, bias2)

# 4.下载AWG代码
code = """
# 示例：波形相乘
GAmp = 400;

f = 140;
length = 140;  # 不要超过 4x10^6
w1 = Sin(f, L=length);
w2 = Sin(2*f, L=length);
w3 = SinC(f, L=length);
w4 = SinC(2*f, L=length)
w5 = Gauss(length/6, L=length);

w12 = w1 * w2
w34 = 0.3 * w3 + w4 * 0.7
w345 = (w3 + w4) * w5

s1 = SEQ([w12(1, T), w34(1, C), w345(1, T)])
s2 = SEQ([w12(1, T), w34(1, C)])

OUT1 = s1;
OUT2 = s1;
"""
succ = device.load_code_to_device(code)
if not succ:
    print("AWG data download failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 5.开始播放
device.start()    # 无限循环
#device.start(10) # 循环10次

# 6.结束
input("press Enter to stop")
device.stop()
device.close_device()

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
param.isDDSModeOpen = 1  # 0 关闭DDS, 1 开启DDS
param.isDAQModeOpen = 0  # 0 关闭DAQ, 1 开启DAQ
param.isAWGModeOpen = 0  # 0 关闭AWG, 1 开启AWG
param.ASGChannelState = (c_ushort * 8)(0,0,0,0,0,0,0,0)
succ = device.set_CRS_params(param)
if not succ:
    print("params set failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 3.设置DDS参数
freq1 = 150.  # 通道1频率, 0~1000 MHz 
freq2 = 150.  # 通道2频率, 0~1000 MHz
phase1 = 1.0  # 通道1相位, 0~2 pi
phase2 = 0.5  # 通道2相位, 0~2 pi
amp1 = 65535  # 通道1幅度, 0~65535
amp2 = 65535  # 通道2幅度, 0~65535
bias1 = 0     # 通道1偏置, -32768~32767, 且 amp1 + bias1 < 65535
bias2 = 0     # 通道2偏置, -32768~32767, 且 amp2 + bias2 < 65535
succ = device.set_DDS_AWG_mode(freq1, freq2, phase1, phase2, amp1, amp2, bias1, bias2)
if not succ:
    print("DDS params set failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 5.开始播放
device.start() # 无限循环
#device.start(10) # 循环10次
print("DDS playing...")

# 6.结束
input("press Enter to stop")
device.stop()
device.close_device()

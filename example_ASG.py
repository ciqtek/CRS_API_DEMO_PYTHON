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
param.isAWGModeOpen = 0  # 0 关闭AWG, 1 开启AWG
param.ASGChannelState = (c_ushort * 8)(1,1,1,1,1,1,1,1) # 启用ASG 8个通道
succ = device.set_CRS_params(param)
if not succ:
    print("params set failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 3.ASG默认电平, 最高位是1通道, 最低为是8通道
dft_lvl = 0b1111_1111
succ = device.set_ASG_default(dft_lvl)

# 4.下载ASG数据
asg_data = [
    (1, [( 20, [0,0,0,0,0,0,0,0]), 
         ( 20, [1,1,1,1,1,1,1,1]), 
         ( 20, [0,0,0,0,0,0,0,0]),]),
    (4, [(100, [0,1,0,1,0,1,0,1]), 
         (100, [1,0,1,0,1,0,1,0]), 
         (200, [1,1,1,1,0,0,0,0]), 
         (200, [0,0,0,0,1,1,1,1]),
         ( 20, [0,0,0,0,0,0,0,0]),]),
    (2, [( 40, [1,1,1,1,1,1,1,1]), 
         ( 40, [0,0,0,0,0,0,0,0]),]),
]
succ = device.download_ASG_pulse_data(asg_data)
if not succ:
    print("download ASG pulse failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 5.开始播放
device.start()    # 无限循环
#device.start(10) # 循环10次

# 6.结束, 停止播放，关闭设备
input("press Enter to stop")
device.stop()
device.close_device()

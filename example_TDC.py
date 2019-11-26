import sys
import time
from crs import *
from ctypes import *
import threading

all_data = []

@CFUNCTYPE(None, c_int, c_int, c_int)
def call_back(grp, countC, countF):
    global all_data
    all_data.append((grp, countC, countF))

@CFUNCTYPE(None, c_int)
def status_callback(status):
    if status == 1:
        print("缓存区溢出，已停止")

class DealData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.working = True
    
    def run(self):
        global all_data
        show_pos_beg = 0
        show_pos_end = 0
        while self.working:
            if len(all_data) != 0:
                show_pos_end = len(all_data)
                for it in all_data[show_pos_beg:show_pos_end]:
                    print(it)
                show_pos_beg = len(all_data)
    
    def stop(self):
        self.working = False


def read_file(filename):
    dlst = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for l in lines:
            d = l.split(',')
            d = int(d[-1])
            dlst.append(d)
    return dlst


device = CRSDevice()

# 1.初始化连接设备
device.init_device()
res = device.connect_device()
if res:
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
param.ASGChannelState = (c_ushort * 8)(0,0,0,0,0,0,0,0)
succ = device.set_CRS_params(param)
if not succ:
    print("parammeters set failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 3.下载TDC校准文件
d1 = read_file("F:/Device-Demos/CRS_SDK/CRS-standard/tdc_calibration/tdc_calib_ch1.csv")
d2 = read_file("F:/Device-Demos/CRS_SDK/CRS-standard/tdc_calibration/tdc_calib_ch2.csv")
d3 = read_file("F:/Device-Demos/CRS_SDK/CRS-standard/tdc_calibration/tdc_calib_ch3.csv")
d4 = read_file("F:/Device-Demos/CRS_SDK/CRS-standard/tdc_calibration/tdc_calib_ch4.csv")
cali_data = [d1, d2, d3, d4]
succ = device.download_TDC_calibration(cali_data)
if not succ:
    print("calibration data set failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 4.设置TDC参数
succ = device.set_TDC_params(400, 400, True, True, 1, 1)
if not succ:
    print("tdc parameters set failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 5.设置回调函数
device.set_status_callback(status_callback)
device.set_TDC_callback(call_back)

# 6.启动数据处理线程
deal_thrd = DealData()
deal_thrd.start()

# 7.开始播放
device.start()

# 主线程休眠 10 秒，停止播放
time.sleep(10)
device.stop()

# 停止监视线程，程序退出
deal_thrd.stop()
deal_thrd.join()

# 8.断开连接
device.close_device()

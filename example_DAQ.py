import sys
import time
from crs import *
from ctypes import *
import threading


dtr = 0
all_data = []

@CFUNCTYPE(None, c_int)
def status_callback(status):
    if status == 1:
        print("USB buffer overflow, you may lost data. Device has stopped.")

@CFUNCTYPE(None, c_int, c_char_p)
def call_back(coll_type, data):
    global dtr, all_data
    dtr += 1
    strd = str(data)[2:-2]
    d1, d2 = strd.split(" ")
    try:
        d1 = int(d1)
        d2 = int(d2)
    except:
        print(strd)
    all_data.append((d1, d2))

class DataCallback(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.working = True
    
    def run(self):
        global dtr
        show_pos_beg = 0
        show_pos_end = 0
        while self.working:
            if dtr != 0:
                show_pos_end = len(all_data)
                for it in all_data[show_pos_beg:show_pos_end]:
                    print(it)
                show_pos_beg = len(all_data)
    
    def stop(self):
        self.working = False


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
param.isDAQModeOpen = 1  # 0 关闭DAQ, 1 开启DAQ
param.isAWGModeOpen = 0  # 0 关闭AWG, 1 开启AWG
param.ASGChannelState = (c_ushort * 8)(0,0,0,0,0,0,0,0) #(1,1,1,1,1,1,1,1)
succ = device.set_CRS_params(param)
if not succ:
    print("params set failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 3.设置DAQ数据
adc_data = [
   (4, [(  100, 1),
        (  100, 0), 
        (  200, 1), 
        (20000, 0),]),
   (2, [(   40, 1), 
        (50000, 0),]),
]
succ = device.download_ADC_data(adc_data)
if not succ:
    print("DAQ data download failed!")
    err_info = device.get_error_code()
    print(err_info[0], err_info[1])
    sys.exit()

# 4.设置回调函数，状态回调和数据回调
device.set_status_callback(status_callback)
device.set_DAQ_callback(call_back)

# 5.启动数据处理线程
dcb_thrd = DataCallback()
dcb_thrd.start()

# 5.开始播放
input("press Enter to start")
device.start()

# 6.数据处理停止条件, 作为示例我们选择让主线程休眠 10 秒，然后停止播放
time.sleep(10)
device.stop()

# 7.停止数据处理线程, 程序退出
dcb_thrd.stop()
dcb_thrd.join()

# 8.停止, 断开连接
device.close_device()

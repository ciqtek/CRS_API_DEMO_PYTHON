import os
from ctypes import *
import platform

ErrorMode = {
    -1: 'UnknownError',
    0: 'NONE',
    1: 'AutoConfigError',
    2: 'DeviceError',
    101: 'OpenFailed',
    102: 'SuccessProgram',
    103: 'LackParameter',    #缺少必要参数
    104: 'WavemodeError',    #波形类型异常
    105: 'LACK_ALL_PARAM',    #未找到任何可用参数
    106: 'UnknownOutput',   #未知的output输出要求
    107: 'OutputDataLengthError', #输出的通道1和通道2不相等
    108: 'EnableSignalError',
    109: 'SpaceNotEnough',
    110: 'AWG_ParamsError',
    1001: 'ScriptStartError',
    1002: 'ScriptOpenError',
    1003: 'ScriptOutLengthError',
    2001: 'ASG_NoneSegment',
    2002: 'ASG_LastLess20',
    2003: 'ASG_HighRangeError',
    2004: 'ASG_LowRangeError',
    2005: 'ASG_IllegalData',
    3001: 'DAQ_NoneSegment',
    3002: 'DAQ_HighRageError',
    3003: 'DAQ_LowRangeError',
    4001: 'TDC_OpenFailed',
    4002: 'TDC_LackData'
}


class Params(Structure):
    _fields_ = [
        ('broadcastMode', c_ushort),
        ('isDDSModeOpen', c_int),
        ('isDAQModeOpen', c_int),
        ('isAWGModeOpen', c_int),
        ('ASGChannelState', (c_ushort *8))
    ]


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]

STATUS_CALLBACK  = CFUNCTYPE(None, c_int)
DAQ_CALLBACKTYPE = CFUNCTYPE(None, c_int, c_char_p)
TDC_CALLBACKTYPE = CFUNCTYPE(None, c_int, c_int, c_int)

@Singleton
class CRSDevice():
    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        wd = os.path.abspath(os.path.dirname(__file__))
        arch = platform.architecture()[0]
        
        dll_path = ""
        
        if arch == '64bit':
            dll_path = os.path.join(wd, 'CRS_SDK_x64.dll')
        else:
            dll_path = os.path.join(wd, 'CRS_SDK.dll')

        # if arch == '64bit':
        #     dll_path = os.path.join(wd, 'CRS_SDK_x64_d.dll')
        # else:
        #     dll_path = os.path.join(wd, 'CRS_SDK_d.dll')

        if os.path.isfile(dll_path):
            self.__dll = CDLL(dll_path)
        else:
            raise Exception("can not found dll")

        self.__dll.CRS_GetErrorCode.restype = c_int
        self.__dll.CRS_GetDeviceInfo.restype = c_char_p
        self.__dll.CRS_MonitorDeviceStatus.restype = c_bool
        self.__dll.CRS_SetStatusCallback.argtypes = [STATUS_CALLBACK]
        self.__dll.CRS_SetStatusCallback.restype = c_bool
        self.__dll.CRS_SetDAQCallbackFunc.argtypes = [DAQ_CALLBACKTYPE]
        self.__dll.CRS_SetDAQCallbackFunc.restype = c_bool
        self.__dll.CRS_InitDevice.restype = c_bool
        self.__dll.CRS_ConnectDievce.restype = c_bool
        self.__dll.CRS_CloseDevice.restype = c_bool
        self.__dll.CRS_LoadCodeToDevice.restype = c_bool
        self.__dll.CRS_StartBroadcast.restype = c_bool
        self.__dll.CRS_StopBroadcast.restype = c_bool
        # self.__dll.CRS_SetDDSCommand.restype = c_bool
        # self.__dll.CRS_SetFIRCommand.restype = c_bool
        self.__dll.CRS_SetDAQParams.restype = c_bool
        self.__dll.CRS_SetASGDefauleLevel.restype = c_bool
        #self.__dll.CRS_ASGPulseDownload.argtypes = [POINTER(POINTER(c_double)), POINTER(POINTER(c_int)), POINTER(c_ushort), c_ushort]
        self.__dll.CRS_ASGPulseDownload.restype = c_bool
        #self.__dll.CRS_ADCENSignalDownload.argtypes = [POINTER(c_longlong), POINTER(c_int), POINTER(c_ushort), c_ushort]
        self.__dll.CRS_ADCENSignalDownload.restype = c_bool
        self.__dll.CRS_SetDDSAWGMode.restype = c_bool
        self.__dll.CRS_StartDDSBroadcast.restype = c_bool
        #self.__dll.CRS_SetCRSParams.argtypes = [] #!!!
        self.__dll.CRS_SetCRSParams.restype = c_bool
        self.__dll.CRS_SetAWGBiases.restype = c_bool
        self.__dll.CRS_SetTDCCallbackFunc.argtypes = [TDC_CALLBACKTYPE]
        self.__dll.CRS_SetTDCCallbackFunc.restype = c_bool
        # self.__dll.CRS_TDCDownloadCalibration.argtypes = [4][200]
        self.__dll.CRS_SetTDCParams.restype = c_bool


    def get_error_code(self):
        errcode = self.__dll.CRS_GetErrorCode()
        return (errcode, ErrorMode[errcode])
    
    def get_device_info(self):
        return str(self.__dll.CRS_GetDeviceInfo())
    
    def get_monitor_status(self):
        return self.__dll.CRS_MonitorDeviceStatus()

    def set_status_callback(self, func):
        if type(func) == STATUS_CALLBACK:
            return self.__dll.CRS_SetStatusCallback(func)
        else:
            return False

    #CRS_SDK_API BOOL CRS_SetCallBackFun(DATA_CALLBACK func);
    def set_DAQ_callback(self, func):
        if type(func) == DAQ_CALLBACKTYPE:
            return self.__dll.CRS_SetDAQCallbackFunc(func)
        else:
            return False

    def init_device(self):
        return self.__dll.CRS_InitDevice()

    def connect_device(self):
        return self.__dll.CRS_ConnectDievce()

    def close_device(self):
        return self.__dll.CRS_CloseDevice()
    
    def load_code_to_device(self, code):
        code = c_char_p(code.encode('utf-8'))
        return self.__dll.CRS_LoadCodeToDevice(code)

    def start(self, num=0):
        n = c_uint(num)
        return self.__dll.CRS_StartBroadcast(n)

    def stop(self):
        return self.__dll.CRS_StopBroadcast()

    # def set_DDS_command(self, freq, pha):
    #     freq = c_double(freq)
    #     pha = c_double(pha)
    #     return self.__dll.CRS_SetDDSCommand(freq, pha)

    # def set_FIR_comand(self, type):
    #     type = c_ushort(type)
    #     return self.__dll.CRS_SetFIRCommand(type)

    def set_DAQ_params(self, offset1, offset2):
        offset1 = c_short(offset1)
        offset2 = c_short(offset2)
        return self.__dll.CRS_SetDAQParams(offset1, offset2)

    def set_ASG_default(self, default_level):
        deflvl = c_ubyte(default_level)
        return self.__dll.CRS_SetASGDefauleLevel(deflvl)

    def download_ASG_pulse_data(self, data):
        seg_num = len(data)
        loop = []

        pulses = []
        for i in range(8):
            pulses.append([])

        length = []
        for i in range(seg_num):
            length.append([0]*8)
        
        seg_idx = -1
        for l, seg_data in data:
            seg_idx += 1
            # print('Segment {}, loop {}'.format(seg_idx, l))
            # print(d)
            loop.append(l)

            level_arr = []
            time_arr = []
            for tm, lvl in seg_data:
                time_arr.append(tm)
                level_arr.append(lvl)
            
            # print("time arr:", time_arr)
            # print("level arr:", level_arr)
            for ch in range(8):
                pre_lvl = 1
                st = 0
                for i in range(len(time_arr)):
                    if level_arr[i][ch] != pre_lvl:
                        length[seg_idx][ch] += 1
                        pulses[ch].append(st)
                        pre_lvl = level_arr[i][ch]
                        st = 0
                    st += time_arr[i]
                length[seg_idx][ch] += 1
                pulses[ch].append(st)

                if length[seg_idx][ch] % 2 == 1:
                    length[seg_idx][ch] += 1
                    pulses[ch].append(0)
                
        # print(pulses)
        # print(length)
        # print(loop)
        # print(seg_num)
        
        # 数据正确，类型转换 
        c_pulses = []
        for i in range(8):
            c_pulses.append((c_double * len(pulses[i]))(*pulses[i]))
        c_pulses = (POINTER(c_double)*len(c_pulses))(*c_pulses)
        #print(type(c_pulses))

        ttype = c_int * 8
        length = (ttype * seg_num)(*(tuple(i) for i in length))
        loop = (c_ushort * len(loop))(*loop)
        seg_num = c_ushort(seg_num)

        # CRS_ASGPulseDownload(double **pulses, int length[][8], unsigned short* loop, unsigned short segmentNum);
        # pulses[i][2*j], pulses[i][2*j+1], 第i个通道的一对高低电平
        # length[i][j] 表示第i段Segment第j个通道pluses高+低电平的个数, 是2的倍数
        return self.__dll.CRS_ASGPulseDownload(c_pulses, length, loop, seg_num)

    def download_ADC_data(self, data):
        seg_num = len(data)
        loop = []

        en_sig = []
        length = [0] * seg_num

        seg_idx = -1
        for l, seg_data in data:
            seg_idx += 1
            loop.append(l)
            pre_lvl = 1
            st = 0
            for tm, lvl in seg_data:
                if lvl != pre_lvl:
                    length[seg_idx] += 1
                    en_sig.append(st)
                    pre_lvl = lvl
                    st = 0
                st += tm
            length[seg_idx] += 1
            en_sig.append(st)
            if length[seg_idx] % 2 == 1:
                length[seg_idx] += 1
                en_sig.append(0)
        
        # print('en_sig:', en_sig)
        # print('length:', length)
        # print('loop', loop)
        # print('seg_num', seg_num)

        en_sig = (c_longlong * len(en_sig))(*en_sig)
        length = (c_int * len(length))(*length)
        loop = (c_ushort * len(loop))(*loop)
        seg_num = c_ushort(seg_num)

        return self.__dll.CRS_ADCENSignalDownload(en_sig, length, loop, seg_num)

    def set_DDS_AWG_mode(self, freq_ch1, freq_ch2, ph_ch1, ph_ch2, amp_ch1, amp_ch2, bias_ch1, bias_ch2):
        freq_ch1 = c_double(freq_ch1)
        freq_ch2 = c_double(freq_ch2)
        ph_ch1  = c_double(ph_ch1)
        ph_ch2  = c_double(ph_ch2)
        amp_val1 = c_ushort(amp_ch1)
        amp_val2 = c_ushort(amp_ch2)
        bias_ch1 = c_short(bias_ch1)
        bias_ch2 = c_short(bias_ch2)
        return self.__dll.CRS_SetDDSAWGMode(freq_ch1, freq_ch2, ph_ch1, ph_ch2, amp_val1, amp_val2, bias_ch1, bias_ch2)

    def start_DDS(self):
        return self.__dll.CRS_StartDDSBroadcast()

    def set_CRS_params(self, params):
        return self.__dll.CRS_SetCRSParams(params)
    
    def set_AWG_biases(self, bias_ch1, bias_ch2):
        bias_ch1 = c_short(bias_ch1)
        bias_ch2 = c_short(bias_ch2)
        return self.__dll.CRS_SetAWGBiases(bias_ch1, bias_ch2)

    def set_TDC_callback(self, func):
        if type(func) == TDC_CALLBACKTYPE:
            return self.__dll.CRS_SetTDCCallbackFunc(func)
        else:
            return False

    def download_TDC_calibration(self, data):
        if len(data) == 4 and len(data[0]) == 200:
            cdata = ((c_ubyte * 200) * 4)()
            for i in range(4):
                for j in range(200):
                    cdata[i][j] = data[i][j]
            return self.__dll.CRS_TDCDownloadCalibration(cdata)
        else:
            raise TypeError("{}.download_TDC_calibration(data): data size is not [4][200]".format(type(self).__name__))

    def set_TDC_params(self, grp1_length, grp2_length, grp1_sw, grp2_sw, grp1_mode, grp2_mode):
        grp1_length = c_int(grp1_length)
        grp2_length = c_int(grp2_length)
        grp1_sw = c_bool(grp1_sw)
        grp2_sw = c_bool(grp2_sw)
        grp1_mode = c_int(grp1_mode)
        grp2_mode = c_int(grp2_mode)
        return self.__dll.CRS_SetTDCParams(grp1_length, grp2_length, grp1_sw, grp2_sw, grp1_mode, grp2_mode)

    def set_clock_source(self, src):
        src = c_int(src)
        return sefl.__dll.CRS_SetClockSource(src)
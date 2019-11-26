# CRS API 调用流程说明

- [CRS API 调用流程说明](#crs-api-%e8%b0%83%e7%94%a8%e6%b5%81%e7%a8%8b%e8%af%b4%e6%98%8e)
  - [AWG](#awg)
    - [C++：](#c)
    - [Python](#python)
  - [ASG](#asg)
    - [C++](#c)
    - [Python](#python-1)
  - [DAQ](#daq)
    - [C++](#c-1)
    - [Python](#python-2)
  - [DDS](#dds)
    - [C++](#c-2)
    - [Python](#python-3)
  - [TDC](#tdc)
    - [C++](#c-3)
    - [Python](#python-4)

我们将按功能来说明API的调用顺序。

## AWG

### C++：
- 调用 `CRS_InitDevice` 初始化 SDK 和设备
- 调用 `CRS_ConnectDievce` 与设备建立通信连接
- 调用 `CRS_SetCRSParams` 设置工作状态和参数，如果只使用 AWG 功能参数设置如下
>```C++
> Params p;
> p.broadcastMode = 0;
> p.isDDSModeOpen = 0;
> p.isAWGModeOpen = 1;
> p.isDAQModeOpen = 0;
> for (int i = 0; i < 8; ++i)
> {
>     p.ASGChannelState[i] = 0;
> }
> ```
- 调用 `CRS_SetAWGBiases` 设置 AWG 未播放状态时的默认电平 
- 调用 `CRS_LoadCodeToDevice` 将 AWG 波形代码传入SDK 进行处理
- 调用 `CRS_StartBroadcast` 开始播放
- 调用 `CRS_StopBroadcast` 停止播放
- 调用 `CRS_CloseDevice` 断开与设备间的通信

具体参考示例：
 
### Python
- 首先实例化一个 `CRSDevice` 对象 `device = CRSDevice()`
- 调用 `init_device` 初始化 SDK 和设备
- 调用 `connect_device` 与设备建立通信连接
- 调用 `set_CRS_params` 设置工作状态和参数，如果只使用 AWG 功能参数设置如下
> ```Python
> param = Params()
> param.broadcastMode = 0
> param.isDDSModeOpen = 0
> param.isDAQModeOpen = 0
> param.isAWGModeOpen = 1
> param.ASGChannelState = (c_ushort * 8)(0,0,0,0,0,0,0,0)
> ```
- 调用 `set_AWG_biases` 设置 AWG 未播放状态时的默认电平 
- 调用 `load_code_to_device` 将 AWG 波形代码传入SDK 进行处理
- 调用 `start` 开始播放
- 调用 `stop` 停止播放
- 调用 `close_device` 断开与设备间的通信

具体参考示例：example_AWG.py

## ASG

### C++
- 调用 `CRS_InitDevice` 初始化SDK和设备
- 调用 `CRS_ConnectDievce` 与设备建立通信连接
- 调用 `CRS_SetCRSParams` 设置工作状态和参数，如果只使用 ASG 功能参数设置如下
>```C++
> Params p;
> p.broadcastMode = 0;
> p.isDDSModeOpen = 0;
> p.isAWGModeOpen = 0;
> p.isDAQModeOpen = 0;
> for (int i = 0; i < 8; ++i)
> {
>     p.ASGChannelState[i] = 1;
> }
> ```
- 调用 `CRS_SetASGDefauleLevel` 设置 ASG 默认电平 
- 调用 `CRS_ASGPulseDownload` 下载 ASG 数据
- 调用 `CRS_StartBroadcast` 开始播放
- 调用 `CRS_StopBroadcast` 停止播放
- 调用 `CRS_CloseDevice` 断开与设备间的通信

具体参考示例：

### Python
- 首先实例化一个 `CRSDevice` 对象 `device = CRSDevice()`
- 调用 `init_device` 初始化 SDK 和设备
- 调用 `connect_device` 与设备建立通信连接
- 调用 `set_CRS_params` 设置工作状态和参数，如果只使用AWG功能参数设置如下
> ```Python
> param = Params()
> param.broadcastMode = 0
> param.isDDSModeOpen = 0
> param.isDAQModeOpen = 0
> param.isAWGModeOpen = 0
> param.ASGChannelState = (c_ushort * 8)(1,1,1,1,1,1,1,1)
> ```
- 调用 `set_ASG_default` 设置 ASG 默认电平 
- 调用 `download_ASG_pulse_data` 下载 ASG 数据
- 调用 `start` 开始播放
- 调用 `stop` 停止播放
- 调用 `close_device` 断开与设备间的通信

具体参考示例：example_ASG.py

## DAQ

### C++
- 调用 `CRS_InitDevice` 初始化 SDK 和设备
- 调用 `CRS_ConnectDievce` 与设备建立通信连接
- 调用 `CRS_SetCRSParams` 设置工作状态和参数，如果只使用 DAQ 功能参数设置如下
>```C++
> Params p;
> p.broadcastMode = 0;
> p.isDDSModeOpen = 0;
> p.isAWGModeOpen = 0;
> p.isDAQModeOpen = 1;
> for (int i = 0; i < 8; ++i)
> {
>     p.ASGChannelState[i] = 0;
> }
> ```
- 调用 `CRS_ADCENSignalDownload` 下载 DAQ 数据
- 调用 `CRS_SetDAQCallbackFunc` 设置回调函数，建议启动一个线程来处理采集到的数据
- 调用 `CRS_SetStatusCallback` 设置状态回调，当缓存区数据溢出时该回调会被触发
- 调用 `CRS_StartBroadcast` 开始播放
- 调用 `CRS_StopBroadcast` 停止播放
- 调用 `CRS_CloseDevice` 断开与设备间的通信

具体参考示例：

### Python
- 首先实例化一个 `CRSDevice` 对象 `device = CRSDevice()`
- 调用 `init_device` 初始化 SDK 和设备
- 调用 `connect_device` 与设备建立通信连接
- 调用 `set_CRS_params` 设置工作状态和参数，如果只使用 DAQ 功能参数设置如下
> ```Python
> param = Params()
> param.broadcastMode = 0
> param.isDDSModeOpen = 0
> param.isDAQModeOpen = 1
> param.isAWGModeOpen = 0
> param.ASGChannelState = (c_ushort * 8)(0,0,0,0,0,0,0,0)
> ```
- 调用 `download_ADC_data` 设置 AWG 未播放状态时的默认电平 
- 调用 `set_DAQ_callback` 设置回调函数，建议启动一个线程来处理采集到的数据
- 调用 `set_status_callback` 设置状态回调，当缓存区数据溢出时该回调会被触发
- 调用 `start` 开始播放
- 调用 `stop` 停止播放
- 调用 `close_device` 断开与设备间的通信

具体参考示例：example_DAQ.py

## DDS

### C++
- 调用 `CRS_InitDevice` 初始化 SDK 和设备
- 调用 `CRS_ConnectDievce` 与设备建立通信连接
- 调用 `CRS_SetCRSParams` 设置工作状态和参数，如果只使用 DDS 功能参数设置如下
>```C++
> Params p;
> p.broadcastMode = 0;
> p.isDDSModeOpen = 1;
> p.isAWGModeOpen = 0;
> p.isDAQModeOpen = 0;
> for (int i = 0; i < 8; ++i)
> {
>     p.ASGChannelState[i] = 0;
> }
> ```
- 调用 `CRS_SetDDSAWGMode` 设置 DDS 参数
- 调用 `CRS_StartBroadcast` 开始播放
- 调用 `CRS_StopBroadcast` 停止播放
- 调用 `CRS_CloseDevice` 断开与设备间的通信

具体参考示例：

### Python
- 首先实例化一个 `CRSDevice` 对象 `device = CRSDevice()`
- 调用 `init_device` 初始化 SDK 和设备
- 调用 `connect_device` 与设备建立通信连接
- 调用 `set_CRS_params` 设置工作状态和参数，如果只使用 DDS 功能参数设置如下
> ```Python
> param = Params()
> param.broadcastMode = 0
> param.isDDSModeOpen = 1
> param.isDAQModeOpen = 0
> param.isAWGModeOpen = 0
> param.ASGChannelState = (c_ushort * 8)(0,0,0,0,0,0,0,0)
> ```
- 调用 `set_DDS_AWG_mode` 设置 DDS 参数
- 调用 `start` 开始播放
- 调用 `stop` 停止播放
- 调用 `close_device` 断开与设备间的通信

具体参考示例：example_DDS.py

## TDC

### C++
- 调用 `CRS_InitDevice` 初始化SDK和设备
- 调用 `CRS_ConnectDievce` 与设备建立通信连接
- 调用 `CRS_SetCRSParams` 设置工作状态和参数，如果只使用 TDC 功能参数设置如下
>```C++
> Params p;
> p.broadcastMode = 0;
> p.isDDSModeOpen = 0;
> p.isAWGModeOpen = 0;
> p.isDAQModeOpen = 0;
> for (int i = 0; i < 8; ++i)
> {
>     p.ASGChannelState[i] = 0;
> }
> ```
- 调用 `CRS_TDCDownloadCalibration` 设置 TDC 校准数据
- 调用 `CRS_SetTDCParams` 设置 TDC 参数
- 调用 `CRS_SetTDCCallbackFunc` 设置 TDC 的数据回调函数
- 调用 `CRS_SetStatusCallback` 设置状态回调，当缓存区数据溢出时该回调会被触发
- 调用 `CRS_StartBroadcast` 开始播放
- 调用 `CRS_StopBroadcast` 停止播放
- 调用 `CRS_CloseDevice` 断开与设备间的通信
具体参考示例：

### Python
- 首先实例化一个 `CRSDevice` 对象 `device = CRSDevice()`
- 调用 `init_device` 初始化 SDK 和设备
- 调用 `connect_device` 与设备建立通信连接
- 调用 `set_CRS_params` 设置工作状态和参数，如果只使用 TDC 功能参数设置如下
> ```Python
> param = Params()
> param.broadcastMode = 0
> param.isDDSModeOpen = 0
> param.isDAQModeOpen = 0
> param.isAWGModeOpen = 0
> param.ASGChannelState = (c_ushort * 8)(0,0,0,0,0,0,0,0)
> ```
- 调用 `download_TDC_calibration` 设置 TDC 校准数据
- 调用 `set_TDC_params` 设置 TDC 参数
- 调用 `set_TDC_callback` 设置 TDC 的数据回调函数
- 调用 `set_status_callback` 设置状态回调，当缓存区数据溢出时该回调会被触发
- 调用 `start` 开始播放
- 调用 `stop` 停止播放
- 调用 `close_device` 断开与设备间的通信

具体参考示例：example_TDC.py


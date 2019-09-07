import time
import psutil
import platform
import json
import requests
from pynvml import *
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def byte2str(n, d = 2):
    s = 'B'
    if n >= 1024:
        n/=1024
        s = 'K'
    if n >= 1024:
        n/=1024
        s = 'M'
    if n >= 1024:
        n/=1024
        s = 'G'
    if n >= 1024:
        n/=1024
        s = 'T'
    return '{:.2f}{}'.format(n,s)

def get_plist():
    p_list = []
    p_list_dict = {}
    for i in psutil.process_iter():
    #     print(i.as_dict())
        p_list.append((i.as_dict()['cpu_percent'],i.as_dict()['username'],i.as_dict()['name']))
        p_list_dict[str(i.as_dict()['pid'])]=(i.as_dict()['cpu_percent'],i.as_dict()['username'],i.as_dict()['name'])
    return p_list,p_list_dict

def get_gpu_status(p_list_dict):
    gpu_status_list = []
    nvmlInit()
    deviceCount = nvmlDeviceGetCount()
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        procs = nvmlDeviceGetComputeRunningProcesses(handle)
        mem = 0
        user = None
        for p in procs:
            if p.usedGpuMemory > mem:
                user = '{}:{}'.format(p_list_dict[str(p.pid)][1],
                                         byte2str(p.usedGpuMemory))
        status = {
                       'gpu_no': i,
                       'gpu_name': nvmlDeviceGetName(handle).decode('utf-8'),
                       'gpu_memory_status': '{}/{}'.format(byte2str(nvmlDeviceGetMemoryInfo(handle).used),byte2str(nvmlDeviceGetMemoryInfo(handle).total)),
                       'gpu_util': nvmlDeviceGetUtilizationRates(handle).gpu,
                       'gpu_memory': round(100*nvmlDeviceGetMemoryInfo(handle).used/nvmlDeviceGetMemoryInfo(handle).total,2),
                       'gpu_temperature': nvmlDeviceGetTemperature(handle,0),
                       'top_gpu_user': user,
                   }
        gpu_status_list.append(status)
    return gpu_status_list

def get_sys_info():
    sys_dic = {'name': 'MIB',
               'details': {'cpu':'XEON E5 6666','cpu_cores':8, 'memory':"16GB*4&2666MHz",'gpu':'RTX 2080 Ti*2'},
               'timestamp': 1932846198,
               'cpu_total': 0.73,
               'cpu_per_core': [0.0,0.43,0.45,0.56,0.89,0.01,0.01,0.02],
               'memory_status': '562M/38.0G',
               'memory_percentage': 0.07,
               'top_cpu_user': 'agent_h',
               'gpu_status':[
                   {
                       'gpu_no': 0,
                       'gpu_name': 'RTX 2080 Ti',
                       'gpu_memory_status': '12M/8119M',
                       'gpu_util': 0.78,
                       'gpu_memory': 0.23,
                       'gpu_temperature': 48,
                       'top_gpu_user': 'agent_n',
                   },
                   {
                       'gpu_no': 1,
                       'gpu_name': 'RTX 2080 Ti',
                       'gpu_memory_status': '3434M/8119M',
                       'gpu_util': 0.33,
                       'gpu_memory': 0.75,
                       'gpu_temperature': 78,
                       'top_gpu_user': 'alien_z',
                   }
               ]
              }
    sys_dic['name']=get_ip()
    sys_dic['timestamp']=time.time()
    sys_dic['cpu_total']=psutil.cpu_percent(interval=.5, percpu=False)
    sys_dic['cpu_per_core']=psutil.cpu_percent(interval=.5, percpu=True)
    sys_dic['memory_status']='{}/{}'.format(byte2str(psutil.virtual_memory().used),byte2str(psutil.virtual_memory().total))
    sys_dic['memory_percentage'] = psutil.virtual_memory().percent
    p_list,p_list_dict=get_plist()
    sys_dic['top_cpu_user']='{}:{}:{}%/{}%'.format(sorted(p_list)[-1][1],sorted(p_list)[-1][2],sorted(p_list)[-1][0],
                                                   str(len(sys_dic['cpu_per_core'])*100))
    sys_dic['gpu_status']=get_gpu_status(p_list_dict)
    sys_dic['details']={'cpu':platform.processor(),
                        'cpu_cores':str(len(sys_dic['cpu_per_core'])),
                        'memory':byte2str(psutil.virtual_memory().total),
                        'gpu':[x['gpu_name'] for x in sys_dic['gpu_status']]
                                          
    }
    return sys_dic


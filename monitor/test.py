import requests
import json
from datetime import datetime
import time
dic = {
        'name': 'MIB',
        'details': {'cpu':'XEON E5 6666','cpu_cores':8, 'memory':"16GB*4&2666MHz",'gpu':'RTX 2080 Ti*2'},
        'timestamp': time.time(),
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

data = json.dumps(dic)
url = 'http://127.0.0.1:5000/add_machine'
header = {'Content-Type': "application/json"}
response = requests.post(url, data=data, headers=header)
print(response.content.decode('utf-8'))


url = 'http://127.0.0.1:5000/get_machines'
response = requests.get(url)
print(response.content.decode('utf-8'))

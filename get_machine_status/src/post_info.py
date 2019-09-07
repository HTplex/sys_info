import json
import requests
import time
from get_sys_info import *

while True:
    try:
        dic = get_sys_info()
        data = json.dumps(dic)
        url = 'http://3.14.87.92/add_machine'
        header = {'Content-Type': "application/json"}
        response = requests.post(url, data=data, headers=header)
#         print(response.content.decode('utf-8'))
        time.sleep(15)
    except:
        print("post failed")
        


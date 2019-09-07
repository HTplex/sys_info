import datetime

ip_str = {
    '10.229.0.4':'KAIJU',
    '10.229.0.6':'MIB',
    '10.229.0.8':'JAEGER',
    '10.229.2.201':'MENGLIN',
    '10.229.2.6':'LAIDT1',
    '10.229.2.7':'LAIDT2',
    '10.229.2.8':'LAIDT3',
    '10.229.2.9':'LAIDT4',
    '10.229.2.10':'LAIDT5',
    '10.229.2.11':'LAIDT6',
    '10.229.2.12':'LAIDT7',
    '10.229.2.13':'LAIDT8',
}

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
#     percent = ""
    filledLength = int(length * iteration // total)
#     print(filledLength)
    bar = fill * filledLength + ' ' * (length - filledLength)
    return str('%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    
def get_status_string(status_dict, mode = "tiny_wide"):
    s = ''
#     s += "{:=^119}\n".format(" "+status_dict["name"]+": "+datetime.datetime.fromtimestamp(status_dict["timestamp"]).strftime('%c')+" ")
    name = status_dict["name"]
    if name in ip_str:
        name = ip_str[name]
    s += "+{:-^119}+\n".format(" "+name+": "+status_dict["timestamp"]+" ")
    s += '|CPU: {: <60}   {: >51}|\n'.format(printProgressBar(status_dict["cpu_total"],100,length = 20, suffix = str(status_dict["top_cpu_user"])),
                                    "MEM: "+printProgressBar(status_dict["memory_percentage"],100,length = 20, suffix = status_dict["memory_status"]))
#     s += 'MEM: ' + printProgressBar(status_dict["memory_percentage"],100,length = 15, suffix = status_dict["memory_status"])
    for i,g in enumerate(status_dict["gpu_status"]):
        s += '|{}: {:<19}, Util:{: <29} Mem: {: <39} {: >15}|\n'.format(str(i),
                                    g["gpu_name"],
                                    printProgressBar(g["gpu_util"],100,length = 15,suffix = "{}C".format(g["gpu_temperature"])),
                                    printProgressBar(g["gpu_memory"],100,suffix = g["gpu_memory_status"],length = 15),
                                                     str(g["top_gpu_user"]))
    s+="+{:-^119}+\n\n".format("")
    return s

def get_machine_info(print_result = True):
    url = 'http://3.14.87.92/get_machines'
    response = requests.get(url)
    resp = json.loads(response.content.decode('utf-8'))

    # print(json.loads(resp))
    info_dict = {}
    for re in resp:
        if re["name"] not in info_dict:
            info_dict[re["name"]] = re
        else:
            if re["timestamp"]>info_dict[re["name"]]["timestamp"]:
                info_dict[re["name"]] = re
    # print(info_dict)
    # keys = sorted(list(info_dict.keys()))
    return_s = ""
    for i in ip_str:
        if i in info_dict:
            if print_result:
                print(get_status_string(info_dict[i]))
            return_s+=get_status_string(info_dict[i])
#             return_s+="\n"
    return return_s
            
get_machine_info()
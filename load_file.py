import os
import numpy as np
from nptdms import TdmsWriter, ChannelObject




def txt2tdms(file_path):
    print(file_path)
    data = np.loadtxt(file_path)
    new_file_path,file_name = os.path.split(file_path)
    print(new_file_path)
    file_name = file_name.split('.')[0]
    new_file_path = os.path.split(new_file_path)[0]
    print(file_name)
    print(new_file_path)
    new_file_path = os.path.join(os.path.dirname(file_path), file_name+'.tdms')
    with TdmsWriter(new_file_path) as tdms_writer:
        channel = ChannelObject('Group', 'Channel1', data)
        tdms_writer.write_segment([channel])





def load_csv(filepath):
    filename = []
    detail = []
    file = open(filepath, 'r', encoding="gbk")  # 读取以utf-8
    context = file.read()  # 读取成str
    list_result = context.split("\n")  # 以回车符\n分割成单独的行
    # 每一行的各个元素是以【,】分割的，因此可以
    length = len(list_result)-1
    print(length)
    for i in range(length):
        #print(list_result[i])
        _, x, y = list_result[i].split(", ")
        filename.append(x)
        detail.append(y)
    file.close()
    return filename, detail
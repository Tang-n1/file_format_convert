import os
import math
import logging
import numpy as np
from nptdms import TdmsWriter, ChannelObject

def get_logger(log_name):
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"  # 日期格式
    fp = logging.FileHandler('./{}.log'.format(log_name), encoding='utf-8')
    fs = logging.StreamHandler()
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])  # 调用
    logger = logging.getLogger(__name__)
    return logger

def mkdir_recursively(path):
    """
    Create the path recursively, same as os.makedirs().

    Return True if success, or return False.

    e.g.
    mkdir_recursively('d:\\a\\b\\c') will create the d:\\a, d:\\a\\b, and d:\\a\\b\\c if these paths does not exist.
    """

    # First transform '\\' to '/'
    local_path = path.replace('\\', '/')
    log = get_logger('file_load')

    path_list = local_path.split('/')
    print
    path_list

    if path_list is None: return False

    # For windows, we should add the '\\' at the end of disk name. e.g. C: -> C:\\
    disk_name = path_list[0]
    if disk_name[-1] == ':': path_list[0] = path_list[0] + '\\'

    dir = ''
    for path_item in path_list:
        dir = os.path.join(dir, path_item)
        print
        "dir:", dir
        if os.path.exists(dir):
            if os.path.isdir(dir):
                log.debug("mkdir skipped: {}, already exist.".format(dir))
            else:  # Maybe a regular file, symlink, etc.
                log.debug("Invalid directory already exist: {}".format(dir))
                return False
        else:
            try:
                os.mkdir(dir)
            except Exception as e:
                log.error("mkdir error: {}".format(dir))
                return False
    return True


def load_lvm():
    pass

def load_tdf_fdt():
    file_name = '1100MH_4_500'

    file_path = r"D:\WorkSpace\电磁信号\电磁信号数据\50-1100\\" + file_name + "\\TData"
    save_file_path = r'D:\WorkSpace\电磁信号\电磁信号数据\50-1100\\' + file_name + '\\NPY'
    mkdir_recursively(save_file_path)
    data_I = []
    data_Q = []
    data_IQ = []
    file_cnt = 0
    for sub_dir in os.listdir(file_path):
        # 循环文件夹中所有文件
        cnt = 0
        print('load %s' % sub_dir)
        with open(os.path.join(file_path, sub_dir), 'rb') as f:
            data = f.read()
            for x in bytes(data):
                if cnt < 32:
                    data_I.append(x)
                else:
                    data_Q.append(x)
                cnt = cnt + 1
                if cnt == 64:
                    cnt = 0
                # 保存数据2*32768为npy
                if len(data_Q) == 32768:
                    data_IQ.append(np.transpose([data_I, data_Q]))
                    data_I = []
                    data_Q = []

        f.close()
    all_data = np.array(data_IQ)
    per_len = math.ceil(len(data_IQ) / 5)
    for k in range(5):
        part_data = all_data[k * per_len:(k + 1) * per_len]
        save_file_name = os.path.join(save_file_path, "{}_{}.npy".format(file_name, str(k)))
        np.save(save_file_name, part_data)
        print('save %d file' % k)

def load_tdms():
    pass

def load_npy():
    pass

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





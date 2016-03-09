# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 浩瀚深度 All Rights Reserved.
    
    FileName: user_behavior_stats.py

    ProjectName: APPStats
    
    Description:
    
    History:
    v1.0.0, huanglvjun, 2016-03-02 15:49, Modify: 
    
"""

import os
import io
import configparser
# import ConfigParser
import datetime
from itertools import islice
import re
from collections import Counter


# parse config file
config = configparser.ConfigParser()
# config = ConfigParser.ConfigParser()
config.read('./user_behavior_stats.cfg')

XDR_PATH = config.get('global', 'XDR_PATH')
PREFIX = config.get('global', 'PREFIX')
POSTFIX = config.get('global', 'POSTFIX')
HOURLY = config.getint('global', 'HOURLY')
DELAY = config.getint('global', 'DELAY')

REGEX_FILE = config.get('global', 'REGEX_FILE')
OUT_PATH = config.get('global', 'OUT_PATH')
OUTFILE_PREFIX = config.get('global', 'OUTFILE_PREFIX')

DATA_SOURCE = config.get('global', 'DATA_SOURCE')
INTERFACE = config.get('global', 'INTERFACE')
NETWORK_TYPE = config.get('global', 'NETWORK_TYPE')
LINE1 = config.get('global', 'LINE1')
LINE2 = config.get('global', 'LINE2')

FILETIMEFORMAT = '%Y%m%d'
RECORDTIMEFORMAT = '%Y-%m-%d'
HOURFORMAT = '%H'

treat_time = datetime.datetime.now() - datetime.timedelta(hours=DELAY)
file_date = treat_time.strftime(FILETIMEFORMAT)
record_date = treat_time.strftime(RECORDTIMEFORMAT)
hour = treat_time.strftime(HOURFORMAT)


# 提取待处理文件列表
def scan_files(directory, prefix=None, postfix=None):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if special_file.startswith(prefix) and special_file.endswith(postfix):
                files_list.append(os.path.join(root, special_file))
    return files_list


# 载入匹配规则
app_regexes = {}
# with open(REGEX_FILE, 'r', encoding='utf-8') as regex_file:
with open(REGEX_FILE, 'r', encoding='utf-8') as regex_file:
    i = 0
    lines = regex_file.readlines()
    for line in islice(lines, 0, None):
        i += 1
        line_splited = line.replace('\n', '').split(',')
        if len(line_splited) != 8:
            print("line " + str(i) + " format error! " + line)
            continue
        if line_splited[5] == '0':
            print("warning: line " + str(i) + " format error! " + line)
            continue
        [app_code, behavior_id, system_id, channel_id, reg_host, host_type, reg_uri, uri_type] = line_splited[0:8]

        key = '|'.join([app_code, behavior_id, system_id, channel_id])
        # 考虑 正则表达式中是否可能包含 '|'
        app_regexes[key] = '|'.join([reg_host, host_type, reg_uri, uri_type])


pv_cnt = Counter()
uv_cnt = Counter()
uv_cnt1 = Counter()
if HOURLY == '0':
    aprefix = PREFIX + '_' + file_date + '_' + hour
else:
    aprefix = PREFIX + '_' + file_date + '_'


files = scan_files(XDR_PATH, aprefix, POSTFIX)
if not len(files):
    print('no input xdr file!')
    exit()


for file in files:
    with open(file, 'r') as input_file:
        lines = input_file.readlines()
        for line in lines:
            line_splited = line.split('|')
            if len(line_splited) != 4:
                continue

            telephone = line_splited[1]  # 用户手机号码
            host = line_splited[2]
            uri = line_splited[3]

            for key in app_regexes:
                [reg_host1, host_type1, reg_uri1, uri_type1] = app_regexes[key].split('|')[0:4]
                if host_type1 == '1' and host == reg_host1:
                    if uri_type1 == '2':
                        # 非开始位置包含
                        if uri.lower().__contains__(reg_uri1.lower()):
                            pv_key = key; uv_key = key + '|' + telephone
                            pv_cnt[pv_key] += 1
                            uv_cnt[uv_key] += 1
                            continue
                    elif uri_type1 == '3':
                        # 开始位置包含
                        if uri.lower().startswith(reg_uri1.lower()):
                            pv_key = key; uv_key = key + '|' + telephone
                            pv_cnt[pv_key] += 1
                            uv_cnt[uv_key] += 1
                            continue
                    elif uri_type1 == '4':
                        # 正则
                        if re.search(reg_uri1, uri, re.IGNORECASE):
                            pv_key = key; uv_key = key + '|' + telephone
                            pv_cnt[pv_key] += 1
                            uv_cnt[uv_key] += 1
                            continue
                        # 空
                    elif uri_type1 == '0':
                        pv_key = key; uv_key = key + '|' + telephone
                        pv_cnt[pv_key] += 1
                        uv_cnt[uv_key] += 1
                        continue

                if host_type1 == '2' and host.__contains__(reg_host1):
                    if uri_type1 == '2':
                        # 非开始位置包含
                        if uri.lower().__contains__(reg_uri1.lower()):
                            pv_key = key; uv_key = key + '|' + telephone
                            pv_cnt[pv_key] += 1
                            uv_cnt[uv_key] += 1
                            continue
                    elif uri_type1 == '3':
                        # 开始位置包含
                        if uri.lower().startswith(reg_uri1.lower()):
                            pv_key = key; uv_key = key + '|' + telephone
                            pv_cnt[pv_key] += 1
                            uv_cnt[uv_key] += 1
                            continue
                    elif uri_type1 == '4':
                        # 正则
                        if re.search(reg_uri1, uri, re.IGNORECASE):
                            pv_key = key; uv_key = key + '|' + telephone
                            pv_cnt[pv_key] += 1
                            uv_cnt[uv_key] += 1
                            continue
                        # 空
                    elif uri_type1 == '0':
                        pv_key = key; uv_key = key + '|' + telephone
                        pv_cnt[pv_key] += 1
                        uv_cnt[uv_key] += 1
                        continue

                if host_type1 == '4' and re.search(reg_host1, host, re.IGNORECASE):
                    if uri_type1 == '2':
                        # 非开始位置包含
                        if uri.lower().__contains__(reg_uri1.lower()):
                            pv_key = key; uv_key = key + '|' + telephone
                            pv_cnt[pv_key] += 1
                            uv_cnt[uv_key] += 1
                            continue
                    elif uri_type1 == '3':
                        # 开始位置包含
                        if uri.lower().startswith(reg_uri1.lower()):
                            pv_key = key; uv_key = key + '|' + telephone
                            pv_cnt[pv_key] += 1
                            uv_cnt[uv_key] += 1
                            continue
                    elif uri_type1 == '4':
                        # 正则
                        if re.search(reg_uri1, uri, re.IGNORECASE):
                            pv_key = key; uv_key = key + '|' + telephone
                            pv_cnt[pv_key] += 1
                            uv_cnt[uv_key] += 1
                            continue
                        # 空
                    elif uri_type1 == '0':
                        pv_key = key; uv_key = key + '|' + telephone
                        pv_cnt[pv_key] += 1
                        uv_cnt[uv_key] += 1
                        continue

# uv_cnt
# key: 'app_id|behavior_id|telephone'
# value: count
# 将key以分隔符split开，统计uv
for key in sorted(uv_cnt):
    k = '|'.join(key.split('|')[0:4])
    uv_cnt1[k] += 1

os.makedirs(OUT_PATH, exist_ok=True)
# 结果保存文件文件名
if HOURLY:
    out_filename = OUT_PATH + os.sep \
            + '_'.join(['hourly_', OUTFILE_PREFIX, DATA_SOURCE, INTERFACE, NETWORK_TYPE, file_date, hour]) + '.txt'
else:
    out_filename = OUT_PATH + os.sep \
            + '_'.join([OUTFILE_PREFIX, DATA_SOURCE, INTERFACE, NETWORK_TYPE, file_date]) + '.txt'

with open(out_filename, 'w') as out_file:

    out_file.write(LINE1 + '\n')
    out_file.write(LINE2 + '\n')
    # join two dict by same key
    for k in sorted(uv_cnt1.keys()):
        pv = str(pv_cnt[k])
        uv = str(uv_cnt1[k])
        line = '|'.join([k, record_date, pv, uv])
        print(line)
        out_file.write(line + '\n')


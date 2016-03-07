# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 浩瀚深度 All Rights Reserved.
    
    FileName: liveness3.py

    ProjectName: APPStats
    
    Description:
    
    History:
    v1.0.0, huanglvjun, 2016-03-02 15:49, Modify: 
    
"""

import os
import configparser
import datetime
from itertools import islice
import re
from collections import Counter


# parse config file
config = configparser.ConfigParser()
config.read('F:\cndmp\APPStats\com\hh\cndmp\\appbehavior\liveness.cfg')

XDR_PATH = config.get('global', 'XDR_PATH')
PREFIX = config.get('global', 'PREFIX')
POSTFIX = config.get('global', 'POSTFIX')
HOURLY = config.getint('global', 'HOURLY')
DELAY = config.getint('global', 'DELAY')

REGEX_FILE = config.get('global', 'REGEX_FILE')
OUT_PATH = config.get('global', 'OUT_PATH')

FILETIMEFORMAT = '%Y%m%d'
RECORDTIMEFORMAT = '%Y-%m-%d'
HOURFORMAT = '%H'

treat_time = datetime.datetime.now() - datetime.timedelta(hours=DELAY)
file_date = treat_time.strftime(FILETIMEFORMAT)
record_date = treat_time.strftime(RECORDTIMEFORMAT)
hour = treat_time.strftime(HOURFORMAT)

print(file_date)
print(record_date)
print(hour)


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
with open(REGEX_FILE, 'r', encoding='utf-8') as regex_file:
    i = 0
    lines = regex_file.readlines()
    for line in islice(lines, 0, None):
        i += 1
        line_splited = line.replace('\n', '').split(',')
        if len(line_splited) != 6:
            print("line " + str(i) + " format error! " + line)
            continue
        [app_id, behavior_id, reg_host, host_type, reg_uri, uri_type] = line_splited[0:6]

        key = app_id + '|' + behavior_id
        # 考虑 正则表达式中是否可能包含 '|'
        app_regexes[key] = '|'.join([reg_host, host_type, reg_uri, uri_type])


pv_cnt = Counter()
uv_cnt = Counter()
uv_cnt1 = Counter()
if HOURLY == '0':
    aprefix = PREFIX + '_' + file_date + '_' + hour
else:
    aprefix = PREFIX + '_' + file_date + '_'

print(aprefix)

files = scan_files(XDR_PATH, aprefix, POSTFIX)
print(files)
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
                if host_type1 == '1' and uri_type1 == '2':
                    if host == reg_host1 and uri.__contains__(reg_uri1):
                        # print("1: " + host)
                        pv_key = key; uv_key = key + '|' + telephone
                        pv_cnt[pv_key] += 1
                        uv_cnt[uv_key] += 1
                        continue
                elif host_type1 == '1' and uri_type1 == '3':
                    if host == reg_host1 and re.search(reg_uri1, uri):
                        # print("2: " + host)
                        pv_key = key; uv_key = key + '|' + telephone
                        pv_cnt[pv_key] += 1
                        uv_cnt[uv_key] += 1
                        continue
                elif host_type1 == '' and uri_type1 == '0':
                    if host == reg_host1:
                        # print("3: " + host)
                        pv_key = key; uv_key = key + '|' + telephone
                        pv_cnt[pv_key] += 1
                        uv_cnt[uv_key] += 1
                        continue
                elif host_type1 == '2' and uri_type1 == '2':
                    if host.__contains__(reg_host1) and uri.__contains__(reg_uri1):
                        # print("4: " + host)
                        pv_key = key; uv_key = key + '|' + telephone
                        pv_cnt[pv_key] += 1
                        uv_cnt[uv_key] += 1
                        continue
                elif host_type1 == '2' and uri_type1 == '3':
                    if host.__contains__(reg_host1) and re.search(reg_uri1, uri):
                        # print("5: " + host)
                        pv_key = key; uv_key = key + '|' + telephone
                        pv_cnt[pv_key] += 1
                        uv_cnt[uv_key] += 1
                        continue
                elif host_type1 == '2' and uri_type1 == '0':
                    if host.__contains__(reg_host1):
                        # print("6: " + host)
                        pv_key = key; uv_key = key + '|' + telephone
                        pv_cnt[pv_key] += 1
                        uv_cnt[uv_key] += 1
                        continue

# uv_cnt
# key: 'app_id|behavior_id|telephone'
# value: count
# 将key以分隔符split开，统计uv
for key in sorted(uv_cnt):
    k = '|'.join(key.split('|')[0:2])
    uv_cnt1[k] += 1

# 结果保存文件文件名
if not HOURLY:
    out_filename = OUT_PATH + os.sep + 'hourly_' + file_date + '_' + hour + '.txt'
else:
    out_filename = OUT_PATH + os.sep + 'daily_' + file_date + '.txt'

with open(out_filename, 'w') as out_file:
    # join two dict by same key
    for k in sorted(uv_cnt1.keys()):
        pv = str(pv_cnt[k])
        uv = str(uv_cnt1[k])
        line = '|'.join([k, record_date, pv, uv])
        out_file.write(line + '\n')


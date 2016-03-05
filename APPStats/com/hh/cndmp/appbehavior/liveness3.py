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

date = '2016-03-04'
pv_cnt = Counter()
uv_cnt = Counter()
uv_cnt1 = Counter()
# parse config file
config = configparser.ConfigParser()
config.read('F:\cndmp\APPStats\com\hh\cndmp\\appbehavior\liveness.cfg')

XDR_PATH = config.get('global', 'XDR_PATH')
PREFIX = config.get('global', 'PREFIX')
POSTFIX = config.get('global', 'POSTFIX')
HOURLY = config.get('global', 'POSTFIX')
REGEX_FILE = config.get('global', 'HOURLY')
OUT_PATH = config.get('global', 'OUT_PATH')

FILETIMEFORMAT = '%Y%m%d'
RECORDTIMEFORMAT = '%Y-%m-%d'
HOURFORMAT = '%H'
DELAY = 0


# 提取待处理文件列表
def scan_files(directory, prefix=None, postfix=None):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if special_file.startswith(prefix) and special_file.endswith(postfix):
                files_list.append(os.path.join(root, special_file))
    return files_list


# 载入匹配规则
print(REGEX_FILE)
app_regexes = {}
with open(REGEX_FILE, 'r', encoding='utf-8') as regex_file:
    i = 0
    lines = regex_file.readlines()
    for line in islice(lines, 1, None):
        i += 1
        line_splited = line.replace('\n', '').split(',')
        if len(line_splited) != 6:
            print("line " + str(i) + " format error! " + line)
            continue
        [app_id, behavior_id, reg_host, host_type, reg_uri, uri_type] = line_splited[0:6]

        key = app_id + '|' + behavior_id
        # # 考虑 正则表达式中是否可能包含 '|'
        app_regexes[key] = '|'.join([reg_host, host_type, reg_uri, uri_type])




treat_time = datetime.datetime.now() - datetime.timedelta(hours=DELAY)
file_date = treat_time.strftime(FILETIMEFORMAT)
record_date = treat_time.strftime(RECORDTIMEFORMAT)
hour = treat_time.strftime(HOURFORMAT)

print(file_date)
print(record_date)
print(hour)

if HOURLY == '0':
    aprefix = PREFIX + '_' + file_date + '_' + hour
else:
    aprefix = PREFIX + '_' + file_date + '_'

print(aprefix)

files = scan_files(XDR_PATH, aprefix, POSTFIX)
print(files)

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

print(pv_cnt)

for v in sorted(uv_cnt):
    key = '|'.join(v.split('|')[0:2])
    uv_cnt1[key] += 1

print(uv_cnt1)
print(uv_cnt1.keys())

for k in uv_cnt1.keys():
    pv = str(pv_cnt[k])
    uv = str(uv_cnt1[k])
    line = '|'.join([k, pv, uv])
    print(line)

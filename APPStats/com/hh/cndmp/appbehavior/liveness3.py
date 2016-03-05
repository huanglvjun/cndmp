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
import time
from itertools import islice
import re
from collections import Counter

date = '2016-03-04'
pv_cnt = Counter()
uv_cnt = Counter()
# parse config file
config = configparser.ConfigParser()
config.read('F:\cndmp\APPStats\com\hh\cndmp\\appbehavior\liveness.cfg')

XDR_PATH = config.get('global', 'XDR_PATH')
REGEX_FILE = config.get('global', 'REGEX_FILE')
OUT_PATH = config.get('global', 'OUT_PATH')

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

pv = {}
with open('F:\cndmp\APPStats\com\hh\cndmp\\appbehavior\\3rdpartyflow_20150812.txt', 'r') as input_file:
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
                    continue
            elif host_type1 == '1' and uri_type1 == '3':
                if host == reg_host1 and re.search(reg_uri1, uri):
                    print("2: " + host)
                    pv_key = key; uv_key = key + '|' + telephone
                    pv_cnt[pv_key] += 1
                    continue
            elif host_type1 == '' and uri_type1 == '0':
                if host == reg_host1:
                    print("3: " + host)
                    pv_key = key; uv_key = key + '|' + telephone
                    pv_cnt[pv_key] += 1
                    continue
            elif host_type1 == '2' and uri_type1 == '2':
                if host.__contains__(reg_host1) and uri.__contains__(reg_uri1):
                    print("4: " + host)
                    pv_key = key; uv_key = key + '|' + telephone
                    pv_cnt[pv_key] += 1
                    continue
            elif host_type1 == '2' and uri_type1 == '3':
                if host.__contains__(reg_host1) and re.search(reg_uri1, uri):
                    print("5: " + host)
                    pv_key = key; uv_key = key + '|' + telephone
                    pv_cnt[pv_key] += 1
                    continue
            elif host_type1 == '2' and uri_type1 == '0':
                if host.__contains__(reg_host1):
                    print("6: " + host)
                    pv_key = key; uv_key = key + '|' + telephone
                    pv_cnt[pv_key] += 1
                    continue

print(pv_cnt)


#        if host not in app_regexes:
#            continue
#
#         if host == "wkvip.laiwang.com" and uri.__contains__('/lws?sdkver'):
#             pv_1 += 1;set1.add(telephone);uv_1 = len(set1);continue
#         elif host == "data.seeyouyima.com" and uri.__contains__('/door'):
#             pv_2 += 1;set2.add(telephone);uv_2 = len(set2);continue


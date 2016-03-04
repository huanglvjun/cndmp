# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 浩瀚深度 All Rights Reserved.
    
    FileName: liveness.py
    
    ProjectName: IP_Res 
    
    Description:
    
    History:
    v1.0.0, huanglvjun, 2016-03-02 15:49, Modify: 
    
"""

import os
# import configparser
import time


date = '2016-03-04'


# parse config file
# config = ConfigParser.ConfigParser()
# config.read('./liveness.cfg')
# 
# XDR_PATH = config.get('global', 'XDR_PATH')
# REGEX_FILE = config.get('global', 'REGEX_FILE')
# OUT_PATH = config.get('global', 'OUT_PATH')
# 
# app_regexes = {}
# with open(REGEX_FILE, 'r', encoding='utf-8') as regex_file:
#     lines = regex_file.readlines()
#     i = 0
#     for line in lines:
#         i += 1
#         line_splited = line.replace('\n', '').split('\t')
#         if len(line_splited) != 4:
#             print("line " + str(i) + " format error! AS: " + line)
#             continue
#         [app_id, app_name, reg_host, reg_uri] = line_splited[0:4]
#         key = reg_host
#         pv_name = 'pv_' + app_name
#         # 考虑 正则表达式中是否可能包含 '|'
#         app_regexes[key] = reg_uri + '|' + app_name

[pv_1, pv_2, pv_3, pv_4, pv_5, pv_6, pv_7, pv_8, pv_9, pv_10, pv_11, pv_12,
 pv_13, pv_14, pv_15, pv_16, pv_17, pv_18, pv_19, pv_20, pv_21, pv_22, pv_23, pv_24, pv_25, pv_26] \
    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

[uv_1, uv_2, uv_3, uv_4, uv_5, uv_6, uv_7, uv_8, uv_9, uv_10, uv_11, uv_12,
 uv_13, uv_14, uv_15, uv_16, uv_17, uv_18, uv_19, uv_20, uv_21, uv_22, uv_23, uv_24, uv_25, uv_26] \
    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

set1 = set();set2 = set();set3 = set();set4 = set();set5 = set();set6 = set();set7 = set();set8 = set()
set9 = set();set10 = set();set11 = set();set12 = set();set13 = set();set14 = set();set15 = set();set16 = set()
set17 = set();set18 = set();set19 = set();set20 = set();set21 = set();set22 = set();set23 = set();set24 = set()
set25 = set();set26 = set()

with open('F:\cndmp\APPStats\com\hh\cndmp\\appbehavior\\3rdpartyflow_20150812.txt', 'r') as input_file:
    lines = input_file.readlines()
    for line in lines:
        line_splited = line.split('|')
        if len(line_splited) != 4:
            continue

        telephone = line_splited[1]  # 用户手机号码
        host = line_splited[2]
        uri = line_splited[3]

#        if host not in app_regexes:
#            continue

        if host == "wkvip.laiwang.com" and uri.__contains__('/lws?sdkver'):
            pv_1 += 1;set1.add(telephone);uv_1 = len(set1);continue
        elif host == "data.seeyouyima.com" and uri.__contains__('/door'):
            pv_2 += 1;set2.add(telephone);uv_2 = len(set2);continue
        elif host == "hi.huofar.com" and uri.__contains__('/dym/feeds'):
            pv_3 += 1;set3.add(telephone);uv_3 = len(set3);continue
        elif host == "3g.39.net" and uri.__contains__('/ymll/'):
            pv_4 += 1;set4.add(telephone);uv_4 = len(set4);continue
        elif host == "www.jingqizhushou.com" and uri.__contains__('/s/api'):
            pv_5 += 1;set5.add(telephone);uv_5 = len(set5);continue
        elif host == "www.xiaohongshu.com" and uri.__contains__('/api/1/sticker/sync'):
            pv_6 += 1;set6.add(telephone);uv_6 = len(set6);continue
        elif host == "app.ymatou.com" and uri.__contains__('/api/Special/NewBannerLists'):
            pv_7 += 1;set7.add(telephone);uv_7 = len(set7);continue
        elif host == "m.ymall.com" and uri.__contains__('/api/menu'):
            pv_8 += 1;set8.add(telephone);uv_8 = len(set8);continue
        elif host == "sp.kaola.com" and uri.__contains__('/api/guidance/'):
            pv_9 += 1;set9.add(telephone);uv_9 = len(set9);continue
        elif host == "www.shihuo.cn" and uri.__contains__('/app3/saveAppInfo'):
            pv_10 += 1;set10.add(telephone);uv_10 = len(set10);continue
        elif host == "v.lehe.com" and uri.__contains__('/goods/RecommendBanner'):
            pv_11 += 1;set11.add(telephone);uv_11 = len(set11);continue
        elif host == "beilou-photos.b0.upaiyun.com" and uri.__contains__('/products/'):
            pv_12 += 1;set12.add(telephone);uv_12 = len(set12);continue
        elif host == "m.taobao.com" and uri.__contains__('/rest/'):
            pv_13 += 1;set13.add(telephone);uv_13 = len(set13);continue
        elif host == "m.jd.com" and uri.__contains__('/stat/access'):
            pv_14 += 1;set14.add(telephone);uv_14 = len(set14);continue
        # elif host == ".yongche.name" and uri.__contains__('/u/images'):
        elif host.__contains__('yongche.name') and uri.__contains__('/u/images'):
            pv_15 += 1;set15.add(telephone);uv_15 = len(set15);continue
        elif host == "mapiproxy.10101111.com" and uri.__contains__('/resource/m/ucar/base/startnew'):
            pv_16 += 1;set16.add(telephone);uv_16 = len(set16);continue
        elif host == "common.diditaxi.com.cn" and uri.__contains__('/passenger/orderrecover'):
            pv_17 += 1;set17.add(telephone);uv_17 = len(set17);continue

        # elif host == "vector0.map.bdimg.com" and uri.__contains__('/vecdata/?qt=vVer.*&pcn=com.ubercab'):
        elif host == "vector0.map.bdimg.com" and uri.__contains__('/vecdata/?qt=vVer') and uri.__contains__('&pcn=com.ubercab'):
            pv_18 += 1;set18.add(telephone);uv_18 = len(set18);continue
        elif host == "customer.vvipone.com" and uri.__contains__('/vip/v4/customer/testServer'):
            pv_19 += 1;set19.add(telephone);uv_19 = len(set19);continue

        # elif host == ".kuaidadi.com" and uri.__contains__('/taxi/a/js.do'):
        elif host.__contains__('.kuaidadi.com') and uri.__contains__('/taxi/a/js.do'):
            pv_20 += 1;set20.add(telephone);uv_20 = len(set20);continue
        elif host == "www.didapinche.com" and uri.__contains__('/dida-web'):
            pv_21 += 1;set21.add(telephone);uv_21 = len(set21);continue
        elif host == "api.miyabaobei.com" and uri.__contains__('/index/navigation/'):
            pv_22 += 1;set22.add(telephone);uv_22 = len(set22);continue
        elif host == "sapi.beibei.com" and uri.__contains__('/martshow/search/'):
            pv_23 += 1;set23.add(telephone);uv_23 = len(set23);continue
        elif host == "rbmcm.suning.com" and uri.__contains__('/rbmcm/mobile/system'):
            pv_24 += 1;set24.add(telephone);uv_24 = len(set24);continue
        elif host == "mlt.app.api.muyingzhijia.com" and uri.__contains__('/api/apphome'):
            pv_25 += 1;set25.add(telephone);uv_25 = len(set25);continue
        elif host == "www.muaijie.com" and uri.__contains__('/appapi/index'):
            pv_26 += 1;set26.add(telephone);uv_26 = len(set26);continue

result_1 = '|'.join(['大姨吗', date, str(pv_1), str(uv_1)])
result_2 = '|'.join(['美柚', date, str(pv_2), str(uv_2)])
result_3 = '|'.join(['越来越好', date, str(pv_3), str(uv_3)])
result_4 = '|'.join(['姨妈来了', date, str(pv_4), str(uv_4)])
result_5 = '|'.join(['经期助手', date, str(pv_5), str(uv_5)])
result_6 = '|'.join(['小红书', date, str(pv_6), str(uv_6)])
result_7 = '|'.join(['洋码头', date, str(pv_7), str(uv_7)])
result_8 = '|'.join(['达令全球好货', date, str(pv_8), str(uv_8)])
result_9 = '|'.join(['考拉海购', date, str(pv_9), str(uv_9)])
result_10 = '|'.join(['识货', date, str(pv_10), str(uv_10)])
result_11 = '|'.join(['美丽说HIGO', date, str(pv_11), str(uv_11)])
result_12 = '|'.join(['密淘全球购', date, str(pv_12), str(uv_12)])
result_15 = '|'.join(['易到用车', date, str(pv_15), str(uv_15)])
result_16 = '|'.join(['神州专车', date, str(pv_16), str(uv_16)])
result_17 = '|'.join(['滴滴出行', date, str(pv_17), str(uv_17)])
result_18 = '|'.join(['Uber', date, str(pv_18), str(uv_18)])
result_19 = '|'.join(['一号专车', date, str(pv_19), str(uv_19)])
result_20 = '|'.join(['快的打车', date, str(pv_20), str(uv_20)])
result_21 = '|'.join(['嘀嗒拼车', date, str(pv_21), str(uv_21)])
result_22 = '|'.join(['蜜芽', date, str(pv_22), str(uv_22)])
result_23 = '|'.join(['贝贝母婴', date, str(pv_23), str(uv_23)])
result_24 = '|'.join(['红孩子母婴', date, str(pv_24), str(uv_24)])
result_25 = '|'.join(['母婴之家', date, str(pv_25), str(uv_25)])
result_26 = '|'.join(['母爱街', date, str(pv_26), str(uv_26)])

print(result_1)
print(result_2)
print(result_3)
print(result_4)
print(result_5)
print(result_6)
print(result_7)
print(result_8)
print(result_9)
print(result_10)
print(result_11)
print(result_12)
print(result_15)
print(result_16)
print(result_17)
print(result_18)
print(result_19)
print(result_20)
print(result_21)
print(result_22)
print(result_23)
print(result_24)
print(result_25)
print(result_26)


# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 浩瀚深度 All Rights Reserved.
    
    FileName: liveness.py
    
    ProjectName: IP_Res 
    
    Description:
    
    History:
    v1.0.0, huanglvjun, 2016-03-02 15:49, Modify: 
    
"""

date = '2016-03-02' # 统计话单对应日期，从话单文件夹提取

app = {}
app['wkvip.laiwang.com'] = '大姨吗'
app['data.seeyouyima.com'] = '美柚'
app['hi.huofar.com'] = '越来越好'

for k in app:
    print(k + '|' + app[k])

pv_dayima = 0
uv_dayima = 0
dayima = '大姨吗'
user_set_dayima = set()

pv_meiyou = 0
uv_meiyou = 0
meiyou = '美柚'
user_set_meiyou = set()

pv_yuelaiyuehao = 0
uv_yuelaiyuehao = 0
yuelaiyuehao = '越来越好'
user_set_yuelaiyuehao = set()


with open('app.txt', 'r') as input_file:
    lines = input_file.readlines()
    for line in lines:
        line_splited = line.split('\t')
        if len(line_splited) != 38:
            continue

        user_id = line_splited[5]  # 用户手机号码
        time = line_splited[18]  # 业务流开始时间，格式为yyyymmddhhmmss（24小时制）
        host = line_splited[24]
        url = line_splited[25]

        if host not in app:
            continue

        if host == "wkvip.laiwang.com" and url.__contains__('/lws?sdkver'):
            pv_dayima += 1
            user_set_dayima.add(user_id)
            uv_dayima = len(user_set_dayima)
            # print(dayima + '|' + date + '|' + host + '|' + user_id)
            continue

        elif host == "data.seeyouyima.com" and url.__contains__('/door'):
            pv_meiyou += 1
            user_set_meiyou.add(user_id)
            uv_meiyou = len(user_set_meiyou)
            continue

        elif host == "hi.huofar.com" and url.__contains__('/dym/feeds'):
            pv_yuelaiyuehao += 1
            user_set_yuelaiyuehao.add(user_id)
            uv_yuelaiyuehao = len(user_set_yuelaiyuehao)
            continue

    result_dayima = '|'.join([dayima, date, str(pv_dayima), str(uv_dayima)])
    result_meiyou = '|'.join([meiyou, date, str(pv_meiyou), str(uv_meiyou)])
    result_yuelaiyuehao = '|'.join([yuelaiyuehao, date, str(pv_yuelaiyuehao), str(uv_yuelaiyuehao)])

    print(result_dayima)
    print(result_meiyou)
    print(result_yuelaiyuehao)

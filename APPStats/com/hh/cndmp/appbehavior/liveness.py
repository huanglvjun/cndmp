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
import configparser
import time


date = '2016-03-03'


def config_parser():
    # parse config file
    config = configparser.ConfigParser()
    config.read('./liveness.cfg')

    XDR_PATH = config.get('global', 'XDR_PATH')
    REGEX_FILE = config.get('global', 'REGEX_FILE')
    OUT_PATH = config.get('global', 'OUT_PATH')

    app_regexes = {}
    with open(REGEX_FILE, 'r', encoding='utf-8') as regex_file:
        lines = regex_file.readlines()
        i = 0
        for line in lines:
            i += 1
            line_splited = line.replace('\n', '').split('\t')
            if len(line_splited) != 4:
                print("line " + str(i) + " format error! AS: " + line)
                continue
            [app_id, app_name, reg_host, reg_uri] = line_splited[0:4]
            key = reg_host
            pv_name = 'pv_' + app_name

            # 考虑 正则表达式中是否可能包含 '|'
            app_regexes[key] = reg_uri + '|' + app_name
        return app_regexes


def pvuv_stats():

    app_regexes = config_parser()

    with open('F:\cndmp\APPStats\com\hh\cndmp\\appbehavior\\app.txt', 'r') as input_file:
        lines = input_file.readlines()
        for line in lines:
            line_splited = line.split('\t')
            if len(line_splited) != 38:
                continue

            telephone = line_splited[5]  # 用户手机号码
            host = line_splited[24]
            uri = line_splited[25]

            if host not in app_regexes:
                continue

            for key in app_regexes:
                reg_host = key
                [reg_uri, app_name] = app_regexes[key].split('|')[0:1]

                if host == reg_host and uri.__contains__(reg_uri):
                    out = stats(app_name)
                else:
                    out = ''

            print(out)


def stats(pv=0, uv=0, name=''):
    pv += 1
    uv += 1
    out = name + '|' + str(pv) + '|' + str(uv)
    return out




if __name__ == "__main__":
    config_parser()
    pvuv_stats()
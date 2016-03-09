#!/bin/bash

########################################################################
# filename: app_host_filter.sh
# version: 1.0.1
# author: hlj
# date: 2016-01-07
# 功能：将话单文件按配置的host过滤，存放到指定目录，原话单文件不动
# 配置文件：app_host_filter.conf app_host.txt
# 参数：
# 修改历史：
# 作    者:
# 日    期：
# 修改内容：
########################################################################

########################################################################
# 函 数 名  : InitEnv
# 功能描述  : 初始化全局变量，定义时间格式，建立目录
# 输入参数  : 无
# 返 回 值  : 无
# 调用函数  : 无
# 修改历史      :
#  1.日    期   : 2015年04月23日
#    作    者   : hlj
#    修改内容   : 新生成函数
########################################################################
function InitEnv
{
    SCRIPT_NAME="$(basename $0 .sh)"
    DIR_INSTALL=$(cd $(dirname $0);pwd)
    FILE_CONF="${DIR_INSTALL}/${SCRIPT_NAME}.conf"
    DATE=$(date +'%Y%m%d')
    TIME=$(date +'%H%M%S')
    UTC=$(date +'%s')
    TREAT_TIME=`date --date='-60 minutes' "+%Y%m%d_%H"`
}

########################################################################

########################################################################
# 函 数 名  : ParseConf
# 功能描述  : 导入配置文件，检查是否有错误，定义与配置文件相关的变量
# 输入参数  : 无
# 返 回 值  : 无
# 调用函数  : 无
# 修改历史      :
#  1.日    期   : 2015年01月23日
#    作    者   : 曹海涛
#    修改内容   : 新生成函数
########################################################################
function ParseConf
{
    if ! [[ -s ${FILE_CONF} ]];then
        Echo "${DATE} ${TIME} Configuration file  not correctly parsed!\nexit\n"
        exit
    fi
    source ${FILE_CONF}
    mkdir -p ${DIR_LOG}

    #脚本运行正常日志
    LOG_NORMAL="${DIR_LOG}/${SCRIPT_NAME}_${DATE}.log"
    #脚本运行错误日志
    LOG_ERROR="${DIR_LOG}/${SCRIPT_NAME}_${DATE}.err"
    #脚本运行警告日志
    LOG_WARNING="${DIR_LOG}/${SCRIPT_NAME}_${DATE}.warnings"
    exec 2>>"${LOG_ERROR}"

    s1=`echo ${source_xdr_path} | sed 's#/##g' | wc -m`
    s2=`echo ${DIR_LOG} | sed 's#/##g' | wc -m`
    if [ ${s1} -le 3 ] || [ ${s2} -lt 3 ];then
        Echo "in configuration file: length of source_xdr_path or DIR_LOG was less then 3 or not correctly parsed!\nexit\n"
        exit
    fi
}
########################################################################

########################################################################
# 函 数 名  : Echo
# 功能描述  : 将信息写入脚本运行日志
# 输入参数  : 1：需写入信息
# 返 回 值  : 无
# 调用函数  : 无
# 修改历史      :
#  1.日    期   : 2015年04月23日
#    作    者   : hlj
#    修改内容   : 新生成函数
########################################################################
function Echo
{
    if (($# == 1));then
       local log="$1"
       echo -e "${DATE} ${TIME} |${log}" >> "${LOG_NORMAL}"
    else
       local log="$2"
       echo -e "${log}" >> "${LOG_NORMAL}"
    fi
}
########################################################################
 
########################################################################
# 函 数 名  : SetCrontab
# 功能描述  : 设置定时任务
# 输入参数  : 无
# 返 回 值  : 无
# 调用函数  : 无
# 修改历史      :
#  1.日    期   : 2015年04月23日
#    作    者   : hlj
#    修改内容   : 新生成函数
########################################################################
function SetCrontab
{
        local path_script="${DIR_INSTALL}/${SCRIPT_NAME}.sh"
        if ! egrep -q ${path_script} /etc/crontab;then
                echo "${SCRIPT_RUNTIME} root ${path_script}" >> /etc/crontab
                echo "install ${SCRIPT_NAME} in ${DIR_INSTALL} done! ^=^"
                exit
        fi
}
########################################################################

########################################################################
# 函 数 名  : CheckScript
# 功能描述  : 检查是否有相同的进程在运行，若存在，则退出本次进程
# 输入参数  : 无
# 返 回 值  : 无
# 调用函数  : Echo
# 修改历史      :
#  1.日    期   : 2015年04月23日
#    作    者   : hlj
#    修改内容   : 新生成函数
########################################################################
function CheckScript
{
        local path_script="${DIR_INSTALL}/${SCRIPT_NAME}.sh"
        local process="$$"
        num=$(ps -ef | grep -v grep | grep -v "${process}" | grep ${path_script} | wc -l)

        if ((num>0));then
                Echo "${path_script} already run:\n$(ps -ef | grep -v grep | grep -v "${process}" | grep ${path_script})\nexit\n"
                exit
        fi
}
########################################################################


########################################################################
# 函 数 名  : host_filter
# 功能描述  : 将话单文件按配置的host进行过滤，存放到指定目录，将原话单文件不动
# 输入参数  : 1：需写入信息
# 返 回 值  : 无
# 调用函数  : 无
# 修改历史      :
#  1.日    期   : 2016-01-07
#    作    者   : hlj
#    修改内容   : 新生成函数
########################################################################
function host_filter
{
    mkdir -p ${filter_xdr_path}

    cd ${source_xdr_path}
    if [ ${tmp_treat_time} == 0 ];then
        aprefix=${prefix}${TREAT_TIME}
        echo "tmp_treat_time == 0 aprefix=${prefix}${TREAT_TIME}"
    else
        aprefix=${prefix}${tmp_treat_time}
        echo "aprefix=${prefix}${tmp_treat_time}"
    fi

    file_number=`ls ./ | grep "^${aprefix}" | grep "${postfix}$"| wc -l `
    Echo "file_number: ${file_number}"
    if [ ${file_number} == 0 ];then
        Echo "No files(${aprefix}*${postfix}) exists in source_xdr_path:${source_xdr_path}"
        exit
    fi

    for file in `ls ./${aprefix}*${postfix}`
    do
    Echo "file: "${file}

    file_basename="$(basename "${file}" .${postfix})"
    filter_xdr_filename_tmp=${file_basename}".tmp"
    filter_xdr_filename=${file_basename}"."txt

    cat ${file} | awk -F '\t' -v filter_resource_file=${filter_resource_file} -v filter_xdr_path=${filter_xdr_path} -v filter_xdr_filename_tmp=${filter_xdr_filename_tmp} -v log_warning=${LOG_WARNING} '
    BEGIN{
        while(getline < filter_resource_file > 0)
        {
            split($1,info,",")
            if( info[6] == 0 || info[8] == 0 )
            {   print strftime("%y-%m-%d %T") >> log_warning
                print "the following regexes were skipped when filter xdr record." >> log_warning
                print $1 >> log_warning
            }
            else
            {
                regex_array[info[5]]=info[6]
            }
        }
        # for(key in regex_array) {print key": "regex_array[key]}
    }

        {
            imei = $5
            telephone = $6
            host = $25
            uri = $26
            for(key in regex_array)
                {
                    if( regex_array[key] == 1 && host == key )
                    {
                        out = imei"|"telephone"|"host"|"uri
                        print out >> filter_xdr_path"/"filter_xdr_filename_tmp
                        break
                    }
                    else if( regex_array[key] == 2 && index(host,key) != 0 )
                    {
                        out = imei"|"telephone"|"host"|"uri
                        print out >> filter_xdr_path"/"filter_xdr_filename_tmp
                        break
                    }
                    else if( regex_array[key] == 4 && host~key )
                    {
                        out = imei"|"telephone"|"host"|"uri
                        print out >> filter_xdr_path"/"filter_xdr_filename_tmp
                        break
              
                    }
                    else
                    {
                        continue
                    }
                }
        }'
        filter_file_number=`ls ${filter_xdr_path}/ | grep "${filter_xdr_filename_tmp}"| wc -l `
        Echo "filter_file_number in ${filter_xdr_path}: ${filter_file_number}"
        if [ ${filter_file_number} -gt 0 ];then
            Echo "mv ${filter_xdr_filename_tmp} ${filter_xdr_path}/${filter_xdr_filename}"
            mv ${filter_xdr_path}/${filter_xdr_filename_tmp} ${filter_xdr_path}/${filter_xdr_filename}
        fi
    done
}
########################################################################


########################################################################
# 函 数 名  : CLEAR
# 功能描述  : 删除话单文件暂存目录
# 输入参数  : 无
# 返 回 值  : 无
# 调用函数  : 无
# 修改历史      :
#  1.日    期   : 2016-01-07
#    作    者   : hlj
#    修改内容   : 新生成函数
########################################################################
function Clear
{
    # 定期删除日志文件
    find  ${DIR_LOG}/ -maxdepth 1 -name "${SCRIPT_NAME}*" -mtime +${LOGSAVEDAY} -exec rm {} \;
}
########################################################################

########################################################################
# BEGINNING OF MAIN
########################################################################
#初始化环境变量
InitEnv
#导入并检查配置文件
ParseConf
#检查是否有相同的脚本运行，若有，则退出
CheckScript
#写入定时任务，当关闭临时处理时，脚本执行方式写入定时任务；启动临时处理时，脚本只运行一次
if [ ${tmp_treat_time} == 0 ];then
    SetCrontab
fi
#按host过滤话单
host_filter
#清除过期文件
Clear
########################################################################
# End of script
########################################################################

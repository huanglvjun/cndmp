#!/bin/bash

########################################################################
# filename: app_host_filter.sh
# version: 1.0.1
# author: hlj
# date: 2016-01-07
# 功能：将话单文件按配置的NAT IP地址段过滤，存放到指定目录，将原话单文件移动至另一指定目录
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
#    作    者   : 齐凯
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
    exec 2>>"${LOG_ERROR}"

    s1=`echo ${source_xdr_path} | sed 's#/##g' | wc -m`
    s2=`echo ${DIR_LOG} | sed 's#/##g' | wc -m`
    if [ ${s1} -le 3 ] || [ ${s2} -lt 3 ];then
        Echo "Configuration file  not correctly parsed!\nexit\n"
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
#    作    者   : 齐凯
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
#    作    者   : 齐凯
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
#    作    者   : 齐凯
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
# 函 数 名  : nat_xdr_filter
# 功能描述  : 将话单文件按配置的NAT IP地址段过滤，存放到指定目录，将原话单文件移动至另一指定目录
# 输入参数  : 1：需写入信息
# 返 回 值  : 无
# 调用函数  : 无
# 修改历史      :
#  1.日    期   : 2016-01-07
#    作    者   : hlj
#    修改内容   : 新生成函数
########################################################################
function nat_xdr_filter
{
    mkdir -p ${nat_xdr_path}
    mkdir -p ${all_xdr_path}
    
    cd ${source_xdr_path}
    file_number=`ls ./ | grep "^${prefix}" | grep "${postfix}$"| wc -l `
    Echo "file_number: ${file_number}"
    if [ ${file_number} == 0 ];then
        Echo "No files(${prefix}*${postfix}) exists in source_xdr_path:${source_xdr_path}"
        exit   
    fi    

    for file in `ls ./${prefix}*${postfix}`
    do
    Echo "file: "${file}
    
    file_basename="$(basename "${file}" .${postfix})"
    nat_xdr_filename_tmp=${file_basename}".tmp"
    nat_xdr_filename=${file_basename}"."${postfix}

    awk -F ',' -v nat_ip_file=${nat_ip_file} -v nat_xdr_path=${nat_xdr_path} -v nat_xdr_filename_tmp=${nat_xdr_filename_tmp} '
    BEGIN{
        while(getline < nat_ip_file > 0)
        {
            ip_array[$1]=$2
            print "ip_int_start: " $1 
            print "ip_int_end: " $2
        }
    }
    
        {    
            source_ip=$3
            source_ip2=gensub("'\''","","g",source_ip)
  
            split(source_ip2,ip_splited,".")
            ip_int=ip_splited[1]*(256**3)+ip_splited[2]*(256**2)+ip_splited[3]*256+ip_splited[4]
            for(key in ip_array)
                {   
                    if(ip_int-0 >= key-0 && ip_int-0 <= ip_array[key]-0)
                    {   
                        print $0 >> nat_xdr_filename_tmp
                        break
                    }
                }
        }' ${file}
        
        nat_file_number=`ls ./ | grep "${nat_xdr_filename_tmp}"| wc -l `
        Echo "nat_file_number: ${nat_file_number}"
        if [ ${nat_file_number} -gt 0 ];then
            Echo "mv ${nat_xdr_filename_tmp} ${nat_xdr_path}/${nat_xdr_filename}"
            mv ${nat_xdr_filename_tmp} ${nat_xdr_path}/${nat_xdr_filename}
        fi

        Echo "mv ${file} ${all_xdr_path}"
        mv ${file} ${all_xdr_path} 
    done
}
########################################################################

########################################################################
# 函 数 名  : nat_xdr_filter
# 功能描述  : 将话单文件按配置的NAT IP地址段过滤，存放到指定目录，将原话单文件移动至另一指定目录
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
    mkdir -p ${nat_xdr_path}

    cd ${source_xdr_path}
    file_number=`ls ./ | grep "^${prefix}" | grep "${postfix}$"| wc -l `
    Echo "file_number: ${file_number}"
    if [ ${file_number} == 0 ];then
        Echo "No files(${prefix}*${postfix}) exists in source_xdr_path:${source_xdr_path}"
        exit
    fi

    for file in `ls ./${prefix}*${postfix}`
    do
    Echo "file: "${file}

    file_basename="$(basename "${file}" .${postfix})"
    nat_xdr_filename_tmp=${file_basename}".tmp"
    nat_xdr_filename=${file_basename}"."txt

    zcat ${file} | awk -F '\t' -v nat_ip_file=${nat_ip_file} -v nat_xdr_path=${nat_xdr_path} -v nat_xdr_filename_tmp=${nat_xdr_filename_tmp} '
    BEGIN{
        while(getline < nat_ip_file > 0)
        {
            ip_array[$1]=$1
            # print "app host: " $1
        }
    }

        {
            imei = $5
            telephone = $6
            host = $25
            uri = $26
            for(key in ip_array)
                {
                    if(host == key)
                    {
                        out = imei"|"telephone"|"host"|"uri
                        print out >> nat_xdr_filename_tmp
                        break
                    }
                }
        }'

        nat_file_number=`ls ./ | grep "${nat_xdr_filename_tmp}"| wc -l `
        Echo "nat_file_number: ${nat_file_number}"
        if [ ${nat_file_number} -gt 0 ];then
            Echo "mv ${nat_xdr_filename_tmp} ${nat_xdr_path}/${nat_xdr_filename}"
            mv ${nat_xdr_filename_tmp} ${nat_xdr_path}/${nat_xdr_filename}
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
#写入定时任务
#SetCrontab
#按host过滤话单
host_filter
#清除过期文件
Clear
########################################################################
# End of script
########################################################################

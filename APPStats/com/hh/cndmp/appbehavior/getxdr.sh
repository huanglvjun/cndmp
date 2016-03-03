#!/usr/bin/env bash

cat 3rdpartyflow_20150812_15* | awk -F '\t' '
    {
    if ($25 == "wkvip.laiwang.com" || $25 == "data.seeyouyima.com" || $25 == "hi.huofar.com" ||
    $25 == "3g.39.net" || $25 == "www.jingqizhushou.com" || $25 == "www.xiaohongshu.com" ||
    $25 == "app.ymatou.com" || $25 == "m.ymall.com" || $25 == "sp.kaola.com" || $25 == "www.shihuo.cn"
    $25 == "v.lehe.com" || $25 == "beilou-photos.b0.upaiyun.com")
    {
        print $0
    }
        }' >> ../app.txt
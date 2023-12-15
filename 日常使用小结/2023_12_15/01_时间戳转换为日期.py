#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: liyi 
@file: 01_时间戳转换为日期.py
@time: 2023-12-15
@desc: 
"""
from datetime import datetime


# 获取时间戳
def timestamp_to_date(timestamp) -> str:
    """
    :param timestamp: 时间戳
        获取时间戳常见方式：
        import time
        from datetime import datetime
        # 方式一
        time.time()   1702621996.4947057
        # 方式二
        datetime.timestamp(datetime.now())  1702623255.463542
    :return str: "%Y-%m-%d %H:%M:%S"
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")



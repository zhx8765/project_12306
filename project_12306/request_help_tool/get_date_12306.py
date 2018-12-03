#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zqf'
import time


def get_date_time(date_str):
    return time.strftime('%a %b %d %Y', time.strptime(date_str, '%Y-%m-%d')) + ' 00:00:00 GMT+0800 (中国标准时间)'

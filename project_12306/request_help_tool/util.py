#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time

__author__ = 'Terry'

import re

def get_input_value_by_name(name, text):
    p = f'<input.*?name="{name}".*?value="(.*?)"'
    v = re.search(p, text, re.RegexFlag.S).group(1)
    return v

def gen_random_hex_str(num, uppered = False):
    s = ''
    for _ in range(num):
        s += random.choice('0123456789abcdef')

    if uppered:
        s = s.upper()

    return s

def gen_random_str(num, uppered = False):
    s = ''
    for _ in range(num):
        s += random.choice('0123456789abcdefghijklmnopqrstuvwxyz')

    if uppered:
        s = s.upper()

    return s

def get_13_time():
    return str(int(time.time()*1000))

def get_str_from_text(p, text):
    ret_str = ''
    try:
        ret_str = re.search(p, text).group(1)
    except:
        # 保存 text 和 p
        pass

    return ret_str

def get_first_str_by_text_multi(p, text):
    l = get_all_str_by_text_multi(p, text)
    if not l:
        # raise Exception("没有有效的值")
        return ''
    else:
        return l[0]

def get_all_str_by_text_multi(p, text):
    l = re.findall(p, text, re.M|re.S)
    return l

def xmlchar_2_cn(s):
    def convert_callback(matches):
        char_id = matches.group(1)
        try:
            return chr(int(char_id))
        except:
            return char_id

    ret = re.sub("&#(\d+)(;|(?=\s))", convert_callback, s)

    return ret

if __name__ == '__main__':
    # print('main')
    # s = ''
    # print(xmlchar_2_cn('&#25105;&#26159;&#27979;&#35797;&#20013;&#25991;abc123'))

    # print(gen_random_str(3))

    pass
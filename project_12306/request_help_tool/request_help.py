#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import parse_qsl

import requests

__author__ = 'Terry'

def make_session(debug=False):
    s = requests.session()
    s.verify = False
    s.trust_env = False
    s.headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/67.0.3396.87 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    if debug:
        s.proxies = {
            'http': '127.0.0.1:8888',
            'https': '127.0.0.1:8888',
        }

    return s

def print_headers_raw_to_dict(headers_raw_l):
    print("{\n    '" + ",\n    ".join(map(lambda s: "'" +
        "': '".join(s.strip().split(':')) + "'", headers_raw_l))[1:-1] + "'\n}")

def print_headers_raw_to_ordered_dict(headers_raw_l):
    print("OrderedDict([\n    (" + "),\n    ".join(map(lambda s: "('" + "': '".join(s.strip().split(':')) + "'", headers_raw_l))[1:-1] + "')\n])")

def print_headers_raw_to_dict_space(headers_raw_l):
    print("{\n    '" + ",\n    ".join(map(lambda s: "'" + "': '".join(s.strip().split('\t') if len(s.strip().split('\t'))>1 else [s.strip(), '']) + "'", headers_raw_l))[1:-1] + "'\n}")

def print_headers_raw_to_ordered_dict_space(headers_raw_l):
    print("OrderedDict([\n    (" + "),\n    ".join(map(lambda s: "('" + "', '".join(s.strip().split('\t') if len(s.strip().split('\t'))>1 else [s.strip(), '']) + "'", headers_raw_l))[1:-1] + "')\n])")

def print_dict_from_copy_headers(headers_raw):
    headers_raw = headers_raw.strip()
    headers_raw_l = headers_raw.splitlines()

    if 'HTTP/1.1' in headers_raw_l[0]:
        headers_raw_l.pop(0)
    if headers_raw_l[0].startswith('Host'):
        headers_raw_l.pop(0)
    if headers_raw_l[-1].startswith('Cookie'):
        headers_raw_l.pop(-1)

    if ':' in headers_raw_l[-1] and ':' in headers_raw_l[0]:
        print_headers_raw_to_dict(headers_raw_l)
        # print_headers_raw_to_ordered_dict(headers_raw_l)
    else:
        print_headers_raw_to_dict_space(headers_raw_l)
        # print_headers_raw_to_ordered_dict_space(headers_raw_l)

def print_url_params(url_params):
    s = str(parse_qsl(url_params.strip(), 1))
    print("OrderedDict(\n    " + "),\n    ".join(map(lambda s: s.strip(), s.split("),")))[1:-1] + ",\n)")

def print_url_params_new(url_params):
    l = parse_qsl(url_params.strip(), 1)
    print("{\n    " + "',\n    ".join(map(lambda s: "'"+s[0]+"': '"+s[1], l)) + "',\n}")

if __name__ == '__main__':
    text = '''
    Cache-Control	no-cache
Accept	*/*
X-Requested-With	XMLHttpRequest
If-Modified-Since	0
    '''

    print_dict_from_copy_headers(text)

    # url_params = 'placementNo=0004&clientType=2&billMaterialsId=58acb91cc2c147079b667674c0d7dec9'
    # print_url_params_new(url_params)
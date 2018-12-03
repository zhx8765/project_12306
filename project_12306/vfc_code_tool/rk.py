#!/usr/bin/env python
# coding:utf-8
import random

import requests
from hashlib import md5


class RClient(object):

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode()).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def create(self, im_func, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        im = im_func()
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        # {'Result': 'GMRWQ', 'Id': '8f555dc5-ab00-4759-a8be-2832f34d3603'}
        return r.json()

    def report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()

    # def get_image(self):
    #     """
    #     获取验证码：
    #     对于rk打码，用来获取验证码的字节；对于manual_dm打码函数，用来获取验证码字节的返回值
    #     :return: self.response_image
    #     """
    #     # 验证码随机地址
    #     url = 'https://kyfw.12306.cn/passport/captcha/captcha-image' \
    #           '?login_site=E&module=login&rand=sjrand&' + str(random.random())
    #     self.response_image = requests.get(url).content
    #     return self.response_image
    
    
if __name__ == '__main__':
    
    username = 'mumuloveshine'
    password = 'mumu1806'
    soft_id = '7545'
    soft_key = 'df49bdfd6416475181841e56ee1dc769'
    rc = RClient(username, password, soft_id, soft_key)
    # im = open('D:/project_12306/12306.jpg', 'rb').read()
    print(rc.create(rc.get_image, 6113))
    # return rc.create(im, 6113)
    



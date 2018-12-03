#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zqf'

from request_help_tool.request_help import make_session
from vfc_code_tool import manual_dm, rk

import urllib3
import random


# 关闭警告
urllib3.disable_warnings()


class Train12306:
    """
    12306登录
    self.answer_list：正确图片的位置列表
    """
    def __init__(self):
        self.session = make_session(debug=True)
        self.response_image = None
        self.response_login_json = {}
        self.response_check_json = {}
        
        # rk打码平台需要的参数
        rk_username = 'mumuloveshine'
        rk_password = 'mumu1806'
        soft_id = '7545'
        soft_key = 'df49bdfd6416475181841e56ee1dc769'
        
        # self.dm = rk.RClient(rk_username, rk_password, soft_id, soft_key)
        self.dm = manual_dm.Manual()
        
    def get_image(self):
        """
        获取验证码：
        对于rk打码，用来获取验证码的字节；对于manual_dm打码函数，用来获取验证码字节的返回值
        :return: self.response_image
        """
        # 验证码随机地址
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image' \
              '?login_site=E&module=login&rand=sjrand&' + str(random.random())
        self.response_image = self.session.get(url).content
        return self.response_image

    def create_captcha_answser(self):
        """
        以列表形式获取验证码值
        :return:
        """
        # 选择打码形式，rk 为付费，manual_dm 为手动打码
        
        self.vcode_json = self.dm.create(self.get_image, 6113)
        
        # 根据手动计算，得出点击图片中心得大致位置（基本准确）
        answer_list_all = [(39, 39), (106, 39), (173, 39), (240, 39), (39, 106), (106, 106), (173, 106), (240, 106)]
        # 根据打码函数返回的json格式的图片序号进行遍历，找到其对应的坐标，并加入到列表中
        answer_list = []
        submit_list = []
        for index in self.vcode_json['Result']:
            answer_list.append(answer_list_all[int(index)-1])
        for x, y in answer_list:
            # 为坐标值增加随机浮动值，更加安全
            submit_list.append(str(x+random.randint(-5, 5)))
            submit_list.append(str(y+random.randint(-5, 5)))
        print(submit_list)
        # 将列表中的坐标值以“，”进行分隔成字符串
        submit_str = ','.join(submit_list)
        return submit_str
        
    def check_image(self):
        """
        进行验证码的校验
        :return:
        """
        for _ in range(5):
            vcode_str = self.create_captcha_answser()
            result = self.vcode_json['Result']
            vcode_id = self.vcode_json['Id']
            
            url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
            headers = {
    
                'Referer': 'https://kyfw.12306.cn/otn/login/init'
            }
            # 将data中的参数进行替换
            data = {
                'answer': vcode_str,
                'login_site': 'E',
                'rand': 'sjrand'
            }
            response_check = self.session.post(url, headers=headers, data=data)
            # 查看验证码验证是否成功
            response_check_json = response_check.json()
            if response_check_json['result_code'] == '4':
                print("验证码验证成功")
                break
            else:
                print("验证码验证失败")
                self.dm.report_error(vcode_id)
        
    def web_login(self, username, password):
        """
        登录
        :param username:
        :param password:
        :return:
        """
        url = 'https://kyfw.12306.cn/passport/web/login'
        headers = {

            'Referer': 'https://kyfw.12306.cn/otn/login/init'
        }
        data = {
            'username': username,
            'password': password,
            'appid': 'otn'
        }
        
        response = self.session.post(url, headers=headers, data=data)
        self.response_login_json = response.json()
    

train12306 = Train12306()


def start_login():
    
    username = 'zhx8765'
    password = '199498zhx'
    
    # 允许连续失败5次，为了防止代码出现问题、服务器的改动及打码平台出现故障造成无效打码的资金损失
    train12306.get_image()
    # train12306.create_captcha_answser()
    train12306.check_image()
    train12306.web_login(username, password)
    

if __name__ == '__main__':
    start_login()


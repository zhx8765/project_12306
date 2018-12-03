#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zqf'
from login_12306 import *
from settings import *
from request_help_tool.get_date_12306 import get_date_time
import re
import time
from urllib import parse


class ReserveTicket:
    def __init__(self, login_12306_object):
        self.train12306 = login_12306_object

    def user_login(self):
        url = 'https://kyfw.12306.cn/otn/login/userLogin'
        data = {
            '_json_att': ''
        }
        self.train12306.session.post(url, data=data)

    def auth_uamtk(self):
        url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        }
        data = {
            'appid': 'otn'
        }
        response = self.train12306.session.post(url, headers=headers, data=data)
        print(response.json()['result_message'])
        self.auth_uamtk_response_newapptk = response.json()['newapptk']

    def uamauthclient(self):
        url = 'https://kyfw.12306.cn/otn/uamauthclient'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        }
        data = {
            'tk': f'{self.auth_uamtk_response_newapptk}'
        }
        response = self.train12306.session.post(url, headers=headers, data=data)
        print(response)

    def visit_left_ticket_init(self):
        url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.train12306.session.get(url)

    def left_ticket_queryA(self, train_date, from_station, to_station):
        self.train_date = train_date
        self.from_station = from_station
        self.to_station = to_station

        url = 'https://kyfw.12306.cn/otn/leftTicket/queryA'
        params = {
            'leftTicketDTO.train_date': train_date,
            'leftTicketDTO.from_station': STATION_DICT[from_station],
            'leftTicketDTO.to_station': STATION_DICT[to_station],
            'purpose_codes': 'ADULT'
        }
        headers = {
            'Cache-Control': 'no-cache',
            # 'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'If-Modified-Since': '0',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init'
        }
        i = 0
        while 1:
            i += 1
            response = self.train12306.session.get(url, headers=headers, params=params)
            response_json = response.json()
            status = response_json['status']
            tag = '0'
            if status:
                print("获取车次列表成功")
                train_list = response_json['data']['result']
                for index, train in enumerate(train_list):
                    self.train_split = train.split('|')
                    if self.train_split[3] == my_train:
                        self.train_split = train.split('|')
                        print('车次：', self.train_split[3], '---', '出发日期：', self.train_split[13],
                              '出发时间：', self.train_split[8], '到达时间：', self.train_split[9], '历时：', self.train_split[10])
                        if self.train_split[SEAT_TYPE_INDEX_DICT[seat_type]] != '无' and self.train_split[SEAT_TYPE_INDEX_DICT[seat_type]] != '' and self.train_split[SEAT_TYPE_INDEX_DICT[seat_type]] != '0':
                            tag = '1'
                            break
                        else:
                            tag = '2'
                            print(f"此座位目前无票,正在刷新第{i}次")
                            time.sleep(1)
                else:
                    if tag == '0':
                        print("无此列车")
                        exit()
            if tag == '1':
                break
            else:
                if tag == '0':
                    print("获取车次列表失败")
                    exit()
                    
    def submit_order_request(self):
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init'
        }
        data = {
            'secretStr': parse.unquote(self.train_split[0]),
            'train_date': self.train_date,
            'back_train_date': self.train_date,
            'tour_flag': 'dc',  # 单程
            'purpose_codes': 'ADULT',  # 普通乘客
            'query_from_station_name': self.from_station,
            'query_to_station_name': self.to_station,
            'undefined': ''
        }
        response = self.train12306.session.post(url, headers=headers, data=data)
        response_json = response.json()
        if response_json['status']:
            print('submitOrderRequest', '确认成功')
        else:
            print('submitOrderRequest', '确认失败')
            print(response_json)

    def passenger_init_dc(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
        }
        response = self.train12306.session.post(url, headers=headers)
        response_text = response.text
        self.token = re.search("globalRepeatSubmitToken = '(.*?)';", response_text).group(1)
        self.key_check_isChange = re.search("key_check_isChange':'(.*?)',", response_text).group(1)
        # print(self.token)
        # print(self.key_check_isChange)

    def get_passenger(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        }
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        response = self.train12306.session.post(url, headers=headers, data=data)
        response_json = response.json()
        if response_json['status']:
            print("常用联系人信息获取成功")
            self.passenger_msgs = response_json['data']['normal_passengers']
            # for passenger_msg in passenger_msgs:
            #     if passenger_msg['passenger_id_no'] == passenger_id:
            #         self.passenger_msg_dict = passenger_msg
            #
        else:
            print("常用联系人信息获取失败")
            print('get_passenger:', response_json)
    
    def deal_passenger_msgs(self, passenger_id):
        passenger_msg = list(filter(lambda x: x['passenger_id_no'] == passenger_id, self.passenger_msgs))[0]
        self.passengerTicketStr = f'{SEAT_TYPE_INDEX_DICT_INFO[seat_type]},{passenger_msg["passenger_flag"]},' \
                                  f'{passenger_msg["passenger_type"]},{passenger_msg["passenger_name"]},' \
                                  f'{passenger_msg["passenger_id_type_code"]},' \
                                  f'{passenger_msg["passenger_id_no"]},{passenger_msg["mobile_no"]},N'
        self.oldPassengerStr = f'{passenger_msg["passenger_name"]},{passenger_msg["passenger_id_type_code"]},' \
                               f'{passenger_msg["passenger_id_no"]},{passenger_msg["passenger_type"]}_'
    
    def check_order_info(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        }
        data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': self.passengerTicketStr,
            'oldPassengerStr': self.oldPassengerStr,
            'tour_flag': 'dc',  # 单程
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        response = self.train12306.session.post(url, headers=headers, data=data)
        response_json = response.json()
        submit_status = response_json['data']['submitStatus']
        if submit_status:
            print('checkOrderInfo  成功')
        else:
            print('checkOrderInfo 失败')
            print('check_order_info:', response_json)
            
    def get_queue_count(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        }
        data = {
            'train_date': get_date_time(train_date),
            'train_no': self.train_split[2],
            'stationTrainCode': self.train_split[3],
            'seatType': '1',
            'fromStationTelecode': self.train_split[6],
            'toStationTelecode': self.train_split[7],
            'leftTicket': self.train_split[12],
            'purpose_codes': '00',
            'train_location': self.train_split[15],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        response = self.train12306.session.post(url, headers=headers, data=data)
        response_json = response.json()
        if response_json['status']:
            print("get_queue_count:成功")
        else:
            print("get_queue_count:失败")
            print('get_queue_count:', response_json)
            
    def single_for_queue(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        }
        data = {
            'passengerTicketStr': self.passengerTicketStr,
            'oldPassengerStr': self.oldPassengerStr,
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': self.key_check_isChange,
            'leftTicketStr': self.train_split[12],
            'train_location': self.train_split[15],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        response = self.train12306.session.post(url, headers=headers, data=data)
        response_json = response.json()
        if response_json['data']['submitStatus']:
            print("single_for_queue:成功")
        else:
            print("single_for_queue:失败")
            print('single_for_queue:', response_json)

    def query_order_wait_time(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        }
        params = {
            'random': '1537237965890',
            'tourFlag': 'dc',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        response = self.train12306.session.get(url, headers=headers, params=params)
        response_json = response.json()
        if response_json['data']['queryOrderWaitTimeStatus']:
            print("queryOrderWaitTime：成功")
            self.order_id = response_json['data']['orderId']
            print(self.order_id)
        else:
            print('queryOrderWaitTime:失败')
            print(response_json)
            
    def result_order(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue'
        headers = {
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        }
        data = {
            'orderSequence_no': self.order_id,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        response = self.train12306.session.post(url, headers=headers, data=data)
        print(response.json())
        
        
if __name__ == '__main__':
    reserve_ticket = ReserveTicket(train12306)
    start_login()
    
    reserve_ticket.user_login()
    reserve_ticket.auth_uamtk()
    reserve_ticket.uamauthclient()
    reserve_ticket.user_login()
    reserve_ticket.visit_left_ticket_init()
    
    # 出发时间、始发站、到达站、座位类型、车次、身份证号
    train_date = '2018-09-30'
    from_station = '杭州'
    to_station = '合肥'
    my_train = 'K308'
    passenger_id = '230623199409081434'
    seat_type = '硬座'

    reserve_ticket.left_ticket_queryA(train_date, from_station, to_station)
    reserve_ticket.submit_order_request()
    reserve_ticket.passenger_init_dc()

    reserve_ticket.get_passenger()
    reserve_ticket.deal_passenger_msgs(passenger_id)
    reserve_ticket.check_order_info()
    reserve_ticket.get_queue_count()
    reserve_ticket.single_for_queue()
    reserve_ticket.query_order_wait_time()
    # reserve_ticket.result_order()
    



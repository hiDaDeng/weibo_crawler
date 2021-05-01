"""
Author: 大邓
Mail: thunderhit@qq.com
Created Time: 2021/4/29
"""

from pyquery import PyQuery
import datetime
import requests
import csv
import time
import re
import json




class Profile(object):
    """
    Profile类用于获取用户（userid）的个人信息，方法有

    1. get_profile(userid='1087770692')

    Weibos类默认为用户提供了一个测试cookies， 但可能会失效。如果程序无法采集数据，可能需要更换cookies； 请登录自己的微博，获取自己最新的cookies
    """
    def __init__(self, csvfile='', delay=1, cookies=''):
        self.__user_info_template = 'https://weibo.cn/{userid}/info'
        self.__REQUEST_DELAY = 0.3 + delay
        self.__HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0'}
        if cookies:
            self.__COOKIES = {'Cookie': cookies}
        else:
            self.__COOKIES = {'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=1521427420.3020706; SCF=AlvwCT3ltiVc36wsKpuvTV8uWF4V1tZ17ms9t-bZCAuiV-ZsmkYB9TEWXW7sd-gDxW34UesUalWH5lMgGsFIVAY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWYACoMUZFHDoS6U9MYf.vu5NHD95Qce0zNSo-f1hq0Ws4DqcjzdJUQUPLadJMt; SUB=_2A25NMZbHDeRhGeBN6VUX9SvEzT-IHXVu3TqPrDV6PUJbkdAKLXnikW1NRJ24IENfNQhgKlnrWsrJzXjq5AY_x0Mb; _T_WM=391c3b6aaf54f1ca5a8688cdd9cfec2c'}

        self.csvfile = csvfile
        self.csvf = open(self.csvfile, "a+", encoding='utf-8', newline='')
        self.fieldnames = ['userid', 'nickname', 'gender', 'birthday', 'province', 'city', 'introduction', 'vip_level', 'labels','authentication']
        self.writer = csv.DictWriter(self.csvf, fieldnames=self.fieldnames)
        self.writer.writeheader()
        self.csvf.close()

    def get_profile(self, userid='1087770692'):
        """
        获取用户userid的个人信息，一般最多只能获取前20页。
        :param userid:  用户的id
        :return: 字典，形如 {'nickname': '陈坤', 'gender': '男', 'province': '重庆', 'brief_introduction': '莫失己道，莫扰他心。', 'birthday': '0001-00-00', 'vip_level': '7级送Ta会员', 'authentication': '演员，代表作《龙门飞甲》《画皮》等，行走的力量发起者', 'labels': '演员'}
        """
        url = self.__user_info_template.format(userid=userid)
        resp = requests.get(url, headers=self.__HEADERS, cookies=self.__COOKIES)
        try:
            doc = PyQuery(resp.text)
        except:
            doc = PyQuery(resp.content)
        rawtextinfos = ';;'.join([item.text() for item in doc.items('div.c')])

        user_item = dict()
        nickname = re.findall('昵称;?:?(.*?)\n', rawtextinfos)
        gender = re.findall('性别;?:?(.*?)\n', rawtextinfos)
        place = re.findall('地区;?:?(.*?)\n', rawtextinfos)
        brief_introduction = re.findall('简介;?:?(.*?)\n', rawtextinfos)
        birthday = re.findall('生日;?:?(.*?)\n', rawtextinfos)
        authentication = re.findall('认证;?:?(.*?)\n', rawtextinfos)
        labels = re.findall('标签;?:?(.*?)更多>>', rawtextinfos)
        vip_level = re.findall('会员等级;?：?(.*?)\n', rawtextinfos)



        user_item["userid"] = userid
        if nickname and nickname[0]:
            user_item["nickname"] = nickname[0].replace(u"\xa0", "")
        if gender and gender[0]:
            user_item["gender"] = gender[0].replace(u"\xa0", "")
        if place and place[0]:
            place = place[0].replace(u"\xa0", "").split(" ")
            user_item["province"] = place[0]
        if len(place) > 1:
            user_item["city"] = place[1]
        if brief_introduction and brief_introduction[0]:
            user_item["introduction"] = brief_introduction[0].replace(u"\xa0", "")
        if birthday and birthday[0]:
            user_item['birthday'] = birthday[0]
        if vip_level and vip_level[0]:
            user_item["vip_level"] = vip_level[0].replace(u"\xa0", "")
        if authentication and authentication[0]:
            user_item["authentication"] = authentication[0].replace(u"\xa0", "").replace("送Ta会员", "")
        if labels and labels[0]:
            user_item["labels"] = labels[0].replace(u"\xa0", ",").replace(';', '').strip(',')
        print(user_item)

        with open(self.csvfile, "a+", encoding='utf-8', newline='') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=self.fieldnames)
            writer.writerow(user_item)

        print('采集完毕，请查看 {} 内的数据'.format(self.csvfile))





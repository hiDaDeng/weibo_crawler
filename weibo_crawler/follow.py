"""
Author: 大邓
Mail: thunderhit@qq.com
Created Time: 2021/4/29
"""

from pyquery import PyQuery
import datetime
import requests
import time
import csv
import re
import json




class Follow(object):
    """
    Follow类获取指定用户id的粉丝信息和关注信息，本类目主要用于扩展用户id数量， 有两种方法

    who_follow(self, userid='1087770692') 获取粉丝列表

    follow_who(self, userid='1087770692') 获取关注列表

    Weibos类默认delay=1，即爬虫默认每过delay发起一次访问。如果你的相提高速度，可以将delay设置为delay=0；

    Weibos类默认为用户提供了一个测试cookies， 但可能会失效。如果程序无法采集数据，可能需要更换cookies； 请登录自己的微博，获取自己最新的cookies
    """
    def __init__(self, csvfile='', delay=1, cookies=''):
        self.__fans_template = "https://weibo.cn/{userid}/fans?page={pn}"
        self.__followers_template = "https://weibo.cn/{userid}/follow?page={pn}"
        self.__REQUEST_DELAY = delay
        self.__HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0'}
        if cookies:
            self.__COOKIES = {'Cookie': cookies}
        else:
            self.__COOKIES = {'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=1521427420.3020706; SCF=AlvwCT3ltiVc36wsKpuvTV8uWF4V1tZ17ms9t-bZCAuiV-ZsmkYB9TEWXW7sd-gDxW34UesUalWH5lMgGsFIVAY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWYACoMUZFHDoS6U9MYf.vu5NHD95Qce0zNSo-f1hq0Ws4DqcjzdJUQUPLadJMt; SUB=_2A25NMZbHDeRhGeBN6VUX9SvEzT-IHXVu3TqPrDV6PUJbkdAKLXnikW1NRJ24IENfNQhgKlnrWsrJzXjq5AY_x0Mb; _T_WM=391c3b6aaf54f1ca5a8688cdd9cfec2c'}


        self.csvfile = csvfile
        self.csvf = open(self.csvfile, "a+", encoding='utf-8', newline='')
        self.fieldnames = ['uid1', 'uid2', 'crawl_time', 'relationship']
        self.writer = csv.DictWriter(self.csvf, fieldnames=self.fieldnames)
        self.writer.writeheader()
        self.csvf.close()



    def __userreq1(self, url, userid):
        """
        被self.fansd调用
        """
        resp = requests.get(url, headers=self.__HEADERS, cookies=self.__COOKIES)
        try:
            doc = PyQuery(resp.text)
        except:
            doc = PyQuery(resp.content)

        links_str = ''.join([item.attr('href') for item in doc.items("a:contains('关注')") if userid not in str(item)])
        uids = re.findall('uid=(\d+)', links_str)
        uids = [{'uid1': uid,
                 'uid2': userid,
                 'crawl_time': str(datetime.datetime.now())[:19],
                 'relationship': uid + '-follow-' + userid} for uid in uids]

        with open(self.csvfile, "a+", encoding='utf-8', newline='') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=self.fieldnames)
            for uid in uids:
                writer.writerow(uid)
                print(uid)
        return resp


    def who_follow(self, userid='1087770692'):
        """
        获取用户userid的粉丝信息，一般最多只能获取前20页。
        :param userid:  用户的id
        :return: 列表，列表中每个元素均为字典，形如 {'uid1': '6991312112', 'uid2': '1087770692', 'relationship': '6991312112-follow-1087770692'}
        """
        url = self.__fans_template.format(userid=userid, pn=1)
        resp = self.__userreq1(url=url, userid=userid)
        max_page_num = re.search(r'/>&nbsp;1/(\d+)页</div>', resp.text)
        max_page_num = int(max_page_num.group(1))
        for pn in range(2, max_page_num + 1):
            try:
                purl = self.__fans_template.format(userid=userid, pn=pn)
                self.__userreq1(purl, userid=userid)
                time.sleep(self.__REQUEST_DELAY)
            except:
                pass

        print('采集完毕，请查看 {} 内的数据'.format(self.csvfile))












    def __userreq2(self, url, userid):
        """
        被self.followers调用
        """
        resp = requests.get(url, headers=self.__HEADERS, cookies=self.__COOKIES)
        try:
            doc = PyQuery(resp.text)
        except:
            doc = PyQuery(resp.content)
        links_str = ''.join([item.attr('href') for item in doc.items("a:contains('关注')") if userid not in str(item)])
        uids = re.findall('uid=(\d+)', links_str)
        uids = [{'uid1': userid,
                 'uid2': uid,
                 'crawl_time': str(datetime.datetime.now())[:19],
                 'relationship': uid + '-follow-' + userid} for uid in uids]




        with open(self.csvfile, "a+", encoding='utf-8', newline='') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=self.fieldnames)
            for uid in uids:
                writer.writerow(uid)
                print(uid)
        return resp, uids

    def follow_who(self, userid='1087770692'):
        """
        获取用户userid的关注的好友信息，一般最多只能获取前20页。
        :param userid:  用户的id
        :return: 列表，列表中每个元素均为字典，形如 {'uid1': '6991312112', 'uid2': '1087770692', 'relationship': '6991312112-follow-1087770692'}
        """

        url = self.__followers_template.format(userid=userid, pn=1)
        resp, uids = self.__userreq2(url=url, userid=userid)
        max_page_num = re.search(r'/>&nbsp;1/(\d+)页</div>', resp.text)
        max_page_num = int(max_page_num.group(1))
        for pn in range(2, max_page_num + 1):
            try:
                purl = self.__followers_template.format(userid=userid, pn=pn)
                _, puids = self.__userreq2(purl, userid=userid)
                time.sleep(self.__REQUEST_DELAY)
            except:
                pass
        print('采集完毕，请查看 {} 内的数据'.format(self.csvfile))





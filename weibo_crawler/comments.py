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



class Comments(object):
    """
    Comments类用于获取某条微博（某weibo_id）内的评论和转发信息

    1. comments(weibo_id='IDl56i8av')

    Weibos类默认delay=1，即爬虫默认每过delay发起一次访问。如果你的相提高速度，可以将delay设置为delay=0；

    Weibos类默认为用户提供了一个测试cookies， 但可能会失效。如果程序无法采集数据，可能需要更换cookies； 请登录自己的微博，获取自己最新的cookies
    """
    def __init__(self, csvfile='', delay=1, cookies=''):
        self.__comment_template = "https://weibo.cn/comment/hot/{weibo_id}?rl=1&page={pn}"
        self.__report_template = 'https://weibo.cn/repost/{weibo_id}?page={pn}'

        self.__REQUEST_DELAY = delay
        self.__HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0'}
        if cookies:
            self.__COOKIES = {'Cookie': cookies}
        else:
            self.__COOKIES = {'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=1521427420.3020706; SCF=AlvwCT3ltiVc36wsKpuvTV8uWF4V1tZ17ms9t-bZCAuiV-ZsmkYB9TEWXW7sd-gDxW34UesUalWH5lMgGsFIVAY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWYACoMUZFHDoS6U9MYf.vu5NHD95Qce0zNSo-f1hq0Ws4DqcjzdJUQUPLadJMt; SUB=_2A25NMZbHDeRhGeBN6VUX9SvEzT-IHXVu3TqPrDV6PUJbkdAKLXnikW1NRJ24IENfNQhgKlnrWsrJzXjq5AY_x0Mb; _T_WM=391c3b6aaf54f1ca5a8688cdd9cfec2c'}

        self.csvfile = csvfile
        self.csvf = open(self.csvfile, "a+", encoding='utf-8', newline='')
        self.fieldnames = ['weibo_id', 'content', 'comment_uid', 'create_time', 'like_num', 'craw_time']
        self.writer = csv.DictWriter(self.csvf, fieldnames=self.fieldnames)
        self.writer.writeheader()
        self.csvf.close()

    def __weiboreq(self, url, weibo_id):
        """
        被self.comments
        """
        resp = requests.get(url, headers=self.__HEADERS, cookies=self.__COOKIES)
        try:
            doc = PyQuery(resp.text)
        except:
            doc = PyQuery(resp.content)
        comment_blocks = [block for block in doc.items("div.c") if 'C_' in str(block)]
        comments = []
        for comment_block in comment_blocks:
            comment = dict()
            try:
                comment['weibo_id'] = weibo_id
                comment['comment_uid'] = comment_block('a').attr('href').replace('/u/', '').replace('/', '')
                comment['create_time'] = comment_block('.ct').text().split('\xa0')[0]
                comment['content'] = comment_block('.ctt').text()
                comment['craw_time'] = str(datetime.datetime.now())[:19]
                comment['like_num'] = re.findall('\d+', comment_block('a').eq(2).text())[0]
            except:
                comment['weibo_id'] = weibo_id
                comment['comment_uid'] = comment_block('a').attr('href').replace('/u/', '').replace('/', '')
                comment['create_time'] = comment_block('.ct').text().split('\xa0')[0]
                comment['content'] = comment_block('.ctt').text()
                comment['craw_time'] = str(datetime.datetime.now())[:19]
                comment['like_num'] = 0
            comments.append(comment)

        with open(self.csvfile, "a+", encoding='utf-8', newline='') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=self.fieldnames)
            for com in comments:
                writer.writerow(com)
                print(com)

        return resp


    def comments(self, weibo_id='IDl56i8av'):
        """
        获取某条微博(weibo_id) 对应的评论数据
        :param weibo_id: 微博id
        :return: 列表； 列表内元素形如{'weibo_id': 'IDl56i8av', 'comment_uid': '7360957592', 'zan': '2', 'create_time': '2020-04-14 23:46:04', 'content': '关门大吉🧨，永远不见', 'craw_time': '2021-04-28 18:37:04'}
        """
        url = self.__comment_template.format(weibo_id=weibo_id, pn=1)
        resp = self.__weiboreq(url=url, weibo_id=weibo_id)

        max_page_num = re.search(r'/>&nbsp;1/(\d+)页</div>', resp.text)
        max_page_num = int(max_page_num.group(1))
        max_page_num = max_page_num if max_page_num <= 50 else 50
        for pn in range(2, max_page_num + 1):
            try:
                purl = self.__comment_template.format(weibo_id=weibo_id, pn=pn)
                self.__weiboreq(purl, weibo_id=weibo_id)
                time.sleep(self.__REQUEST_DELAY)
            except:
                pass

        print('采集完毕，请查看 {} 内的数据'.format(self.csvfile))














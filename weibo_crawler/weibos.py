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




class Weibos(object):
    """
    Weibos类用于获取某关键词(某微博用户)一定日期范围的微博信息，有三种方法

    1. get_weibos_by_userid(userid='1087770692')

    2. get_weibos_by_userid_and_date(userid='1087770692', startdate='2020-01-01', enddate='2020-12-31')

    3. get_weibos_by_topic_and_date(topic='python', startdate='2020-01-01', enddate='2020-12-31')

    Weibos类默认delay=1，即爬虫默认每过delay发起一次访问。如果你的相提高速度，可以将delay设置为delay=0；

    Weibos类默认为用户提供了一个测试cookies， 但可能会失效。如果程序无法采集数据，可能需要更换cookies； 请登录自己的微博，获取自己最新的cookies
    """
    def __init__(self, csvfile, delay=1, cookies=''):
        self.__by_userid_template = 'https://weibo.cn/{userid}/profile?page={pn}'
        self.__by_userid_and_date_template = "https://weibo.cn/{userid}/profile?hasori=0&haspic=0&starttime={start}&endtime={end}&advancedfilter=1&page={pn}"
        self.__by_topic_and_date = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={topic}&starttime={start}&endtime={end}&atten=1&sort=time&page={pn}"

        self.__REQUEST_DELAY = delay
        self.__HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0'}
        if cookies:
            self.__COOKIES = {'Cookie': cookies}
        else:
            self.__COOKIES = {'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=1521427420.3020706; SCF=AlvwCT3ltiVc36wsKpuvTV8uWF4V1tZ17ms9t-bZCAuiV-ZsmkYB9TEWXW7sd-gDxW34UesUalWH5lMgGsFIVAY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWYACoMUZFHDoS6U9MYf.vu5NHD95Qce0zNSo-f1hq0Ws4DqcjzdJUQUPLadJMt; SUB=_2A25NMZbHDeRhGeBN6VUX9SvEzT-IHXVu3TqPrDV6PUJbkdAKLXnikW1NRJ24IENfNQhgKlnrWsrJzXjq5AY_x0Mb; _T_WM=391c3b6aaf54f1ca5a8688cdd9cfec2c'}


        self.csvfile = csvfile
        self.csvf = open(self.csvfile, "a+", encoding='utf-8', newline='')
        self.fieldnames = ['uid', 'weibo_id', 'orinin_link', 'product', 'ratescore',
                      'content', 'like_num', 'repost_num', 'comment_num',
                      'create_time', 'crawl_time', 'device', 'img', 'raw_img', 'video_link', 'location']
        self.writer = csv.DictWriter(self.csvf, fieldnames=self.fieldnames)
        self.writer.writeheader()
        self.csvf.close()

    def __req_weibos(self, url, userid):
        resp = requests.get(url, headers=self.__HEADERS, cookies=self.__COOKIES)
        try:
            doc = PyQuery(resp.text)
        except:
            doc = PyQuery(resp.content)
        datas = []
        items = list(doc.items('body div.c'))[1:-2]
        for item in items:
            data = dict()
            raw = item.text()
            content = ''.join(item.text().split('\n')[:-1])

            like_num = re.findall('赞\[(\d+)\]', raw)
            if like_num and len(like_num) >= 1:
                like_num = like_num[-1]


            try:
                raw_repost = str(item("a:contains('转发')"))
                repost_num = re.findall('转发\[(\d+)\]', raw_repost)[0]
                weibo_id, uid = re.findall("https://weibo.cn/repost/(.*?)\?uid=(\d+)", raw_repost)[0]

            except:
                repost_num = 0
                weibo_id = ''
                uid = ''


            comment_num = re.findall('评论\[(\d+)\]', raw)
            if comment_num and len(comment_num) >= 1:
                comment_num = comment_num[-1]

            create_time = item('.ct').eq(-1).text()
            crawl_time = str(datetime.datetime.now())[:19]

            try:
                device = item('.ct:contains("来自")').text().split('来自')[-1]
            except:
                device = ''

            try:
                img = item('img').attr('src')
            except:
                img = ''

            try:
                img_id = img.split('/')[-1][:-4]
                repost_id = item.attr('id').replace('M_', '')
                raw_img = 'https://weibo.cn/mblog/oripic?id={repost_id}&u={img_id}'.format(img_id=img_id,
                                                                                           repost_id=repost_id)
            except:
                raw_img = ''

            try:
                mapp = item("a:contains('显示地图')").attr('href')
                location = re.findall('xy=(.*?)&', mapp)[0]
            except:
                mapp = ''
                location = ''

            try:
                video_link = item("a:contains('微博视频')").attr('href')

            except:
                video_link = ''

            try:
                orinin_link = item("a:contains('原文评论')").attr('href')
            except:
                orinin_link = ''

            try:
                product = item('.ctt:contains("我的评分") a').text()
                ratescore = len(re.findall('\[星星\]', str(item)))
            except:
                product = ''
                ratescore = 0


            data['uid'] = uid
            data['weibo_id'] = weibo_id
            data['product'] = product  #商品服务
            data['ratescore'] = ratescore #评分
            data['content'] = content #微博内容
            data['like_num'] = like_num #点赞数
            data['repost_num'] = repost_num  #转发数
            data['comment_num'] = comment_num #评论数
            data['create_time'] = create_time #创建时间
            data['crawl_time'] = crawl_time #爬取时间
            data['device'] = device  #设备
            data['img'] = img  #图片链接
            data['raw_img'] = raw_img #原始图片
            data['location'] = location  #坐标
            data['video_link'] = video_link  #视频链接
            data['orinin_link'] = orinin_link #原文全文链接

            with open(self.csvfile, "a+", encoding='utf-8', newline='') as csvf:
                writer = csv.DictWriter(csvf, fieldnames=self.fieldnames)
                writer.writerow(data)
            datas.append(data)
            print(data)
            print()
        return resp





    def get_weibos_by_userid(self, userid='1087770692'):
        """
        通过用户id获取 该用户发布的微博信息
        :param userid:  微博用户
        :return:  列表，该用户的很多个微博记录； 列表中的元素为字典信息
        """
        url = self.__by_userid_template.format(userid=userid, pn=1)
        resp = self.__req_weibos(url=url, userid=userid)
        max_page_num = re.search(r'/>&nbsp;1/(\d+)页</div>', resp.text)
        if max_page_num:
            max_page_num = int(max_page_num.group(1))
            for pn in range(2, max_page_num + 1):
                purl = self.__by_userid_template.format(userid=userid, pn=pn)
                self.__req_weibos(url=purl, userid=userid)
                time.sleep(self.__REQUEST_DELAY)

        print('采集完毕，请查看 {} 内的数据'.format(self.csvfile))










    def get_weibos_by_userid_and_date(self, userid='1087770692', startdate='2020-01-01', enddate='2020-12-31'):
        """
        通过用户id和日期获取指定日期范围内该用户的发布的微博信息
        :param userid: 用户id
        :param startdate:  起始日期，形如"2020-01-01"
        :param enddate:  结束日期，形如"2020-12-31"
        :return: 列表，该用户的很多个微博记录； 列表中的元素为字典信息
        """
        start_date = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        time_spread = datetime.timedelta(days=20)

        purls = []
        while start_date < end_date:
            start_date_string = start_date.strftime("%Y%m%d")
            tmp_end_date = start_date + time_spread
            if tmp_end_date >= end_date:
                tmp_end_date = end_date
            end_date_string = tmp_end_date.strftime("%Y%m%d")

            url = self.__by_userid_and_date_template.format(userid=userid, start=start_date_string, end=end_date_string, pn=1)
            resp = self.__req_weibos(url=url, userid=userid)
            max_page_num = re.search(r'/>&nbsp;1/(\d+)页</div>', resp.text)

            if max_page_num:
                max_page_num = int(max_page_num.group(1))
                for pn in range(2, max_page_num + 1):
                    purl = self.__by_userid_and_date_template.format(userid=userid, start=start_date_string, end=end_date_string, pn=pn)
                    purls.append(purl)

            start_date = start_date + time_spread

        for purl in purls:
            self.__req_weibos(url=purl, userid=userid)
        print('采集完毕，请查看 {} 内的数据'.format(self.csvfile))


    def get_weibos_by_topic_and_date(self, topic='python', startdate='2020-01-01', enddate='2020-12-31'):
        """
        通过关键词和日期获取指定日期范围内该关键词的微博信息（微博搜索高级搜索结果）
        :param topic:  topic关键词
        :param startdate: 起始日期，形如"2020-01-01"
        :param enddate: 结束日期，形如"2020-12-31"
        :return:  列表，该用户的很多个微博记录； 列表中的元素为字典信息
        """

        start_date = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        time_spread = datetime.timedelta(days=1)

        purls = []
        while start_date <= end_date:
            day_string = start_date.strftime("%Y%m%d")
            url = self.__by_topic_and_date.format(topic=topic, start=day_string, end=day_string, pn=1)
            resp = self.__req_weibos(url=url, userid='')
            max_page_num = re.search(r'/>&nbsp;1/(\d+)页</div>', resp.text)

            if max_page_num:
                max_page_num = int(max_page_num.group(1))
                for pn in range(2, max_page_num + 1):
                    purl = self.__by_topic_and_date.format(topic=topic, userid='', start=day_string, end=day_string, pn=pn)
                    purls.append(purl)

            start_date = start_date + time_spread

        for purl in purls:
            self.__req_weibos(url=purl, userid='')
        print('采集完毕，请查看 {} 内的数据'.format(self.csvfile))








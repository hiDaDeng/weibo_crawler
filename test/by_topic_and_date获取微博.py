from weibo_crawler.weibos import Weibos
import os

#获取python话题微博数据
cookies = ''


csvfile = os.getcwd()+'/data/python.csv'
WB = Weibos(csvfile=csvfile,
            delay=1,
            cookies=cookies)
WB.get_weibos_by_topic_and_date(topic='python',
                                startdate='2020-01-01',
                                enddate='2020-12-31')
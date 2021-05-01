from weibo_crawler.weibos import Weibos
import os

#获取指定日期范围内的话题数据
#如果程序失败，需要传入你的微博cookies
cookies = ''
# csv文件路径
csvfile = os.getcwd()+'/data/by_userid_and_date1087770692.csv'
WB = Weibos(csvfile=csvfile,
            delay=1,
            cookies=cookies)
# 某用户指定日期的微博数据
WB.get_weibos_by_userid_and_date(userid='1087770692',
                                 startdate='2020-01-01',
                                 enddate='2020-12-31')
from weibo_crawler.weibos import Weibos
import os

#如果程序失败，需要传入你的微博cookies
cookies = ''

# csv文件路径
csvfile = os.getcwd()+'/data/1087770692date.csv'

WB = Weibos(csvfile=csvfile,
            delay=1,
            cookies=cookies)

# 某用户指定日期的微博数据
WB.get_weibos_by_userid(userid='1087770692')
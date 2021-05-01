from weibo_crawler import Profile
import os

#如果程序失败，需要传入你的微博cookies
cookies = ''

# csv文件路径
csvfile = os.getcwd()+'/data/简介.csv'
prof = Profile(csvfile=csvfile,
                delay=1,
                cookies=cookies)

prof.get_profile(userid='1087770692') #陈坤微博的id
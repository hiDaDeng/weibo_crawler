from weibo_crawler import Follow
import os

#如果程序失败，需要传入你的微博cookies
cookies = ''

# csv文件路径
csvfile = os.getcwd()+'/data/1087770692fans.csv'
follow = Follow(csvfile=csvfile,
                delay=1,
                cookies=cookies)

#哪些微博用户关注了陈坤
follow.who_follow(userid='1087770692')
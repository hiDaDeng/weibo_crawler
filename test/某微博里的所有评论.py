from weibo_crawler import Comments
import os

#采集某条微博下所有评论
cookies = ''
# csv文件路径
csvfile = os.getcwd()+'/data/comments.csv'
coms = Comments(csvfile=csvfile,
                delay=1,
                cookies=cookies)
# weibo_id='IDl56i8av')
coms.comments(weibo_id='IDl56i8av')
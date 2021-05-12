# 一、简介

weibo_crawler参考[【nghuyong/WeiboSpider】](https://github.com/nghuyong/WeiboSpider) 对代码用法进行了简化，可以做轻度的微博数据采集。



### 1. 1 支持爬虫

- 用户信息抓取
- 用户微博抓取(全量/指定时间段)
- 用户社交关系抓取(粉丝/关注)
- 微博评论抓取
- 基于关键词和时间段(粒度到小时)的微博抓取
- 微博转发抓取



<br>



# 二、安装

```
pip3 install weibo_crawler
```

<br>

# 三、快速上手

weibo_crawler库的使用方法

```
from weibo_crawler import Profile, Follow, Weibos, Comments
```



注意：微博分PC微博和手机微博，两者的数据其实是一样的，虽然手机微博在浏览器中页面看起来很丑，但手机微博更容易采集， 本教程是对**微博手机端**设计的爬虫，手机端微博链接  https://weibo.cn/ 

### 3.1 个人简介

获取某用户个人简介

```python
from weibo_crawler import Profile
import os

#如果程序失败，需要传入你的微博cookies
cookies = ''

# csv文件路径
csvfile = os.getcwd()+'/简介.csv'
prof = Profile(csvfile=csvfile, 
                delay=1, 
                cookies=cookies)

prof.get_profile(userid='1087770692') #陈坤微博的id
```

Run

```
{'nickname': '陈坤', 
'gender': '男', 
'province': '重庆', 
'brief_introduction': '莫失己道，莫扰他心。', 
'birthday': '0001-00-00', 
'vip_level': '7级送Ta会员', 
'authentication': '演员，代表作《龙门飞甲》《画皮》等，行走的力量发起者', 'labels': '演员'}

```

**用户id获取方式**

打开手机微博https://weibo.cn 找到感兴趣的用户的个人页面（以我的个人微博为例）

![](img/userid.png)

### 3.2 获取粉丝/关注列表

哪些微博用户关注了陈坤

```python
from weibo_crawler import Follow
import os

#如果程序失败，需要传入你的微博cookies
cookies = ''

# csv文件路径
csvfile = os.getcwd()+'/fans.csv'
follow = Follow(csvfile=csvfile, 
                delay=1, 
                cookies=cookies)

#哪些微博用户关注了陈坤
follow.who_follow(userid='1087770692')
```

Run

```
{'uid1': '1879804794', 'uid2': '1087770692', 'crawl_time': '2021-04-30 18:24:40', 'relationship': '1879804794-follow-1087770692'}
{'uid1': '6371190854', 'uid2': '1087770692', 'crawl_time': '2021-04-30 18:24:40', 'relationship': '6371190854-follow-1087770692'}
{'uid1': '7602005193', 'uid2': '1087770692', 'crawl_time': '2021-04-30 18:24:40', 'relationship': '7602005193-follow-1087770692'}
{'uid1': '3227075870', 'uid2': '1087770692', 'crawl_time': '2021-04-30 18:24:40', 'relationship': '3227075870-follow-1087770692'}
```



陈坤关注了哪些微博用账号

```python
#如果程序失败，需要传入你的微博cookies
cookies = ''

# csv文件路径
csvfile = os.getcwd()+'/chenkun_follow_who.csv'
follow = Follow(csvfile=csvfile, 
                delay=1, 
                cookies=cookies)

#哪些微博用户关注了陈坤
follow.follow_who(userid='1087770692')
```

Run

```
{'uid1': '1087770692', 'uid2': '7451895315', 'crawl_time': '2021-04-30 18:25:30', 'relationship': '7451895315-follow-1087770692'}
{'uid1': '1087770692', 'uid2': '1715351501', 'crawl_time': '2021-04-30 18:25:30', 'relationship': '1715351501-follow-1087770692'}
{'uid1': '1087770692', 'uid2': '1278932711', 'crawl_time': '2021-04-30 18:25:30', 'relationship': '1278932711-follow-1087770692'}
{'uid1': '1087770692', 'uid2': '1299491507', 'crawl_time': '2021-04-30 18:25:30', 'relationship': '1299491507-follow-1087770692'}

```



### 3.3 某微博下的评论

获取某条微博weibo_id里的评论信息

```python
from weibo_crawler import Comments
import os

#如果程序失败，需要传入你的微博cookies
cookies = ''

# csv文件路径
csvfile = os.getcwd()+'/comments.csv'
coms = Comments(csvfile=csvfile, 
                delay=1, 
                cookies=cookies)

# weibo_id='IDl56i8av')
coms.comments(weibo_id='IDl56i8av')
```

Run

```
{'weibo_id': 'IDl56i8av', 'comment_uid': '2249872265', 'like_num': '82', 'create_time': '2020-04-14 23:44:51', 'content': '明天，你好！雷神山关门大吉', 'craw_time': '2021-04-30 18:33:13'}
{'weibo_id': 'IDl56i8av', 'comment_uid': '5458366215', 'like_num': '49', 'create_time': '2020-04-14 23:42:37', 'content': '晚安💤疫情快点好起来吧', 'craw_time': '2021-04-30 18:33:13'}
{'weibo_id': 'IDl56i8av', 'comment_uid': '6577817093', 'like_num': '29', 'create_time': '2020-04-14 23:42:32', 'content': '跪求大家救救我们一家！', 'craw_time': '2021-04-30 18:33:13'}

```

**微博id的获取方式**

打开手机微博https://weibo.cn  以我的个人微博为例，点击该用户的微博历史记录，使用浏览器开发者工具可以获取某微博的weiboID

![](img/微博id.png)

<br>

### 3.4 获取多微博

- get_weibos_by_userid(userid='1087770692')

- get_weibos_by_userid_and_date(userid='1087770692', startdate='2020-01-01', enddate='2020-12-31')

- get_weibos_by_topic_and_date(topic='python', startdate='2020-01-01', enddate='2020-12-31')



#### 3.4.1 get_weibos_by_userid

获取某指定用户的所有微博数据

```python
from weibo_crawler.weibos import Weibos
import os

#如果程序失败，需要传入你的微博cookies
cookies = ''

# csv文件路径
csvfile = os.getcwd()+'/1087770692.csv'
WB = Weibos(csvfile=csvfile, 
            delay=1, 
            cookies=cookies)

# userid='1087770692'
WB.get_weibos_by_userid(userid='1087770692')

```

Run

```
{'uid': '1087770692', 'weibo_id': 'Kdiasmwfx', 'product': '', 'ratescore': 0, 'content': 'A组转B组，之后转回A。', 'like_num': '10820', 'repost_num': '8115', 'comment_num': '8665', 'create_time': '今天 13:57', 'crawl_time': '2021-04-30 18:37:53', 'device': '', 'img': None, 'raw_img': '', 'location': '', 'video_link': None, 'orinin_link': None}

{'uid': '1087770692', 'weibo_id': 'KcZQbvplr', 'product': '', 'ratescore': 0, 'content': '转发了\xa0山下学堂\xa0的微博:#表演与行为艺术##山下学堂# 2020新人班“美术馆计划”的两日，学员们来到@红砖美术馆 ，共同参观“詹姆斯·李·拜尔斯：#完美时刻# ”展览，并与红砖美术馆携手再现这位传奇艺术家的三件参与式行为表演作品。红砖美术馆高级策展人 Jonas Stampe 为每个作品指导。“缓慢、放松，你们这样很美。”他鼓励...全文\xa0[组图共18张]原图\xa0赞[218]\xa0原文转发[7107]\xa0原文评论[44]转发理由:转发微博', 'like_num': '8266', 'repost_num': '7082', 'comment_num': '7549', 'create_time': '04月28日 15:18', 'crawl_time': '2021-04-30 18:37:53', 'device': '', 'img': 'https://h5.sinaimg.cn/upload/2016/05/26/319/5337.gif', 'raw_img': 'https://weibo.cn/mblog/oripic?id=KcZQbvplr&u=5337', 'location': '', 'video_link': None, 'orinin_link': 'https://weibo.cn/comment/KcZpdwdlK?rl=1#cmtfrm'}

{'uid': '1087770692', 'weibo_id': 'KcQkm0cFm', 'product': '', 'ratescore': 0, 'content': '突然发现，一累了就找吃的视频看。完全下意识的，已经好一段时间了。', 'like_num': '21261', 'repost_num': '7766', 'comment_num': '11419', 'create_time': '04月27日 15:05', 'crawl_time': '2021-04-30 18:37:53', 'device': '', 'img': '//h5.sinaimg.cn/m/emoticon/icon/default/d_wabishi-816c4e8890.png', 'raw_img': 'https://weibo.cn/mblog/oripic?id=KcQkm0cFm&u=d_wabishi-816c4e8890', 'location': '', 'video_link': None, 'orinin_link': None}

```



#### 3.4.2 get_weibos_by_userid_and_date

获取某指定用户指定日期范围内的微博数据

```python
from weibo_crawler.weibos import Weibos
import os

#如果程序失败，需要传入你的微博cookies
cookies = ''

# csv文件路径
csvfile = os.getcwd()+'/1087770692date.csv'

WB = Weibos(csvfile=csvfile, 
            delay=1, 
            cookies=cookies)

# 某用户指定日期的微博数据
WB.get_weibos_by_userid_and_date(userid='1087770692', 
                                 startdate='2020-01-01', 
                                 enddate='2020-12-31')
```

Run

```
{'uid': '1087770692', 'weibo_id': 'Iquq5giZd', 'product': '', 'ratescore': 0, 'content': '分享图片 \xa0[组图共2张]原图', 'like_num': '37582', 'repost_num': '7136', 'comment_num': '7772', 'create_time': '2020-01-21 11:34:45\xa0来自绿洲APP', 'crawl_time': '2021-04-30 18:40:43', 'device': '绿洲APP', 'img': 'http://wx4.sinaimg.cn/wap180/40d61044gy1gb41ple6h0j20yi1azb29.jpg', 'raw_img': 'https://weibo.cn/mblog/oripic?id=Iquq5giZd&u=40d61044gy1gb41ple6h0j20yi1azb29', 'location': '', 'video_link': None, 'orinin_link': None}

{'uid': '1087770692', 'weibo_id': 'IqdeJlfr9', 'product': '', 'ratescore': 0, 'content': '过节几天要练练钢笔字了', 'like_num': '25958', 'repost_num': '5462', 'comment_num': '6298', 'create_time': '2020-01-19 15:50:05', 'crawl_time': '2021-04-30 18:40:43', 'device': '', 'img': None, 'raw_img': '', 'location': '', 'video_link': None, 'orinin_link': None}

{'uid': '1087770692', 'weibo_id': 'IphT4lwlZ', 'product': '', 'ratescore': 0, 'content': '生活是自己的不仅仅存在于别人的谈论中过好自己的随喜别人的', 'like_num': '44829', 'repost_num': '7008', 'comment_num': '6711', 'create_time': '2020-01-13 13:50:09', 'crawl_time': '2021-04-30 18:40:43', 'device': '', 'img': None, 'raw_img': '', 'location': '', 'video_link': None, 'orinin_link': None}

```



#### 3.4.3 get_weibos_by_topic_and_date

获取指定话题、指定日期范围的微博

```python
from weibo_crawler.weibos import Weibos
import os

#如果程序失败，需要传入你的微博cookies
cookies = ''

# csv文件路径
csvfile = os.getcwd()+'/1087770692date.csv'

WB = Weibos(csvfile=csvfile, 
            delay=1, 
            cookies=cookies)

# 某指定话题日期范围内的微博数据
WB.get_weibos_by_topic_and_date(topic='python', 
                                startdate='2020-01-01', 
                                enddate='2020-12-31')
```

Run

```
{'uid': '6438471311', 'weibo_id': 'InwK8nQZT', 'product': '', 'ratescore': 0, 'content': '虾尾拌面要去壳:明后两天本学畜将渡劫批判性思维python品牌传播轮番轰炸希望我可以苟下来', 'like_num': '0', 'repost_num': '0', 'comment_num': '0', 'create_time': '2020-01-01 23:58:44\xa0来自逢考必过的人', 'crawl_time': '2021-04-30 18:43:25', 'device': '逢考必过的人', 'img': 'https://h5.sinaimg.cn/upload/2016/05/26/319/5338.gif', 'raw_img': 'https://weibo.cn/mblog/oripic?id=InwK8nQZT&u=5338', 'location': '', 'video_link': None, 'orinin_link': None}

{'uid': '6023446153', 'weibo_id': 'InwJreRSg', 'product': '', 'ratescore': 0, 'content': '小小书染:2020年第一天就献给了Python真好！原图', 'like_num': '2', 'repost_num': '0', 'comment_num': '2', 'create_time': '2020-01-01 23:57:01\xa0来自nova4自拍极点全面屏', 'crawl_time': '2021-04-30 18:43:25', 'device': 'nova4自拍极点全面屏', 'img': '//h5.sinaimg.cn/m/emoticon/icon/default/d_hehe-0be7e6251f.png', 'raw_img': 'https://weibo.cn/mblog/oripic?id=InwJreRSg&u=d_hehe-0be7e6251f', 'location': '', 'video_link': None, 'orinin_link': None}

{'uid': '5815948537', 'weibo_id': 'InwHm8QV3', 'product': '', 'ratescore': 0, 'content': '坐中偶书:明天开始学Python原图', 'like_num': '0', 'repost_num': '0', 'comment_num': '0', 'create_time': '2020-01-01 23:51:53\xa0来自nova4自拍极点全面屏', 'crawl_time': '2021-04-30 18:43:25', 'device': 'nova4自拍极点全面屏', 'img': 'https://h5.sinaimg.cn/upload/2016/05/26/319/donate_btn_s.png', 'raw_img': 'https://weibo.cn/mblog/oripic?id=InwHm8QV3&u=donate_btn_s', 'location': '', 'video_link': None, 'orinin_link': None}

```



# 四、cookies

Weibo_crawler内置了一个cookies值，一般情况下cookies设置为空字符串即可； 

如果程序跑不出来结果，报错，需要传入自己的微博cookies。



点击手机weibo  https://weibo.cn  ， 登入账号密码后

1. 打开浏览器开发者工具Network面板
2. 刷新页面，找到含有weibo的任意网址，获取cookies

![](img/cookies.jpg)


<br>


## 如果

如果您是经管人文社科专业背景，编程小白，面临海量文本数据采集和处理分析艰巨任务，个人建议学习[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)视频课。作为文科生，一样也是从两眼一抹黑开始，这门课程是用五年时间凝缩出来的。自认为讲的很通俗易懂o(*￣︶￣*)o，

- python入门
- 网络爬虫
- 数据读取
- 文本分析入门
- 机器学习与文本分析
- 文本分析在经管研究中的应用

感兴趣的童鞋不妨 戳一下[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)进来看看~

![[](img/课程.png)](https://ke.qq.com/course/482241?tuin=163164df)
<br>

## 更多

- [B站:大邓和他的python](https://space.bilibili.com/122592901/channel/detail?cid=66008)

- 公众号：大邓和他的python

- [知乎专栏：数据科学家](https://zhuanlan.zhihu.com/dadeng)


![](img/公众号.png)

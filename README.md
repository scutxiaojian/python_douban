# python_douban
# 目标

获得自己可能喜欢的电影的信息。

给定初始豆瓣页面(默认为《美国队长3》)url，然后提取该电影的名称，评分，导演，编剧，主演，类型，制片国家/地区，上映日期，剧情简介，热评和豆瓣推荐电影的url。只要url管理器中的未爬取url集合不为空或者未到达指定爬取的次数，就一直爬取网页的信息以及新的url。

# 使用Python3.5.1 编写，需要的Python模块：
urllib, 高级Web交流模块，根据支持的协议下载数据<br>
beautifulsoup, 处理HTML/XML<br>
re, 提供正则表达式相关操作<br>
xlwt, 提供Excel相关的操作<br>

# 文件

douban_spider_main.py, 爬虫引擎，进行各项任务的调度<br>
douban_url_manager.py, url管理器，管理已爬取和未爬取的url，提供添加url，获取url，查询是否还有未爬取的url等功能<br>
douban_downloader.py, html下载器<br>
douban_parser.py, html分析器，提取html中的数据和url<br>
douban_outputer.py, html输出器，将提取的信息以一种较为友好的html,txt,xls形式保存

from bs4 import BeautifulSoup
import re, douban_downloader

class HtmlParser(object):
    def __init__(self):
        self.downloader = douban_downloader.HtmlDownloader() #html网页下载器
        
    def _get_new_urls(self, soup):
        new_urls = set()
        #同样喜欢区域：<div class="recommendations-bd">
        recommend = soup.find('div', class_='recommendations-bd')
        # <a href="https://movie.douban.com/subject/1866473/?from=subject-page" class="" >蚁人</a>
        links = recommend.find_all('a', href=re.compile(r"https://movie\.douban\.com/subject/\d+/"))
        for link in links:
            new_url = link['href']
            new_urls.add(new_url)
        return new_urls
    
    def _get_hot_review(self, soup):
        try: #没有热评，返回空
            firstReview = soup.find('div', class_='review-hd').find('h3').find('a').find_next_sibling('a')
            url = firstReview['href']
        except:
            return None 
        try: #页面错误，返回空
            html_cont = self.downloader.download(url)
            soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
            hotReview = soup.find('div', property='v:description') #包含了一定html的格式，只需修改一小部分即可直接显示
            hotReviewFormatted = str(hotReview)
            return hotReviewFormatted
        except:
            return None
        
    def _get_new_data(self, page_url, soup):
        res_data = {}
        try: #舍弃页面信息不完全的url
            #url
            res_data['url'] = page_url
            #<span property="v:itemreviewed">美国队长3 Captain America: Civil War</span>
            res_data['movieName'] = soup.find('span', property='v:itemreviewed').get_text()
            #<strong class="ll rating_num" property="v:average">7.9</strong>
            res_data['score'] = soup.find('strong', class_='ll rating_num').get_text()
            
            '''
            <div id="info">
            <span ><span class='pl'>导演</span>: <span class='attrs'><a href="/celebrity/1321812/" rel="v:directedBy">安东尼·罗素</a> / <a href="/celebrity/1320870/" rel="v:directedBy">乔·罗素</a></span></span><br/>
            <span ><span class='pl'>编剧</span>: <span class='attrs'><a href="/celebrity/1276125/">克里斯托弗·马库斯</a> / <a href="/celebrity/1276126/">斯蒂芬·麦克菲利</a> / <a href="/celebrity/1050183/">杰克·科比</a> / <a href="/celebrity/1154644/">乔·西蒙</a></span></span><br/>
            <span class="actor"><span class='pl'>主演</span>: <span class='attrs'><a href="/celebrity/1017885/" rel="v:starring">克里斯·埃文斯</a> / <a href="/celebrity/1016681/" rel="v:starring">小罗伯特·唐尼</a> / <a href="/celebrity/1054453/" rel="v:starring">斯嘉丽·约翰逊</a> / <a href="/celebrity/1021985/" rel="v:starring">塞巴斯蒂安·斯坦</a> / <a href="/celebrity/1027217/" rel="v:starring">安东尼·麦凯</a> / <a href="/celebrity/1053573/" rel="v:starring">唐·钱德尔</a> / <a href="/celebrity/1013770/" rel="v:starring">杰瑞米·雷纳</a> / <a href="/celebrity/1327680/" rel="v:starring">查德维克·博斯曼</a> / <a href="/celebrity/1003482/" rel="v:starring">保罗·贝坦尼</a> / <a href="/celebrity/1129847/" rel="v:starring">伊丽莎白·奥尔森</a> / <a href="/celebrity/1002667/" rel="v:starring">保罗·路德</a> / <a href="/celebrity/1044902/" rel="v:starring">艾米丽·万凯普</a> / <a href="/celebrity/1325351/" rel="v:starring">汤姆·霍兰德</a> / <a href="/celebrity/1053566/" rel="v:starring">丹尼尔·布鲁赫</a> / <a href="/celebrity/1100321/" rel="v:starring">弗兰克·格里罗</a> / <a href="/celebrity/1031849/" rel="v:starring">威廉·赫特</a> / <a href="/celebrity/1049612/" rel="v:starring">马丁·弗瑞曼</a> / <a href="/celebrity/1000111/" rel="v:starring">霍普·戴维斯</a> / <a href="/celebrity/1047974/" rel="v:starring">玛丽莎·托梅</a> / <a href="/celebrity/1313633/" rel="v:starring">吉姆·拉什</a> / <a href="/celebrity/1313839/" rel="v:starring">金世佳</a></span></span><br/>
            <span class="pl">类型:</span> <span property="v:genre">动作</span> / <span property="v:genre">科幻</span> / <span property="v:genre">冒险</span><br/>
            <span class="pl">官方网站:</span> <a href="http://marvel.com/captainamerica" rel="nofollow" target="_blank">marvel.com/captainamerica</a><br/>
            <span class="pl">制片国家/地区:</span> 美国<br/>
            <span class="pl">语言:</span> 科萨语 / 英语 / 德语 / 俄语 / 罗马尼亚语<br/>
            <span class="pl">上映日期:</span> <span property="v:initialReleaseDate" content="2016-05-06(中国大陆/美国)">2016-05-06(中国大陆/美国)</span> / <span property="v:initialReleaseDate" content="2016-04-12(加州首映)">2016-04-12(加州首映)</span><br/>
            <span class="pl">片长:</span> <span property="v:runtime" content="148">148分钟(中国大陆)</span> / 147分钟<br/>
            <span class="pl">又名:</span> 美国队长3：内战 / 美国队长3：英雄内战(港/台) / 美队3 / Captain America 3<br/>
            <span class="pl">IMDb链接:</span> <a href="http://www.imdb.com/title/tt3498820" target="_blank" rel="nofollow">tt3498820</a><br>
            </div>
            '''
            info = soup.find('div', id='info')      
            res_data['director'] = info.find('span').find('span',class_='attrs').get_text()
            res_data['scripter'] = info.find('span').find_next_sibling('span').find('span',class_='attrs').get_text()
            res_data['actor'] = info.find('span').find_next_sibling('span').find_next_sibling('span').find('span',class_='attrs').get_text()
            res_data['type'] = info.find('span', property='v:genre').get_text()
            res_data['country'] = info.find(text='制片国家/地区:').next_element
            res_data['date'] = info.find('span',property='v:initialReleaseDate').get_text()
            res_data['summary'] = soup.find('span',property='v:summary').get_text().strip()

        except:
            print ('invalid data')
            return None
        res_data['hotReview'] = self._get_hot_review(soup)
        return res_data
        
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self._get_new_data(page_url, soup)
        new_urls = self._get_new_urls(soup)

        return new_urls, new_data

        
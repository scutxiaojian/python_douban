import douban_url_manager,douban_downloader,douban_parser,douban_outputer

class SpiderMain(object):
	def __init__(self):
		self.urls = douban_url_manager.UrlManager()
		self.downloader = douban_downloader.HtmlDownloader()
		self.parser = douban_parser.HtmlParser()
		self.outputer = douban_outputer.HtmlOutputer()

	def craw(self,root_url):
		count = 1
		self.urls.add_new_url(root_url)
		
		while self.urls.has_new_url:
			try :
				new_url = self.urls.get_new_url()
				print('craw %d : %s' % (count,new_url))
				html_cont = self.downloader.download(new_url)
				new_urls,new_data = self.parser.parse(new_url,html_cont)
				self.urls.add_new_urls(new_urls)
				self.outputer.collect_data(new_data)
				if count == 20:
					break

				count = count + 1

			except:
				print('craw failed')
				
		self.outputer.output_html()
		self.outputer.output_xls()

if __name__=="__main__":
	root_url = "https://movie.douban.com/subject/25820460/"
	obj_spider = SpiderMain()
	obj_spider.craw(root_url)
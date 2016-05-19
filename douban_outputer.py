import xlwt
class HtmlOutputer(object):

	def __init__(self):
		self.datas = []

	def collect_data(self,data):
		if data is None:
			return
		self.datas.append(data)

	def output_html(self):

		hotReview = open('hotReview.html','w',encoding='utf-8')
		hotReview.write("<html>")
		hotReview.write("<head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"></head>")
		hotReview.write("<body>")
		hotReview.write("<table>")

		fout = open('output.txt','w',encoding='utf-8')
		for data in self.datas:
			fout.write('\n电影名：'+data['movieName']+'\n')
			fout.write('豆瓣评分：'+data['score']+'\n')
			fout.write('导演：'+data['director']+'\n')
			fout.write('编剧：'+data['scripter']+'\n')
			fout.write('主演：'+data['actor']+'\n')
			fout.write('类型：'+data['type']+'\n')
			fout.write('制片国家/地区：'+data['country']+'\n')
			fout.write('上映日期：'+data['date']+'\n')
			fout.write('剧情简介：'+data['summary']+'\n')

			hotReview.write("<tr>")
			hotReview.write("<td>电影名：%s<br>热评：%s<br></td>" % (data['movieName'],data['hotReview']))
			hotReview.write("</tr>")

		hotReview.write("</table>")
		hotReview.write("</body>")
		hotReview.write("</html>")
		fout.close()
		hotReview.close()

	def output_xls(self):
		w = xlwt.Workbook() #创建一个工作簿
		ws = w.add_sheet('sheet1') #创建一个工作表
		ws.write(0,0,u'序号')
		ws.write(0,1,u'电影名')
		ws.write(0,2,u'豆瓣评分')
		ws.write(0,3,u'导演')
		ws.write(0,4,u'编剧')
		ws.write(0,5,u'主演')
		ws.write(0,6,u'类型')
		ws.write(0,7,u'制片国家/地区')
		ws.write(0,8,u'上映日期')

		row = 1
		for data in self.datas:
			ws.write( row, 0, row )
			ws.write( row, 1, data['movieName'] )
			ws.write( row, 2, float(data['score']) )
			ws.write( row, 3, data['director'] )
			ws.write( row, 4, data['scripter'] )
			ws.write( row, 5, data['actor'] )
			ws.write( row, 6, data['type'] )
			ws.write( row, 7, data['date'] )
			row += 1
		w.save('movie.xls') #保存
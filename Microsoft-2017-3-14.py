import requests
import re
from bs4 import BeautifulSoup

# url = 'https://answers.microsoft.com/zh-hans/forum/forumthreadlist?forumId=7b159860-51a0-4f7f-baa5-f3f12aa8e4b7&sort=LastReplyDate&dir=Desc&tab=Threads&meta=surfpro4&status=all&mod=&modAge=&advFil=&postedAfter=&postedBefore=&page='
url = 'https://answers.microsoft.com/zh-hans/forum/forumthreadlist?forumId=7b159860-51a0-4f7f-baa5-f3f12aa8e4b7&sort=LastReplyDate&dir=Desc&tab=Threads&meta=surf3&status=all&mod=&modAge=&advFil=&postedAfter=&postedBefore=&page='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
s = requests.Session()
dateDic = {'一月':'1','二月':'2',
			'三月':'3','四月':'4',
			'五月':'5','六月':'6',
			'七月':'7','八月':'8',
			'九月':'9','十月':'10',
			'十一月':'11','十二月':'12'}
# f = open('Surface pro4.txt','w')
f = open('Surface pro3.txt','w')
f.write('帖子名称\t发帖时间\t查看数量\t回复数量\n')
f.flush()
count = 0

for i in range(48):
	res = s.get(url + str(i+1),headers = headers)
	soup = BeautifulSoup(res.text,'html.parser')
	nodes = soup.find_all('tr',class_ = 'forumList')
	for j in nodes:
		try:
			li = {}
			li['帖子名称'] = j.find('a',class_='forumTitleLink wrapWord').text.replace('\t','').replace('\n','').replace('\r','')
			ns = j.find_all('span',class_='text-nowrap')
			for k in ns:
				if '由' in k.text:
					try:
						date = re.search('[\u4e00-\u9fa5]+[ ][0-9]+[,][ ][0-9]+',k.text).group()
						month = dateDic[date[:date.find(' ')]]
						date = date[date.find(' ')+1:]
						day = date[:date.find(',')]
						year = date[date.find(',')+2:]
						li['发帖时间'] = year + '-' + month + '-' + day
					except:
						continue
				elif '浏览' in k.text:
					li['查看数量'] = re.search('[0-9]+',k.text).group()
				elif '次回复' in k.text:
					li['回复数量'] = re.search('[0-9]+',k.text).group()
				else:
					pass

			f.write(li['帖子名称'] + '\t' + li['发帖时间'] + '\t' + li['查看数量'] + '\t' + li['回复数量'] + '\n')
			f.flush()
			count += 1
			print('第' + str(count) + '个帖子爬取成功！')
		except:
			count += 1
			print('第' + str(count) + '个帖子爬取失败！')


f.close()




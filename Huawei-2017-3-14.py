import requests
import re
from bs4 import BeautifulSoup

s = requests.Session()
url = 'http://club.huawei.com/forum-1084-'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
res = s.get(url + str(1) + '.html', headers=headers)

soup = BeautifulSoup(res.text, 'html.parser')
num = soup.find('a', class_='last').text.replace('... ', '')
# num = 1
f = open('荣耀畅玩平板.txt', 'w')
f.write('帖子id\t帖子名称\t发帖时间\t查看数量\t回复数量\t帖子类型\n')
f.flush()
count = 0


for i in range(int(num)):
    res = s.get(url + str(i + 1) + '.html', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    nodes = soup.find_all('tbody',id = re.compile('normalthread_[0-9]+'))
    for j in nodes:
        try:
            li = []
            li.append(j['id'].replace('normalthread_',''))
            li.append(j.find('a',class_ = 's xst').text.replace('\t','').replace('\n','').replace('\r',''))
            # if li[-1] == '':
            #     print(j)
            #     dsadsadas()

            ns = j.find_all('span')
            for k in ns:
                try:
                    if re.search('[0-9]{4}[-][0-9]+[-][0-9]+$',k['title']):
                        li.append(re.search('[0-9]{4}[-][0-9]+[-][0-9]+$',k['title']).group())
                        break
                except:
                    if re.search('[0-9]{4}[-][0-9]+[-][0-9]+$',k.text):
                        li.append(re.search('[0-9]{4}[-][0-9]+[-][0-9]+$',k.text).group())
                        break
                    else:
                        pass

            li.append(j.find('span',class_ = 'thd-ico thd-view').text)
            li.append(j.find('span',class_ = 'thd-ico thd-replies').text) 
            li.append(j.find('span',class_ = 'thd_sort').text.replace('\t','').replace('\n','').replace('\r','')[1:-2])     
            f.write('\t'.join(li) + '\n')
            f.flush()    
            count += 1
            print('已经爬取' + str(count) + '个帖子！')
        except:
            count += 1
            print('第' + str(count) + '个帖子爬取失败！')

f.close()

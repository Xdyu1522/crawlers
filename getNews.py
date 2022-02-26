import bs4, requests
from fake_useragent import UserAgent
ua = UserAgent()
docs = []
hots = []
print('正在爬取百度今日新鲜事……')
headers = {'User-Agent':ua.random}
geturl = 'https://top.baidu.com/board?tab=realtime&sa=fyb_search_ala_36172_more'
req = requests.get(url=geturl, headers=headers)
find = bs4.BeautifulSoup(req.text, 'html.parser')
docf = find.findAll(name='div', attrs={"class" :"c-single-text-ellipsis"})
for i in range(len(docf)):
    docs.append(docf[i].getText())
hotf = find.findAll(name='div', attrs={"class" :"hot-index_1Bl1a"})
for c in range(len(hotf)):
    hots.append(hotf[c].getText())
with open('百度今日新鲜事.txt', 'w', encoding='utf-8') as f:
    for n in range(30):
        f.write(f'{n + 1}\n')
        f.write(f'{docs[n].strip()}\n')
        f.write(f'{hots[n].strip()}热度\n')
        f.write('---------------------------------------\n')
print('数据爬取完毕!')       
print('已将数据写入文件!')
x = input('按Enter键退出……')
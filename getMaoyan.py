import bs4
import requests
from fake_useragent import UserAgent
names = []
scores = []
stars = []
times = []
print('正在爬取猫眼电影前100中的电影信息')
page = 0
for c in range(10):
    ua = UserAgent(verify_ssl=False)
    headers = {'User-Agent':ua.random}
    url = f'https://maoyan.com/board/4?offset={page}'
    req = requests.get(url, headers=headers)
    print(f'Get from {url}……')
    req.raise_for_status()
    find = bs4.BeautifulSoup(req.text, 'html.parser')
    allname = find.findAll(name='p', attrs={"class" :"name"})
    for i in range(len(allname)):
        names.append(allname[i].getText())
    allscore = find.findAll(name='p', attrs={"class" :"score"})
    for n in range(len(allscore)):
        scores.append(allscore[n].getText())
    allstars = find.findAll(name='p', attrs={"class" :"star"})
    for c in range(len(allstars)):
        stars.append(allstars[c].getText())
    alltimes = find.findAll(name='p', attrs={"class" :"releasetime"})
    for r in range(len(alltimes)):
        times.append(alltimes[r].getText())
    page += 10
    print(f'{page}%')
with open('猫眼电影前100.txt', 'w', encoding='utf-8') as f:
    for w in range(100):
        f.write(f'{w + 1}\n')
        f.write(f'{names[w]}  ')
        f.write(f'{scores[w]}分\n')
        f.write(f'{stars[w].strip()}\n')
        f.write(f'{times[w]}\n')
        f.write('----------------------------------------------------------------------\n')
print('爬取完毕!')
print('已将内容写入文件')
x = input('按Enter键退出……')
from fake_useragent import UserAgent
import requests
import bs4
import sys, time
ua=UserAgent(verify_ssl=False)
url = input('请输入一个CSDN链接:') if len(sys.argv) == 1 else sys.argv[1]
headers = {'User-Agent':ua.random}
try:
    req=requests.get(url=url,headers=headers)
except Exception:
    print('请输入正确的网址！')
    time.sleep(1)
    sys.exit()
req.raise_for_status()
find = bs4.BeautifulSoup(req.text, 'html.parser')
code = find.findAll(name='code', attrs={"class" :"language-python"})
if len(code) == 0:
    code = find.findAll(name='code', attrs={"class" :"prism language-python"})
if len(code) == 0:
    code = find.select('code')
if len(code) == 0:
    print('对不起，不支持此类型的链接或链接输入错误！')
    time.sleep(1)
    sys.exit()
for codes in range(len(code)):
    print('\n', end='')
    print('---------------------------------')
    print(code[codes].getText())
    print('\n', end='')
    print('---------------------------------')
    print('\n', end='')
title = find.select('title')[0].getText()
filename = f'{title}.txt'
filename = filename.replace('/', '')
with open(filename, 'w',encoding='utf-8') as f:
    f.write(url)
    for codes in range(len(code)):
        f.write('\n')
        f.write('---------------------------------')
        f.write('\n')
        f.write(code[codes].getText())
        f.write('\n')
        f.write('---------------------------------')
print('已将代码写入文件！')
a = input('按Enter键退出')
sys.exit()
#爬取CSDN上需要登录才可以复制的脚本
#开发者:xie 2021.10.3
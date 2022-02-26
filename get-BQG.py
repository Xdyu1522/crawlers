import requests, bs4, sys, time, os
print('欢迎来到小说爬取程序,请输入书名')
book_name = input()
print('正在搜索……')
sear = requests.get(f'https://www.bige7.com/s?q={book_name}')
fsear = bs4.BeautifulSoup(sear.text, 'html.parser')
book_list = fsear.findAll(name='h4', attrs={"class" :"bookname"})
if len(book_list) == 0: 
    print('请输入正确的书名或检查网络！')
    time.sleep(2)
    sys.exit()
for i in range(len(book_list)): 
    print(i+1, book_list[i].getText())
n = 0
while n <= 0 or n >= len(book_list) + 1:
    print('请输入正确的序号')
    n = input()
    if n.isdigit(): 
        n = int(n)
    else: 
        n = 0
        continue
yn = input(f'确定为该编号（{n} {book_list[n-1].getText()}）吗？（确定按Enter，否则输入q退出重新选择）')
if yn == 'q': 
    sys.exit()
a = str(book_list[n-1])
b = bs4.BeautifulSoup(a, 'html.parser')
bookurl = f"https://www.bige7.com{b.a['href']}"
print(f'书本页面为{bookurl}')
os.makedirs(book_list[n-1].getText(), exist_ok=True)
print('成功创建文件夹')
os.chdir(f'./{book_list[n-1].getText()}')
cp = 1
burl = requests.get(bookurl)
burlf = bs4.BeautifulSoup(burl.text, 'html.parser')
mainurlf = burlf.findAll(name='a', attrs={"class" :"rl"})
mainurlff = bs4.BeautifulSoup(str(mainurlf[0]), 'html.parser')
mainurl = mainurlff.a['href']
a = list(str(mainurl))
a.remove('.'); a.remove('/')
main_url = f"{bookurl}{''.join(a)}"
while True:
    print(f'正在从{main_url}获取第{cp}章') 
    things_get = requests.get(main_url)
    things_find = bs4.BeautifulSoup(things_get.text, 'html.parser')
    try: 
        title = things_find.findAll(name='h1', attrs={"class" :"wap_none"})[0].getText()
    except IndexError: 
        print('爬取结束')
        break        
    thingsf = things_find.findAll(name='div', attrs={"id" :"chaptercontent"})
    things = str(thingsf[0].getText())
    things = '\n\n\u3000\u3000'.join(things.split())
    things = '\u3000\u3000' + things
    print(title, '\n', things)
    cp += 1
    print('正在保存')
    with open(f'{title}.txt', 'a', encoding='utf-8') as f: 
        f.write(things)
        f.write('\n')
    nexturl = str(things_find.findAll(name='a', attrs={"id" :"pb_next"})[0])
    nextf = bs4.BeautifulSoup(nexturl, 'html.parser')
    main_url = f"https://www.bige7.com{nextf.a['href']}"
    end = list(main_url)

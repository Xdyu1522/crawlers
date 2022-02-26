import tkinter as tk
from tkinter.constants import END
import requests, bs4, time, sys
word = input('Input a word to translation:')
url = f'http://www.youdao.com/w/eng/{word}/#keyfrom=dict2.index'
res = requests.get(url)
try:
    res.raise_for_status()
except requests.HTTPError:
    print('请输入正确的单词！')
    time.sleep(1)
    sys.exit()
find = bs4.BeautifulSoup(res.text, 'html.parser')
mean1 = find.findAll(name='div', attrs={"class" :"trans-container"})
try:
    mean2 = mean1[0].getText()
except IndexError:
    print('请输入正确的单词！')
    time.sleep(1)
    sys.exit()
mean2 = str(mean2)
mean = mean2.replace(' ', '')
mean = mean.replace('[', '')
mean = mean.replace(']', '')
mean = mean.strip()
mean = mean.replace('\n\n', '\n')#将两个换行符作为整体，替换为一个换行符
print(mean)
root = tk.Tk()
root.geometry('800x800')
root.title('翻译结果')
txt = tk.Text(root, font='等线 15')
txt.insert(END, mean)
txt.grid(row=0, column=0)
def save():
    global word
    filename = f'{word}.txt'
    with open(filename, 'w') as f:
        f.write(mean)
    root.destroy()
btn = tk.Button(root, text='保存到文件',font='等线 15', command=save)
btn.grid(row=1, column=0)
root.mainloop()
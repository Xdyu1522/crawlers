import requests, bs4, pymysql, datetime
class Jpb(): 
    def __init__(self): 
        now = datetime.datetime.now()
        self.tablename = f'T{now.strftime(r"%Y%m%d")}'
        self.conn = pymysql.connect(host='localhost', user='root', passwd='xdyu1031', database='2022jpb')
        self.cursor = self.conn.cursor()
        try: 
            self.cursor.execute(f'drop table {self.tablename};')
        except:...
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        sql2 = f"""CREATE TABLE IF NOT EXISTS {self.tablename} (
                Id int(5) PRIMARY KEY, Ranking int(5), Country_name VARCHAR(20), Gold_medal_num int(5), Silver_medal_num int(5), Bronze_medal_num int(5), Sum int(5)
                ) DEFAULT CHARSET utf8 COLLATE utf8_general_ci;"""
        self.cursor.execute(sql2)

    def main(self): 
        id = 1
        url = r'https://tiyu.baidu.com/beijing2022/home/tab/%E5%A5%96%E7%89%8C%E6%A6%9C'
        r = requests.get(url, headers=self.headers)
        find = bs4.BeautifulSoup(r.text, 'html.parser')
        countries_list = find.findAll(name='a', attrs={"class": 'medal-list-item-link'})
        for country in countries_list:
            name = country.select('div[class="national-name m-c-line-clamp1"]')[0].getText()
            gold = country.select('div[class="num"]')[0].getText()
            silver = country.select('div[class="num"]')[1].getText()
            bronze = country.select('div[class="num"]')[2].getText()
            sum = country.select('div[class="num"]')[3].getText()
            ranking = country.select('div[class="label-wrap"]')[0].getText().replace('\n', '').strip()
            print(ranking, name, gold, silver, bronze, sum)
            sql=f'insert into {self.tablename} values(%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql, (id, ranking, name, gold, silver, bronze, sum))
            self.conn.commit()
            id += 1
        self.cursor.close()
        self.conn.close()
        print('爬取成功.')

if __name__ == '__main__': 
    get = Jpb()
    get.main()
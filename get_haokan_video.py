import pymysql, requests, json, time, random
from fake_useragent import UserAgent
class Haokan(): 
    def __init__(self, word): 
        self.word = word
        self.conn = pymysql.connect(host='localhost', user='root', passwd='xdyu1031', database='Haokan')
        self.cursor=self.conn.cursor()
        # self.headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    def main(self): 
        # proxy_list = [
        # {"https": "https://112.115.57.20:3128"},        
        # {'https': 'https://121.41.171.223:3128'}]
        proxy = []
        headers = {'User-Agent':str(UserAgent().random)}
        sqln = f'DROP TABLE IF EXISTS {self.word}'
        self.cursor.execute(sqln)
        sql1 = f'CREATE TABLE IF NOT EXISTS {self.word} (id int(5) PRIMARY KEY,Viedo_id VARCHAR(30),Video_title VARCHAR(100),Video_author VARCHAR(20),Viedo_length VARCHAR (10),Video_link VARCHAR(5000),Viedo_cover_src VARCHAR(5000),Download_link VARCHAR(5000)) DEFAULT CHARSET utf8 COLLATE utf8_general_ci;'
        self.cursor.execute(sql1)
        n = 1
        id = 1
        proxies = { "http": None, "https": None}
        while True:
            url = f'https://haokan.baidu.com/web/search/api?pn={n}&rn=10&type=video&query={self.word}'
            r = requests.get(url, headers=headers)
            dic = json.loads(r.text) 
            n += 1
            if dic['errno'] == 0: 
                if len(dic['data']['list']) != 0:
                    for video in dic['data']['list']: 
                        vid = video['vid']
                        title = video['title']
                        author = video['author']
                        cover = video['cover_src']
                        videourl = f'https://haokan.baidu.com/v?vid={vid}'
                        video_url = f'https://haokan.baidu.com/v?vid={vid}&_format=json'
                        req = requests.get(video_url, headers=headers)
                        d = json.loads(req.text)
                        length = d['data']['apiData']['curVideoMeta']['time_length']
                        link = d['data']['apiData']['curVideoMeta']['clarityUrl'][-1]['url']
                        print(vid, title, author, cover, length, link)
                        sql=f'insert into {self.word} values(%s,%s,%s,%s,%s,%s,%s,%s)'
                        self.cursor.execute(sql, (id, vid, title, author, length, videourl, cover, link))
                        self.conn.commit()
                        id += 1
                else:
                    print(f'\033[35;46m----------------------------爬取了{id}个视频信息----------------------------\033[0m')
                    self.cursor.close()
                    self.conn.close()
                    break
            else:
                print(f'\033[35;46m----------------------------爬取了{id}个视频信息----------------------------\033[0m')
                self.cursor.close()
                self.conn.close()
                break
        time.sleep(random.randrange(1, 2))


if __name__ == '__main__': 
    haokan = Haokan('北京冬奥会')
    haokan.main()
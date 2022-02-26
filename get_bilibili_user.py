import requests, json, pymysql, time
class Bilibili_user(): 
    def __init__(self, uid): 
        self.uid = uid
        self.conn = pymysql.connect(host='localhost', user='root', passwd='xdyu1031', database='Bilibili_users')
        self.cursor=self.conn.cursor()
        self.headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    def get_tablename(self): 
        url = f'https://api.bilibili.com/x/space/acc/info?mid={self.uid}&jsonp=jsonp'
        r = requests.get(url, headers=self.headers)
        dic = json.loads(r.text)
        name = dic['data']['name']
        return name

    def main(self, tablename): 
        sql2 = f"""CREATE TABLE IF NOT EXISTS {tablename} (
               id int(5) PRIMARY KEY ,video_title VARCHAR(100),video_avid VARCHAR(20),video_bvid VARCHAR(20),video_play_num INT(10),video_comment_num VARCHAR(10),video_danmu_num VARCHAR(10),video_created DATETIME,video_length VARCHAR (10),video_description VARCHAR(1000),video_link VARCHAR (50)
                ) DEFAULT CHARSET utf8 COLLATE utf8_general_ci;"""
        self.cursor.execute(sql2)
        n =1
        id_num = 1
        while True: 
            url = f'https://api.bilibili.com/x/space/arc/search?mid={self.uid}&ps=30&tid=0&pn={n}&keyword=&order=pubdate&jsonp=jsonp'
            r = requests.get(url, headers=self.headers)
            dic = json.loads(r.text)
            video_list = dic['data']['list']['vlist']
            n += 1
            if len(video_list)!=0: 
                for video in video_list: 
                    title=video['title']
                    aid = video['aid']
                    bvid = video['bvid']
                    play_num = video['play']
                    comment_num=video['comment']
                    danmu_num=video['video_review']
                    created_ = video['created']
                    timeArray = time.localtime(created_)
                    created = time.strftime(r"%Y-%m-%d %H:%M:%S", timeArray)
                    print(created)
                    length=video['length']
                    description=video['description']
                    video_link='https://www.bilibili.com/video/' + bvid
                    sql=f'insert into {tablename} values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    self.cursor.execute(sql, (id_num,title,aid,bvid,play_num,comment_num,danmu_num,created,length,description,video_link))
                    self.conn.commit()
                    id_num += 1
                    print(title,aid,created,length,video_link)
            else: 
                print(f'\033[35;46m----------------------------爬取了{id_num-1}个视频----------------------------\033[0m')
                self.cursor.close()
                self.conn.close()
                break

if __name__ == '__main__': 
    user = Bilibili_user(565388139)
    tablename = user.get_tablename()
    user.main(tablename=tablename)
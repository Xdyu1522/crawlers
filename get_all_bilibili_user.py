import requests, json, pymysql, random, time, json
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
class Get_users(): 
    def __init__(self): 
        self.conn = pymysql.connect(host='localhost', user='root', passwd='xdyu1031', database='all_bilibili_users')
        self.cursor = self.conn.cursor()
        self.cursor.execute('drop table if exists all_users')
        sql = 'create table all_users(Id int(5) PRIMARY KEY, Name VARCHAR(30), Sex VARCHAR(5), Sign VARCHAR(100), Level int(10), Fans int(100), Face_url VARCHAR(100)) DEFAULT CHARSET utf8 COLLATE utf8_general_ci;'
        self.cursor.execute(sql)
        self.all = []

    def get(self, start, end, proxies): 
        ua = UserAgent()
        for i in range(start, end): 
            headers = {'User-Agent': str(ua.random), 'Connection': 'keep-alive'}
            info = requests.get(f'http://api.bilibili.com/x/space/acc/info?mid={i}&jsonp=jsonp', headers=headers, proxies=proxies)
            fans = requests.get(f'http://api.bilibili.com/x/relation/stat?vmid={i}&jsonp=jsonp', headers=headers, proxies=proxies)
            dinfo = json.loads(info.text)
            dfans = json.loads(fans.text)
            if dinfo['code'] == 0 and dfans['code'] == 0:
                id = dinfo['data']['mid']
                name = dinfo['data']['name']
                sex = dinfo['data']['sex']
                sign = dinfo['data']['sign']
                level = dinfo['data']['level']
                fan = dfans['data']['follower']
                face = dinfo['data']['face']
                dic = {'id': id, 'name': name, 'sex': sex, 'sign': sign, 'level': level, 'fan': fan, 'face':face}
                self.all.append(dic)
                time.sleep(random.randrange(1, 3))
            else: 
                time.sleep(random.randrange(1, 3))
                continue
            


    def main(self, start, end, max, proxies={'http': None, 'https': None}): 
        num = end-start
        if num % max != 0: 
            raise ValueError(f'请输入{max}的倍数')
        pool = ThreadPoolExecutor(max_workers=max)
        # start = 1
        futures = []
        starts = int(start - num/max)
        ends=int()
        while ends<end: 
            starts += int(num / max)
            ends = int(starts + num / max)
            if ends == end: ends+=1
            print(starts, ends)
            futures.append(pool.submit(self.get, starts, ends, proxies))
            # starts += int(num / max)
        wait(futures)
        for i in self.all: 
            id = i['id']
            name = i['name']
            sex = i['sex']
            sign = i['sign']
            level = i['level']
            fan = i['fan']
            face = i['face']
            sql=f'insert into all_users values(%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql, (id, name, sex, sign, level, fan, face))
            self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print(self.all)

if __name__ == '__main__': 
    get = Get_users()
    st = input('请输入起始UID:')
    while not st.isdigit():
        st = input('请输入起始UID:')
    st = int(st)

    ed = input('请输入结束UID:')
    while not ed.isdigit():
        ed = input('请输入起始UID:')
    ed = int(ed)

    th = input('请输入线程数:')
    while not th.isdigit():
        th = input('请输入线程数;')
    th = int(th)
    
    get.main(st ,ed , th)

    a = input('是否保存json?(是输入y,否上输入任意值)')
    if a == 'y':
        with open(f'UID{st}-{ed}.json', 'w') as f:
            tmp = {'data': get.all}
            f.write(json.dumps(tmp, indent=4))


import requests
from fake_useragent import UserAgent
import json
import queue
import threading
import time
import pymysql
import os
from pathlib import Path
import shutil

ua = UserAgent()


# 多线程
class MyThread(threading.Thread):
    def __init__(self, mid_queue):
        super(MyThread, self).__init__()
        self.mid_queue = mid_queue
        self.cnn = pymysql.connect(host='127.0.0.1', user='root', password='', port=3306, database='bilibili',
                              charset='utf8')
        self.cursor = self.cnn.cursor()
        self.sql = "insert into user_info (mid, name, sex, face, sign, level, birthday, official, archive_view, article_view, likes, follower, following) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def run(self):
        while not self.mid_queue.empty():
            dict = self.get_message()
            self.save(dict)

    def get_message(self):
        mid = self.mid_queue.get()
        info_dict = {}

        main_url = f"https://api.bilibili.com/x/space/acc/info?mid={mid}&jsonp=jsonp"
        like_view = f"https://api.bilibili.com/x/space/upstat?mid={mid}&jsonp=jsonp"
        following_follower = f"https://api.bilibili.com/x/relation/stat?vmid={mid}&jsonp=jsonp"

        headers = {
            "Referer": f"https://space.bilibili.com/{mid}",
            "User-Agent": ua.random
        }
        proxies = {
            'http': 'http://113.195.155.211:9999',
            'https': 'http://183.164.239.47:9999'
        }

        response = requests.get(main_url, headers=headers, proxies=proxies).json()

        if response['code'] == -404:
            # code=-404的为被封用户，无信息
            info_dict["id"] = mid
            info_dict["message"] = "该用户已被封号"
        else:
            # main_info
            main_response = response["data"]
            info_dict["mid"] = main_response['mid']
            info_dict["用户名"] = main_response["name"]
            info_dict["性别"] = main_response["sex"]
            info_dict["头像地址"] = main_response["face"]
            info_dict["签名"] = main_response["sign"]
            info_dict["等级"] = main_response["level"]
            info_dict["生日"] = main_response["birthday"]
            info_dict["认证信息"] = main_response["official"]["title"]

            # like&view info
            like_view_response = requests.get(like_view, headers=headers, proxies=proxies).json()["data"]
            info_dict["播放数"] = like_view_response["archive"]["view"]
            info_dict["阅读数"] = like_view_response["article"]["view"]
            info_dict["获赞数"] = like_view_response["likes"]

            # follower&following info
            following_follower_response = requests.get(following_follower, headers=headers, proxies=proxies).json()[
                "data"]
            info_dict["粉丝数"] = following_follower_response["follower"]
            info_dict["关注数"] = following_follower_response["following"]

            print(f'正在爬取:{mid}--{info_dict["用户名"]}信息~~~')

            img = requests.get(info_dict["头像地址"], headers=headers, proxies=proxies).content
            self.face_download(img, info_dict["用户名"], info_dict["头像地址"][-3:])
        return info_dict

    def save(self, dict):
        try:
            self.cursor.execute(self.sql, (dict['mid'], dict['用户名'], dict['性别'], dict['头像地址'], dict['签名'], dict['等级'], dict['生日'], dict['认证信息'], dict['播放数'], dict['阅读数'], dict['获赞数'], dict['粉丝数'], dict['关注数']))
            self.cnn.commit()
        except Exception as error:
            print(error)
            self.cnn.rollback()

    def face_download(self, img, name, extension_name):
        path = os.getcwd()
        path = os.path.join(path, 'img')
        dir = Path(path)
        if not dir.exists():
            os.makedirs(path)
        with open(path + f'\\{name}.{extension_name}', 'wb') as fp:
            fp.write(img)
            fp.close()


def main():
    threadings = []

    mid_queue = queue.Queue()
    mid = {mid_queue.put(str(i)) for i in range(1, 5)}  # 总用户数458241268

    for i in range(10):
        thread = MyThread(mid_queue)
        threadings.append(thread)
        thread.start()

    for i in threadings:
        i.join()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f'用时{end - start}s')

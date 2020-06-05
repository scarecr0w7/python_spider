import requests
import re
from selenium import webdriver
import time
from tqdm import tqdm


def no_wm_video(url):
    # 通过单个视频分享链接下载抖音无水印视频
    broswer = webdriver.PhantomJS()
    broswer.get(url)
    video_title = re.findall('<p class="desc">(.*?)</p>', broswer.page_source)[0]
    author = re.findall('<p class="name nowrap">(.*?)</p>', broswer.page_source)[0]
    video_url = re.findall('playAddr: "(.*?)",', broswer.page_source)[0]
    video_url = re.sub('playwm', 'play', video_url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36'
    }
    response = requests.get(video_url, headers=headers)
    with open(f'{author} {video_title}.mp4', 'wb') as fp:
        # fp.write(response.content)
        for data in tqdm(response.iter_content()):
            fp.write(data)
        print(f'{author} {video_title}已下载完成')


def main():
    tips = '''
    *************************************************************************************************************
        请输入分享链接，可以输入单个链接，也可输入多个链接。
        单个链接示例：https://v.douyin.com/JeUKHSf/
        多个链接示例：https://v.douyin.com/JeUKHSf/，https://v.douyin.com/JeUKHSf/，https://v.douyin.com/JeUKHSf/
        输入exit退出
    *************************************************************************************************************
    '''
    print(tips)
    while True:
        url = input('请输入链接>>')
        if url == 'exit':
            break
        if '，' in url:
            urls = re.split('，', url)
            for video in urls:
                no_wm_video(video)
                time.sleep(1)
        else:
            no_wm_video(url)

main()

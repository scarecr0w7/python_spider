import requests
import re
from selenium import webdriver


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
    with open(f'{author}--{video_title}.mp4', 'wb') as fp:
        fp.write(response.content)


if __name__ == '__main__':
    url = 'https://v.douyin.com/JeFMQ88/'
    no_wm_video(url)


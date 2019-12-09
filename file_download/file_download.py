import requests
from fake_useragent import UserAgent
from tqdm import tqdm

ua = UserAgent()


def download(url):
    file = url.split('/')[-1]
    title = url.split(':')
    if title[0] != ('http' and 'https'):
        print('输入链接错误请再次输入：')
        return None
    else:
        headers = {
            'UserAgent': ua.random
        }
        response = requests.get(url, headers, stream=True)
        content_size = int(response.headers['Content-Length'])/(1024*1024)
        if response.status_code == 200:
            with open(f'{file}', 'wb') as fp:
                for i in tqdm(iterable=response.iter_content(1024*1024), total=content_size, unit='M', desc=f'{file}'):
                    fp.write(i)
            print(f'{file}下载完成')
        else:
            print('链接异常请检查！')


if __name__ == '__main__':
    print('*' * 50)
    print('欢迎使用！！！')
    print('请输入类似格式（https://github.com/liangzhuz/python_spider/archive/master.zip）的链接下载文件, 或输入exit退出程序。')
    print('*' * 50)
    url = input('请输入：')
    while url != 'exit':
        download(url)
        url = input('请输入链接继续或 exit 退出：')

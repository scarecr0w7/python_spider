import requests
import re

s = requests.session()


def login_taobao(TPL_username, TPL_password_2, ua):
    try:
        # 验证用户名密码
        url = 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F'
        headers ={
            'content-length': '2931',
            'cache-control': 'max-age=0',
            'origin': 'https://login.taobao.com',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'referer': 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7'
        }
        data = {
            'TPL_username': TPL_username,
            'ncoToken': '733a05f5289720af3c850c8a9f698f96bfe6cd6a',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': 0,
            'newlogin': 0,
            'TPL_redirect_url': 'https://www.taobao.com/',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'loginType': '3',
            'gvfdcname': '10',
            'gvfdcre': '68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D613231626F2E323031372E3735343839343433372E372E3561663931316439316D4B67474E26663D746F70266F75743D7472756526726564697265637455524C3D68747470732533412532462532467777772E74616F62616F2E636F6D253246',
            'TPL_password_2': TPL_password_2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'oslanguage': 'zh-CN',
            'sr': '1920*1080',
            'naviVer': 'chrome|80.03987132',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'osPF': 'Win32',
            'appkey': '00000000',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/&useMobile=true',
            'um_token': 'T9A70753FED4D5DF4D703E42AB46F3611ACAA6E6D8F86A7FE16ADEFE1FB',
            'ua': ua
        }
        response = s.post(url, headers=headers, data=data)
        # 得到获取st码的网址
        token_url = re.search('<script src="(.*?)"></script>', response.text).group(1)

        # 获取st码
        st_response = s.get(token_url)
        st_code = re.search('"data":{"st":"(.*?)"}', st_response.text).group(1)

        # 根据st码登陆帐户
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'host': 'login.taobao.com'
        }
        login_url = f'https://login.taobao.com/member/vst.htm?st={st_code}'
        login_res = s.get(login_url, headers=headers)
        location_url = re.search('top.location.href = "(.*?)";', login_res.text).group(1)

        # 访问我的淘宝页面
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        my_taobao = s.get(location_url, headers=headers)
        name = re.search('<input id="mtb-nickname" type="hidden" value="(.*?)"/>', my_taobao.text).group(1)
        if my_taobao.status_code == 200:
            print(f'{name} 登陆成功！')
    except Exception as e:
        print('登陆失败！')
        print(f'Error: {e}')


if __name__ == '__main__':
    TPL_username = 'your username'
    TPL_password_2 = 'your password'
    ua = 'your ua'
    login_taobao(TPL_username, TPL_password_2, ua)

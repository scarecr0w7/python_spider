import time
import taobao_login
import re
import json
import pymongo


client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = client['database']
coll = db['collection']

TPL_username = 'your username'
TPL_password_2 = 'your password'
ua = 'your ua'
# 登陆taobao
taobao_login.login_taobao(TPL_username, TPL_password_2, ua)

commodity_name = '商品名称'
num = 0

while num <= 4356:
    kw = {
        'q': commodity_name,
        's': num
    }
    url = 'https://s.taobao.com/search?'
    response = taobao_login.s.get(url, params=kw)
    print(response.url)
    result = re.search('g_page_config = (.*?);\s*g_srp_loadCss\\(\\);', response.text).group(1)
    dict = json.loads(result)
    if dict['mods']['itemlist'] == "hide":
        # 如果"status"="hide"说明没有数据
        break
    datas = dict['mods']['itemlist']['data']['auctions']
    for data in datas:
        # 'category' == ''的商品不是搜索到的商品信息
        if data['category'] == '':
            continue
        try:
            # 天猫会员店商品信息无付款人数
            sell = data['view_sales']
        except Exception as e:
            sell = 'none'
        item = {
            'shop_name': data['nick'],
            'title': data['raw_title'],
            'detail_url': data['detail_url'],
            'price': data['view_price'],
            'location': data['item_loc'],
            'sell': sell,
        }
        coll.insert_one({**item})
    num += 44
    time.sleep(1)
import pymongo
import pandas as pd
from pyecharts.charts import Bar, Page, Pie
from pyecharts import options as opts


def process_sell(data):
    # 处理销售数据
    data = data.replace('人付款', '')
    if '万' in data:
        data = data.replace('万+', '')
        data = float(data) * 10000
        data = str(data).split('.')[0]
        return int(data)
    if '+' in data:
        data = data.replace('+', '')
        return int(data)
    if data == 'none':
        return 0
    else:
        return int(data)


def process_location(data):
    if ' ' in data:
        data = data.split(' ')[0]
        return data
    else:
        return data


def process_price(data):
    return float(data)


client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = client['taobao']
coll = db['search_data']
data = coll.find()

df = pd.DataFrame(data)

df['sell'] = df['sell'].map(process_sell)
sell_data = df.sort_values(by='sell', ascending=False)
sell_data = sell_data[['shop_name', 'sell']]

df['location'] = df['location'].map(process_location)

shop_name_group = df.groupby('shop_name').count()
shop_name_group = shop_name_group.sort_values(by=['title'], ascending=False)

prices = df.loc[:, 'price']
prices = prices.map(process_price)
price_data = pd.cut(prices, bins=[0, 50, 100, 150, 200, 10000], labels=['50以下', '50-100元', '100-150元', '150-200元', '200元以上']).value_counts()
list = [price_data[0], price_data[1], price_data[2], price_data[3], price_data[4]]
price = pd.DataFrame(list, index=['50以下', '50-100元', '100-150元', '150-200元', '200元以上'], columns=['A'])
price = price['A'].values.tolist()



# 数据可视化
page = Page()

# 价格区间柱状图
bar = Bar()
bar.add_xaxis(['50以下', '50-100元', '100-150元', '150-200元', '200元以上'])
bar.add_yaxis('价格区间统计', price)
page.add(bar)

# 销量前15店铺饼状图
pie = (
    Pie()
    .add('', sell_data.values.tolist()[:15])
    .set_global_opts(title_opts=opts.TitleOpts(title='销量前15店铺', pos_left='center'), legend_opts=opts.LegendOpts(is_show=False))

)
page.add(pie)

page.render()


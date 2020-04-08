淘宝搜索商品信息爬取并可视展示

### taobao_login.py

登陆淘宝

参数：

+ TPL_username：用户名
+ TPL_password_2：加密后的密码
+ ua：多个参数混合后的浏览器信息

参数通过浏览器抓包获取

## taobao.py

搜索商品并保存到Mnogodb数据库中

commodity_name需要爬取的商品名称

## data_analysis.py

对爬取到的数据进行可视化展示，输出到``render.html``查看

+ 店铺位置分布图
+ 销量前15店铺饼状图
+ 价格区间柱状图
+ 产品数量前15店铺柱状图

#### 效果

![1](https://github.com/liangzhuz/python_spider/blob/master/taobao_search_commodity_info/img/1.png)

![2](https://github.com/liangzhuz/python_spider/blob/master/taobao_search_commodity_info/img/2.png)

![3](https://github.com/liangzhuz/python_spider/blob/master/taobao_search_commodity_info/img/3.png)

![4](https://github.com/liangzhuz/python_spider/blob/master/taobao_search_commodity_info/img/4.png)
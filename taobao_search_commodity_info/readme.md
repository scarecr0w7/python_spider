# 淘宝搜索商品信息爬取

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


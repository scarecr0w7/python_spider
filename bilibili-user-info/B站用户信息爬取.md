# B站用户信息爬取

## 地址分析

​		经过分析B站用户信息是通过json加载

​		用户主要信息json地址：``https://api.bilibili.com/x/space/acc/info?mid={mid}&jsonp=jsonp``

​		获赞数和观看数json地址:``https://api.bilibili.com/x/space/upstat?mid={mid}&jsonp=jsonp``

​		粉丝数和关注数json地址：``https://api.bilibili.com/x/relation/stat?vmid={mid}&jsonp=jsonp``

​		其中{mid}为用户id

## 信息获取

​		首先判断``code ``是否为``-404``，``code == -404``说明该用户已被封，写入用户ID和说明，用户状态正常则获取用户``id``、``用户名``、``性别``、``头像地址``、``签名``、``等级``、``生日``、``认证信息``、``播放数``、``阅读数``、``获赞数``、``粉丝数``和``关注数``以供分析。

## 信息存储

​		最后，获取到的信息添加到Mysql数据库，并下载用户头像到当前目录的img目录下



##### 仅供学习


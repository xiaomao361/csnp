crew member sentry notification plugin
===

机组使用的[sentry-onpremise](https://github.com/getsentry/onpremise)的通知插件

目前包含了

+ 企业微信
+ 钉钉

两种通知方式

底层基于群聊机器人的webhook

sentry测试版本：`23.3.1`

可根据自己的需要填写企业微信key或者钉钉的token，也可以都添加会同时发送

安装方法：

进入sentry目录

1. `vim sentry/enhance-image.sh` 

添加下面内容

```bash
pip install csnp==0.0.7
```

> 莫名其妙的就从0.0.1到了0.0.7，因为没研究出来怎么在本地debug，调试只能每次上传到pypi以后，构建sentry测试

> 有知道的朋友麻烦告诉我怎么本地调试sentry，跪谢

2. 构建并重启sentry

`sudo docker-compose down`

`sudo ./install.sh`

`sudo docker-compose up -d`

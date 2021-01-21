# shopex-dingding-notify-2.x
基于python2.7.13版本，异常消息推送到钉钉

安装方式


    一、
    
    1、git clone https://github.com/magic119/shopex-dingding-notify-2.x.git
    
    2、切换到文件夹下，找到setup.py，在终端执行 python setup.py install 会自动将项目安装到第三方库中
    在执行命令之前，选择好对应的python版本，2.7.x
    
    二、推荐使用
        
    pip install -i https://pypi.org/simple/ shopex-dingding-notify-2.x

使用方式
    
    1、控制台打印的信息可以在安装好库中的conf文件夹的config.py中配置(不建议修改)，其他配置作用的详细信息请参考config.py中的
    注释。
    
    2、发送消息到指定的mq队列里面或者从mq队列里面取出消息发送到钉钉，都需要创建对应的客户端。
    
    代码事例：
    
        发送消息到钉钉（异常消息通知依赖于工程，工程停止，异常消息通知也会停止）
            from client.client import SendMessageToDingDing
            # 钉钉那边需要的参数
            app_key = "xxx"
            app_secret = "xxx"
            api_url = "xxx"

        client = SendMessageToDingDing(app_key=app_key, app_secret=app_secret, api_url=api_url, kwargs={})
        try:
            # 第一个参数是一个列表，表示要发送给谁
            # 第二个参数也是一个列表， 表示mq消息队列
            client.start(["s4261"], ["dingding"])
        except Exception as e:
            pass

        while 1:
            time.sleep(10)

        发送异常消息到mq（请提前在mq中创建好队列，绑定好交换机）
            kwargs = {
                "exchange_name": "amq.direct",
                "routing_key": "event"
            }

        client = SendMessageToMq(kwargs)
        client.send(json.dumps({"data": "test"}))

# Chatroom

## 环境配置
```
$ virtualenv env                  # 新建一个虚拟环境
$ env\Scripts\activate            # 激活虚拟环境
$ pip install -r requirements.txt # 生成文件需要的包
```
## 运行步骤
```
$ $env:FLASK_DEBUG = "1"          # 开启调试模式  (或者set FLASK_DEBUG=1)
$ $env:FLASK_APP = 'start'        # 设置app位置  （如果报错就设置）
$ flask forge                     # 生成虚假数据  （只需第一次）
$ flask run                       # 运行
* Running on http://127.0.0.1:5000/
```

## 测试账号
* email: `admin@123Wooden.com`
* password: `123Wooden`








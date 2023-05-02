# 2023/4/29
## error：
- 使用蓝图访问不到模板和静态资源  
    解决：
    1. 共用原始资源文件夹
        模板：在定义蓝图时声明位置：`template_folder="../templates"`
        静态资源：还没解决
    2. 拥有自己的资源文件夹
        模板：在定义蓝图时声明位置：`template_folder="templates"`
        静态资源：在定义蓝图时声明位置：`static_folder="static"`
                 同时在生成app实例时标明：`app = Flask('Chatroom', static_folder=None)`

## success：
+ 实现基本框架，初始化数据库
+ 实现客户端发送消息

---

# 2023/4/30
## error：
- 服务端向客户端广播消息时报错：
    `TypeError: Object of type method is not JSON serializable`
- 原因： 数据中的一个方法少了参数 'avatar': current_user.avatar(64)

- socket报错：
    `The WebSocket transport is not available, you must install a WebSocket server that is compatible with your async mode to enable it. See the documentation for details. (further occurrences of this error will be logged with level INFO)`
-原因： 安装了eventlet, 用flask_run命令运行
-解决： 指定异步模式socketio.init_app(app, async_mode='eventlet') 

- 指定异步模式后报错：
    `RuntimeError: You need to use the eventlet server. See the Deployment sectio`
-解决：使用socketio.run(app)运行

- 修改运行语句后使用flask run命令依然报错
-解决： 通过python start.py运行或直接通过编辑器运行该文件

- python start.py 终端一直在初始化
    `Server initialized for eventlet.`
-解决： 第一种方式：安装simple-websocket, 使用flask run运行
        第二种方式： 切换生产模式，用python start.py运行 
        ````
        from app import create_app
        from eventlet import wsgi
        import eventlet
        app = create_app()
        wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)
        ````
- tips: ````
        在下载了eventlet的情况下
        使用python start.py运行 使用的是eventlet
        使用flask run命令 使用的是threading
        ````

## success：
+ 实现服务端接受消息后再广播出去
+ 实现客户端接受服务端广播的消息并显示在页面上

---

# 2023/5/1
## error：
- 部署后报错：
    `WebSocket connection to 'ws://xxxx'failed`
- 解决：在socket.io.js文件中将'ws:'替换为'http:'
        ctrl+f 找到这行代码`var uri = this.uri()`，在后面追加
        `if (uri) 
            uri.replace('ws:', 'http:')`

## success：
+ 完成用户人员展示，上线昵称后面+绿点 下线去掉绿点
+ 上传到github
+ 在pythonanywhere部署
    ````
    # 部署配置
    # import sys
    # path = '/home/123Wooden/Chatroom'
    # if path not in sys.path:
    #     sys.path.append(path)
    # from start import app as applicaiton
    ````

---

# 2023/5/2
## error
- 配置pythonanywhere的数据库报错：
    `AttributeError: 'NoneType' object has no attribute 'get_engine'`
  解决：````
        migrate = Migrate()
        migrate.init_app(app, db)
        ````
- 配置pythonanywhere的数据库报错：
    `AttributeError: 'NoneType' object has no attribute 'drivername'`
  解决：````
        SQLALCHEMY_DATABASE_URI = 'xxx'
        or
        DATABASE_URL = 'xxx'
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        ````

## success
+ 改善pythonanywhere上的socket速度



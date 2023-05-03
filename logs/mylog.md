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
- 为静态资源打包后报错：
    `The referenced blueprint <Flask 'Chatroom'> has no static folder.`
  解决：声明根部静态资源位置`app = Flask('Chatroom', static_folder='asserts')`

## succes
+ 试图改善pythonanywhere上的socket速度，
    1. 查找数据库的慢查询语句
    2. 为页面设置缓存
    3. 静态资源打包
  部署需要 
    修改config.py和chat.py文件，开启缓存
    数据库初始化

# 2023/5/3

+ 增加了日志模块
+ 设置了不同的环境配置，部署只需修改.env中的FLASK_ENV,FLASK_CONFIG的两个变量值即可
+ 增加了根目录下的模板与静态资源文件夹，解决了蓝图模板继承根目录模板的问题
    参照http://fewstreet.com/2015/01/16/flask-blueprint-templates.html
+ 不完美地解决了在蓝图和根目录静态资源文件夹一致的情况下，蓝图静态资源访问不到的问题
搜索到的答案：
    1. 仅使用应用程序静态文件夹。
    2.注册蓝图时设置url_prefix。
    3.为蓝图使用另一个静态文件夹前缀。
    4.禁用应用程序静态文件夹app = Flask(__name__, static_folder=None)。
    5.使用带有静态端点描述符(https://stackoverflow.com/a/19179524/880326)的hack。
实际上：
    1是不可能的，太不方便了；
    2.我的index页面也在蓝图里呀，不方便；
    3.flask_assert里默认蓝图的静态资源是static的，不好改；
    4.前几天是这么解决的，但是不够美观；
    5.如果能解决就是最好的答案，但可惜试了一下没起作用。
    


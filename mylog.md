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
-环境： pip install eventlet
-解决： 指定异步模式socketio.init_app(app, async_mode='eventlet') 

- 指定异步模式后报错：
    `RuntimeError: You need to use the eventlet server. See the Deployment sectio`
-解决：使用socketio.run(app)运行

- 修改运行语句后使用flask run命令依然报错
-解决： 通过python start.py运行或直接通过编辑器运行该文件

- python start.py 突然运行不了了
-解决：以上问题都是因为下载了eventlet导致，卸载eventlet, 下载simple-websocket即可

## success：
+ 实现服务端接受消息后再广播出去
+ 实现客户端接受服务端广播的消息并显示在页面上


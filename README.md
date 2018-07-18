# pzl
### 你需要安装的依赖
**任何一步做不干净可能你都没办法成功跑出来，所以请务必按照 版本号&&网上的靠谱教程 安装**

后端(Server)代码运行环境 Python 3.6.5

Python3 依赖安装工具 pip3

数据库 MySQL 5.x(必须是5.x版本！使用的数据库连接库不支持新版本 MySQL)

Python 依赖：
逐个使用 pip3 安装 Flask, Flask-cors, pymysql, DBUtils

### 安装完毕后的你
1. 首先确保打开了 MySQL 服务器，且服务器监听 3306 端口
2. 确保 MySQL 服务器有 root 用户，且 root 用户的密码是 rootroot
3. 通过命令行，使用 root 账户登录 MySQL 服务器，新建一个数据库，并命名为 pzl
4. 使用命令行，到 /pzl/server 目录下，使用 python3 命令运行 dbinit.py 脚本进行数据库初始化（建表、插入初始数据）

**确保上述均完成后，**

使用**命令行**打开到 /pzl/server 目录下，使用 python3 命令运行 app.py 脚本

Flask 服务器运行在 127.0.0.1:5000 端口

登录页面 127.0.0.1:5000/login

### 初始数据
可以自己去看 dbinit.py 文件的最后几行

一个测试用户，username=pangzilong, password=pangzilong

还有三个测试订单

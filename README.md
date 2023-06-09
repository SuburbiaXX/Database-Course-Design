# NUAA-数据库课设
## 项目介绍
- 本项目旨在搭建一个 B/S 框架的在线 markdowm 编辑平台
- 其中已经实现了大部分的框架功能, 具体一些其他的功能可以再添加
- 已实现: 
  - markdown 文件的渲染、导出
  - 对某个 markdown 文件的共享, 并且可以指定是否可写
- 后续计划(画饼):
  - [ ] 支持导入 markdown 功能
  - [ ] 对文件分享的用户指定不同的权限(当前只能给分享的用户指定一样的权限)
  - [ ] 支持不同的文稿格式(这个已经在数据库中留有属性字段)

## 项目自述
- 本项目在构建和逻辑花费了大量的时间, 然后偷懒的地方也偷懒了(比方说不区分注册和登陆)
- 同时本项目的跳转十分简陋, 随随便便就可以攻击, 改一改 url 或者 sql 注入就寄了
- 本项目的框架逻辑代码绝对都是亲手所写,所以会有相当的 bug, 相关效果的 css 和 js 文件从网上找了点好康的, 然后进行缝合
- 综上所述, 本项目实质上是一坨屎山, 存在大量的调试注释, 并且 css 和 js 的引入和编写十分的不优雅, 但是代码能跑就行

## 项目结构
- 项目采用前后端分离的方式进行开发, 前端使用 jQuery、Bootstrap 相关样式, 后端使用 python 的 flask 框架
- 项目结构如下:
```bash
.
├── README.md
├── .gitignore
├── app.py
├── DB_Draft.sql
├── templates
│   ├── homepage.html
│   ├── editpage.html
│   ├── sourcepage.html
│   ├── login.html
│   ├── sharepage.html
│   ├── help.html
│   ├── setting.html
├── static
│   ├── mycss
│   │   ├── homepage.css
│   │   ├── login.css
│   │   ├── logo.css
│   │   ├── select.css
│   ├── myjs
│   │   ├── homepage.js
│   │   ├── select.js
│   │   ├── shapegenerator.js
│   │   ├── shapes.js
│   ├── bootstrap-4.6.2-dist # 使用 bootstrap4 样式进行开发
│   │   ├── css 相关
│   │   ├── js 相关
```


## 开发环境
- 操作系统: macOS Ventura 13.4
- Python: 3.8.16 + 相关库(见 app.py 中)
- flask: 2.2.3
- 开发工具:Vscode + PyCharm 2023.1.2 + Chrome
- 数据库: MySQL 8.0.32-arm64 | Navicat Premium 16.1.9
- 数据库相关表的构建, 见 `DB_Draft.sql`

## 项目运行
- 安装好相关的库, 并且配置好数据库
- 运行 `app.py` 文件

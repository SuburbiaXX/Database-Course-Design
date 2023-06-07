from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
# 配置数据库连接
HOSTNAME = "127.0.0.1"
PORT = "3306"
DATABASE = "DB_Draft"
USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
# 配置 SQLAlchemy 是否追踪对象的修改并发送信号
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 请求结束时会自动提交事务，即对数据库的更改会立即生效
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
# 配置 Bootstrap, 感觉不出来有什么不同, 但是还是放着
bootstrap = Bootstrap4(app)


@app.route('/')
def start():
    message = request.args.get('message')
    return render_template('login.html', message=message)


@app.route('/login', methods=['POST'])
def login():
    # 获取表单数据
    # print(request.form)
    entered_username = request.form['username']
    entered_password = request.form['password']
    if entered_username == "" or entered_password == "":
        # 用户名或密码为空
        return redirect(url_for('start', message='用户名或密码不能为空'))
    # 从数据库中获取用户名和密码
    user = db.session.execute(text('SELECT * FROM user WHERE username=:username'),
                              {'username': entered_username}).fetchone()
    if user and user.password == entered_password:
        # 登录成功
        return redirect(url_for('homepage', username=entered_username))
    elif user == None:
        # 新建这个用户
        phase = "INSERT INTO user (username, password) VALUES (:username, :password)"
        db.session.execute(text(phase), {'username': entered_username, 'password': entered_password})
        db.session.commit()
        return redirect(url_for('homepage', username=entered_username))
    else:
        return redirect(url_for('start', message='用户名已经存在或密码错误'))


@app.route('/homepage')
def homepage():
    username = request.args.get('username')
    # 根据 username 查询 history 数据表, 获取 username 一致的所有数据, 并且根据 modtime 降序排列, 只获取modtime是最近的 7 天的数据
    history = db.session.execute(
        text('SELECT * FROM history WHERE username=:username AND modtime>=DATE_SUB(CURDATE(), INTERVAL 6 DAY) ORDER BY modtime DESC'),
        {'username': username}).fetchall()
    # print(len(history))
    # 构造一个字典, 存储history中周一到周日的size的总和, 并且使得size[6]是今天的时间，size[0]是6天前的时间
    size = {}
    for i in range(7):
        size[i] = 0
    for i in range(len(history)):
        size[history[i].modtime.weekday()] += history[i].size

    return render_template('homepage.html', username=username, history=history, size=size)


@app.route('/sourcepage')
def sourcepage():
    # 查询 document 数据表, 获取 username 一致的所有数据
    username = request.args.get('username')
    documents = db.session.execute(text('SELECT * FROM document WHERE username=:username'),
                                   {'username': username}).fetchall()
    # 并且获取permission表中username不为username且shareable为1、sharee字段包含username的数据
    shared_documents = db.session.execute(
        text('SELECT * FROM permission WHERE username!=:username AND shareable=1 AND sharee LIKE :sharee'),
        {'username': username, 'sharee': '%' + username + '%'}).fetchall()


    # 合并shared_documents到documents之中
    for shared_document in shared_documents:
        documents.append(db.session.execute(text('SELECT * FROM document WHERE docname=:docname'),
                                            {'docname': shared_document.docname}).fetchone())
    
    # 渲染模板, 并传入数据
    if request.args.get('message'):
        message = request.args.get('message')
        return render_template('sourcepage.html', documents=documents, username=username, message=message)
    else:
        return render_template('sourcepage.html', documents=documents, username=username)


@app.route('/editpage')
def editpage():

    if request.args.get('ownername'):
        ownername = request.args.get('ownername')
        if ownername == "None":
            ownername = ""
    else:
        ownername = ""
    if request.args.get('message'):
        message1 = request.args.get('message')
    else:
        message1 = ""

    docname = request.args.get('docname')
    username = request.args.get('username')

    if request.args.get('NEW'):
        # 新建文档
        # 获取表单数据
        content = ""
        # 获取当前系统时间
        # 新创建数据
        try:
            # 向 document 数据表中插入数据
            phase = "INSERT INTO document (docname, createtime, updatetime, size, username) VALUES (:docname, NOW(), NOW(), :size, :username)"
            db.session.execute(text(phase), {'docname': docname, 'size': 0, 'username': username})
            db.session.commit()
            # 向 content 数据表中插入数据
            phase = "INSERT INTO content (docname, content, format, username) VALUES (:docname, :content, :format, :username)"
            db.session.execute(text(phase), {'docname': docname, 'content': content, 'format': '0', 'username': username})
            db.session.commit()
            # 向 permission 数据表中插入数据
            phase = "INSERT INTO permission (docname, username, shareable, writable, sharee) VALUES (:docname, :username, 0, 0, NULL)"
            db.session.execute(text(phase), {'docname': docname, 'username': username})
            db.session.commit()

            return render_template('editpage.html', username=username, docname=docname, message='新建文档成功!!!')
        except Exception as e:
            print(e)
            return redirect(url_for('sourcepage', username=username, message='新建文档失败, 请查看文件名称是否规范!!!'))
    else:
        # 从数据库中获取文档内容
        if ownername == username or ownername == "":
            try:
                phase = "SELECT content FROM content WHERE docname=:docname AND username=:username"
                content = db.session.execute(text(phase), {'docname': docname, 'username': username}).fetchone()[0]
                # print("数据库读取出来" + content)
                content = content.replace('<br>', '\r\n')
                # print("修改后" + content)
                # 返回 content 内容
                return render_template('editpage.html', username=username, docname=docname, content=content, message=message1)
            except Exception as e:
                print(e)
                return render_template('editpage.html', username=username, docname=docname, message='读取文档失败!!!')
        else:
            try:
                phase = "SELECT content FROM content WHERE docname=:docname AND username=:username"
                content = db.session.execute(text(phase), {'docname': docname, 'username': ownername}).fetchone()[0]
                # print("数据库读取出来" + content)
                content = content.replace('<br>', '\r\n')
                # print("修改后" + content)
                # 返回 content 内容
                return render_template('editpage.html', username=username, docname=docname, content=content, message=message1)
            except Exception as e:
                print(e)
                return render_template('editpage.html', username=username, docname=docname, message='读取文档失败!!!')


@app.route('/sharepage')
def sharepage():
    if request.args.get('message'):
        message = request.args.get('message')
    else:
        message = ""
    username = request.args.get('username')
    # 根据 username 查询 permission 数据表, 获取 username 为 username 的所有数据
    permissions = db.session.execute(text('SELECT * FROM permission WHERE username=:username'),
                                     {'username': username}).fetchall()
    # 从 user 数据表中获取除自己以外的所有用户
    users = db.session.execute(text('SELECT * FROM user WHERE username!=:username'), {'username': username}).fetchall()
    # 渲染模板, 并传入数据
    # print("读取数据")
    # print(permissions)
    # print(permissions[0].shareable)
    # print(users)
    return render_template('sharepage.html', username=username, permissions=permissions, users=users, message=message)


@app.route('/deletedoc')
def deletedoc():
    # 获取表单数据
    docname = request.args.get('docname')
    username = request.args.get('username')
    # 从 document 数据表中根据 docname 和 username 查询数据
    judge = db.session.execute(text('SELECT * FROM document WHERE docname=:docname AND username=:username'),{'docname': docname, 'username': username}).fetchone()
    if judge is None:
        return redirect(url_for('sourcepage', username=username, message='删除文档失败, 不能删除被分享的文件!!!'))

    # 删除数据
    try:
        phase = "DELETE FROM document WHERE docname=:docname"
        db.session.execute(text(phase), {'docname': docname})
        db.session.commit()
        return redirect(url_for('sourcepage', username=username, message='删除文档成功!!!'))
    except Exception as e:
        return redirect(url_for('sourcepage', username=username, message='删除文档失败, 请查看文件名称是否规范!!!'))


@app.route('/savedoc', methods=['POST'])
def savedoc():
    # 获取表单数据
    ownername = ""
    username = request.args.get('username')
    docname = request.args.get('docname')
    ownername = request.form['ownername']
    content = request.form['plain-text']
    content = content.replace('\r\n', '<br>')
    if ownername == "None":
        ownername = ""
    
    if ownername == username or ownername == "":
        # 更新数据
        try:
            phase = "UPDATE document SET updatetime=NOW(), size=:size WHERE docname=:docname AND username=:username"
            db.session.execute(text(phase), {'size': len(content), 'docname': docname, 'username': username})
            db.session.commit()

            phase = "UPDATE content SET content=:content WHERE docname=:docname AND username=:username"
            db.session.execute(text(phase), {'content': content, 'docname': docname, 'username': username})
            db.session.commit()

            # 向history表中新增数据
            phase = "INSERT INTO history (docname, username, modtime, content, size) VALUES (:docname, :username, NOW(), :content, :size)"
            db.session.execute(text(phase), {'docname': docname, 'username': username, 'content': content, 'size': len(content)})
            db.session.commit()

            return redirect(url_for('editpage', username=username, docname=docname, message='保存文档成功!!!'))
        except Exception as e:
            # print(e)
            return redirect(url_for('editpage', username=username, docname=docname, message='保存文档失败, 请重试!!!'))
    else:
        # 通过 docname 查询 permission 表, 判断 ownername 
        permission = db.session.execute(text('SELECT * FROM permission WHERE docname=:docname AND username=:username AND sharee LIKE :sharee'),{'docname': docname, 'username': ownername, 'sharee': '%' + username + '%'}).fetchone()
        # print(permission)
        if permission is not None and permission.writable == '1':
            try:
                phase = "UPDATE document SET updatetime=NOW(), size=:size WHERE docname=:docname AND username=:username"
                db.session.execute(text(phase), {'size': len(content), 'docname': docname, 'username': ownername})
                db.session.commit()

                phase = "UPDATE content SET content=:content WHERE docname=:docname AND username=:username"
                db.session.execute(text(phase), {'content': content, 'docname': docname, 'username': ownername})
                db.session.commit()

                # 向history表中新增数据
                phase = "INSERT INTO history (docname, username, modtime, content, size) VALUES (:docname, :username, NOW(), :content, :size)"
                db.session.execute(text(phase), {'docname': docname, 'username': username, 'content': content, 'size': len(content)})
                db.session.commit()
                return redirect(url_for('editpage', username=username, docname=docname, ownername=ownername, message='保存文档成功!!!'))
            
            except Exception as e:
                return redirect(url_for('editpage', username=username, docname=docname, ownername=ownername, message='保存文档失败, 请重试!!!'))
                
    return redirect(url_for('editpage', username=username, docname=docname, ownername=ownername, message='只读文档, 无法保存!!!'))
        

@app.route('/share', methods=['GET', 'POST'])
def share():
    # print(request.form)
    # 获取表单数据
    docname = request.form['docname']
    sharee = request.form['choose']
    shareable = request.form['shareable']
    writable = request.form['writable']
    username = request.form['username']
    # 如果 sharee 为空
    if sharee == '':
        sharee = ""
    # print(docname)
    # print(sharee)
    # print(shareable)
    # print(writable)
    # print(username)
    if shareable == 'true':
        shareable = 1
    else:
        shareable = 0

    # 获取数据库中原先分享情况
    phase = "SELECT shareable, writable FROM permission WHERE docname=:docname AND username=:username"
    shareable_old = db.session.execute(text(phase), {'docname': docname, 'username': username}).fetchone()
    db.session.commit()

    if writable == 'true' and shareable == 1:
        writable = 1
    elif (writable == 'true' and shareable == 0 and shareable_old == 0) or (shareable == 0 and sharee != '' and shareable_old == 0) or (shareable_old == 0 and shareable == 0 and sharee != '') :
        return redirect(url_for('sharepage', username=username, message='分享失败, 请重试!!!'))
    elif writable == 'false' and shareable == 0 and sharee == '' and shareable_old == 0:
        return redirect(url_for('sharepage', username=username))
    else:    
        writable = 0

    if (shareable_old == 1 and shareable == 0) or (shareable == 0):
        sharee = ""

    # 更新数据
    # try:
    phase = "UPDATE permission SET shareable=:shareable, writable=:writable, sharee=:sharee WHERE docname=:docname AND username=:username"
    db.session.execute(text(phase), {'shareable': shareable, 'writable': writable, 'sharee': sharee, 'docname': docname, 'username': username})
    db.session.commit()
    # except Exception as e:
        # return redirect(url_for('sharepage', username=username, message='分享失败, 请重试!!!'))
    
    # 重定向到 sharepage() 函数
    return redirect(url_for('sharepage', username=username, message='修改分享权限成功!!!'))


@app.route('/setting', methods=['GET', 'POST'])
def setting():
    # 获取用户名
    username = request.args.get('username')
    # 查询数据库中的用户信息
    user = db.session.execute(text('SELECT * FROM user WHERE username=:username'), {'username': username}).fetchone()
    email = user.email
    phone = user.phone
    if email == None:
        email = ''
    if phone == None:
        phone = ''
    return render_template('setting.html', username=username, email=email, phone=phone)


@app.route('/changeinfo' , methods=['POST'])
def changeinfo():
    # print(request.form)
    # 获取表单数据
    username_old = request.form['old_username']
    username_new = request.form['username']

    # 查询数据库, 如果 username_new 已经存在, 则返回错误信息
    user = db.session.execute(text('SELECT * FROM user WHERE username=:username'), {'username': username_new}).fetchone()
    if user is not None and username_new != username_old:
        return redirect(url_for('setting', username=username_old, message='用户名已存在!!!'))
    
    email = request.form['email']
    phone = request.form['phone']
    new_password = request.form['new_password']
    co_password = request.form['confirm_password']
    if new_password != co_password:
        return redirect(url_for('setting', username=username_old, message='两次密码不一致!!!'))
    # 更新数据
    try:
        phase = "UPDATE user SET username=:username_new, email=:email, phone=:phone, password=:new_password WHERE username=:username"
        db.session.execute(text(phase), {'username_new': username_new, 'email': email, 'phone': phone, 'new_password': new_password, 'username': username_old})
        db.session.commit()
        return redirect(url_for('setting', username=username_new, email=email, message='修改信息成功!!!'))
    except Exception as e:
        return redirect(url_for('setting', username=username_old, email=email, message='修改信息失败, 请重试!!!'))


@app.route('/help')
def help():
    username = request.args.get('username')
    return render_template('help.html', username=username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)

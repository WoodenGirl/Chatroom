from flask import Blueprint, render_template, abort, request, current_app
from flask_login import current_user
from flask_socketio import emit
from app.models import Message, User
from app.extensions import socketio, db, cache

chat_blue = Blueprint('chat', __name__, url_prefix="/chat", template_folder="templates", static_folder="static")

online_users = []

# 服务器接听消息

@socketio.on('connect')
def connect():
    global online_users
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)
        # 上线
        emit('online', {'online_id': current_user.id}, broadcast=True)
    emit('user count', {'count': len(online_users)}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
        # 下线
        emit('offline', {'offline_id': current_user.id}, broadcast=True)
    emit('user count', {'count': len(online_users)}, broadcast=True)

@socketio.on('new message')
def new_message(message_body): 
    message = Message(author=current_user._get_current_object(), body=message_body)
    db.session.add(message)
    db.session.commit()
    # 新消息
    emit('new message', { 
          'message_html': render_template('chat._message.html', message=message),
          'message_body': message_body,
          'avatar': current_user.avatar(64),
          'nickname': current_user.nickname,
          'user_id': current_user.id
          }, broadcast=True)

# Controller

# 渲染index

@chat_blue.route('/')
@cache.cached(timeout=60)
def index():
    users = User.query.all()
    user_amount = User.query.count() 
    messages = Message.query.order_by(Message.timestamp.asc())
    return render_template('chat.index.html', messages=messages, users=users, user_amount=user_amount)

# 删除消息

@chat_blue.route('/message/delete/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if current_user != message.author and not current_user.is_admin:
        abort(403)
    db.session.delete(message)
    db.session.commit()
    return '', 204

# 无限滑动

@chat_blue.route('/messages') 
def get_messages():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(
        page, per_page=current_app.config['CHATROOM_MESSAGE_PER_PAGE'])
    messages = pagination.items
    return render_template('chat._messages.html', messages=messages[::-1])

    

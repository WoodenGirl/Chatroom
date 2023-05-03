$(document).ready(function () {

    var ENTER_KEY = 13;
    // 客户端发送新信息
    function new_message(e) {
        var $textarea = $('#message-textarea');
        var message_body = $textarea.val().trim();   // 获取消息正文
        if (e.which === ENTER_KEY && !e.shiftKey && message_body) {
            e.preventDefault();   // 阻止默认行为，即换行
            socket.emit('new message', message_body);   // 发送事件，传入消息正文
            $textarea.val('')   // 清空输入框
        }
    }
    $('#message-textarea').on('keydown', new_message.bind(this));
    
    // 客户端监听消息
    socket.on('new message', function (data) {
        if (data.user_id !== current_user_id) {
            messageNotify(data);
        }
        $('.messages').append(data.message_html);   // 插入新消息到页面
        flask_moment_render_all();    // 渲染页面的时间戳
        scrollToBottom();     // 进皮条滚动到底部
    });

    // 统计上线人数
    socket.on('user count', function (data) {
        $('#user-count').html(data.count);
    })

    // 上线
    socket.on('online', function (data) {
        $user_status = $('.user_status')
        // if ($user_status.data('id') === data.online_id) {
        //      $user_status.append('<div>绿点</div>')
        // }        
        
    });

    // 下线
    socket.on('offline', function (data) {
        if ($user_status.data('id') === data.online_id) {
        } 
    });


    // 引用消息
    $('.messages').on('click', '.quoteMessage', function () {
        var $textarea = $('#message-textarea');
        var message = $(this).parent().find('.message-body').text();
        $textarea.val('>> ' + message + '\n\n');
        $textarea.val($textarea.val()).focus()
    });
    
    // 删除消息
    $('.messages').on('click', '.deleteMessage', function () {
        var $this = $(this);
        if (confirm('are you sure to delete this message ?'))
            $.ajax({
                type: 'DELETE',
                url: $this.data('href'),
                success: function () {
                    $this.parent().remove();
                },
                error: function () {
                    alert('Oops, something was wrong!');
                }
            });
    });

    // 滚动加载消息（一次30条）
    var page = 1
    function load_messages() {
        var $messages = $('.messages');
        var position = $messages.scrollTop();
        if (position === 0) {
            page ++;
            $.ajax({
                url: message_url,
                type: 'GET',
                data: {page: page},
                success: function (data) {
                    var before_height = $messages[0].scrollHeight;
                    $(data).prependTo(".messages").hide().fadeIn(800);
                    var after_height = $messages[0].scrollHeight;
                    flask_moment_render_all();
                    $messages.scrollTop(after_height - before_height);
                }
            })
        }
    }


    // 新消息通知
    function messageNotify(data) {
        if (Notification.permission !== "granted")
            Notification.requestPermission();
        else {
            var notification = new Notification("Message from " + data.nickname, {
                icon: data.gravatar,
                body: data.message_body.replace(/(<([^>]+)>)/ig, "")
            });

            notification.onclick = function () {
                window.open(root_url);
            };
            setTimeout(function () {
                notification.close()
            }, 4000);
        }
    }
    // 进皮条滚动到底部
    function scrollToBottom() {
        var $messages = $('.messages');
        $messages.scrollTop($messages[0].scrollHeight);
    }

});
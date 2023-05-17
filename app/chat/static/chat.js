$(document).ready(function () {

    var ENTER_KEY = 13;
    var message_count = 0;

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
        message_count++;
        if (!document.hasFocus()){   // 标签页消息提醒
            document.title = '(' + message_count + ') ' + 'ChatRoom';
        }
        if (data.user_id !== current_user_id) {  // 新消息通知
            messageNotify(data);
        }
        $('.messages').append(data.message_html);   // 插入新消息到页面
        flask_moment_render_all();    // 渲染页面的时间戳
        scrollToBottom();     // 进皮条滚动到底部
    });

    // 统计在线人数
    socket.on('user count', function (data) {
        $('#user-count').html(data.count);
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
            $('.ui.loader').toggleClass('active');
            $.ajax({
                url: messages_url,
                type: 'GET',
                data: {page: page},
                success: function (data) {
                    var before_height = $messages[0].scrollHeight;
                    $(data).prependTo(".messages").hide().fadeIn(800);
                    var after_height = $messages[0].scrollHeight;
                    flask_moment_render_all();
                    $messages.scrollTop(after_height - before_height);
                    $('.ui.loader').toggleClass('active');
                },
                error: function () {
                    alert('No more messages.');
                    $('.ui.loader').toggleClass('active');
                }
            })
        }
    }
    $('.messages').scroll(load_messages);


    // 新消息通知
    function messageNotify(data) {
        if (Notification.permission !== "granted")
            Notification.requestPermission();
        else {
            var notification = new Notification("Message from " + data.nickname, {
                icon: data.avatar(16),
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

    // 初始化
    function init() {
        $(window).focus(function () {  // 页面被激活
            message_count = 0;
            document.title = 'Chatroom';
        });
        scrollToBottom();
    }

    // 进皮条滚动到底部
    function scrollToBottom() {
        var $messages = $('.messages');
        $messages.scrollTop($messages[0].scrollHeight);
    }

    init()
});

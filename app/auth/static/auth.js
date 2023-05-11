$(document).ready(function () {
    // 验证用户名
    // 获取用户名表单
    const reg_nickname = document.querySelector('[name = register_nickname]');
    // 使用change事件  值发生变化的时候
    reg_nickname.addEventListener('change', verifyName);
    // 封装verifyName函数
    function verifyName() {
        const span = reg_nickname.nextElementSibling;
        // 定用户名规则
        const reg = /^[a-zA-Z0-9-_]{6,10}$/;
        if (!reg.test(reg_nickname.value)) {
            span.innerHTML = '输入不合法,请输入6~10位字母或数字';
            return false;
        }
        // 合法 清空span
        span.innerHTML = '';
        return true;
    };


    // 验证电子邮件
    // 获取电子邮件表单
    const reg_email = document.querySelector('[name = register_email]');
    // 使用change事件  值发生变化的时候
    reg_email.addEventListener('change', verifyEmail);
    // 封装verifyEmail函数
    function verifyEmail() {
        const span = reg_email.nextElementSibling;
        // 定邮箱规则
        const reg = /^[A-Za-z0-9\-_]+[A-Za-z0-9\.\-_]*[A-Za-z0-9\-_]+@[A-Za-z0-9]+[A-Za-z0-9\.\-_]*(\.[A-Za-z0-9\.\-_]+)*[A-Za-z0-9]+\.[A-Za-z0-9]+[A-Za-z0-9\.\-_]*[A-Za-z0-9]+$/;
        if (!reg.test(reg_email.value)) {
            span.innerHTML = '输入不合法,请输入正确的电子邮箱';
            return false;
        }
        // 合法 清空span
        span.innerHTML = '';
        return true;
    };


    // 验证密码
    // 获取密码表单
    const reg_password = document.querySelector('[name = register_password]');
    // 使用change事件  值发生变化的时候
    reg_password.addEventListener('change', verifyPwd);
    // 封装verifyPwd函数
    function verifyPwd() {
        const span = reg_password.nextElementSibling;
        // 定密码规则
        const reg = /^[a-zA-Z0-9-_]{6,20}$/;
        if (!reg.test(reg_password.value)) {
            span.innerHTML = '输入不合法,6~20位数字字母符号组成';
            return false;
        }
        // 合法 清空span
        span.innerHTML = '';
        return true;
    };


    // 再次验证密码，需与第一次的密码相同
    const password2 = document.querySelector('[name = password2]');
    // 使用change事件  值发生变化的时候
    password2.addEventListener('change', verifyConfirm);
    // 封装verifyConfirm函数
    function verifyConfirm() {
        const span = password2.nextElementSibling;
        if (password2.value != reg_password.value) {
            span.innerHTML = '两次密码输入不一致';
            return false;
        }
        // 合法 清空span
        span.innerHTML = '';
        return true;
    };


    // 勾选我同意模块后才能进行提交
    const queren = document.querySelector('[name = queren]');
    queren.addEventListener('click', is_checked);
    function is_checked() {
        if (queren.checked) {
            return true;
        }
        else {
            return false;
        }
    };


    // 以上全部验证通过才能进行提交
    const form = document.querySelector('form');
    // const span = queren.previousElementSibling;
    form.addEventListener('submit', function (e) {
        // 判断是否勾选我同意
        if (!is_checked()) {
            // span.innerHTML = '请勾选同意协议';
            alert('请勾选同意协议');
            // 阻止提交
            e.preventDefault();
        }
        // 依次判断上面的每个框框是否通过，只要有一个没有通过的就阻止提交
        if (!(verifyName() && verifyEmail() && verifyPwd() && verifyConfirm() && is_checked())) {
            e.preventDefault();
        }
    });


    // // 登录模块
    // // 点击提交模块
    // const form = document.querySelector('form');
    // const agree = document.querySelector('[name = agree]');
    // const email = document.querySelector('[name = email]')
    // form.addEventListener('submit',function(e){
    //     // 阻止默认行为
    //     e.preventDefault();
    //     if(!agree.checked){
    //         alert('请勾选同意协议');
    //     }

    //     // 记录用户名到本地存储
    //     localStorage.setItem('email',email.value);

    //     // 跳转到首页
    //     location.href = "{{url_for('chat.index')}}";
    // }); 

});

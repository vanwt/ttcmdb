function get_term_size() {
    // 此函数用于获取窗口大小
    var init_width = 10;
    var init_height = 18;

    var windows_width = $(window).width();
    var windows_height = $(window).height();

    return {
        cols: Math.floor(windows_width / init_width),
        rows: Math.floor(windows_height / init_height),
    }
}

$(function () {
    let cols = get_term_size().cols;
    let rows = get_term_size().rows;
    var term = new Terminal(
        {
            cols: cols,
            rows: rows,
            useStyle: true,
            cursorBlink: true
        }
    );
    // 创建websocket连接
    var sid = $('#sid').val();
    var key = $('#skey').val();
    var uid = $('#uid').val();
    var ssh_c = new WebSocket(
        'ws://' + window.location.host + '/ssh/web/?sid=' + sid + '&&uid=' + uid + '&&skey=' + key
    );
    ssh_c.onopen = function () {
        term.open(document.getElementById('terminal'));
    };
    // 接受消息
    ssh_c.onmessage = function (recv) {
        let data = JSON.parse(recv.data);
        let message = data['message'];
        term.write(message)
    };
    ssh_c.onclose = function (recv) {
        ssh_c.send(JSON.stringify("exit;"));
        console.error('websocket服务关闭')
    };
    //通过term发送消息，是一个字母一个字母的发送
    term.on('data', function (data) {
        let message = {};
        message['status'] = 0;
        message['message'] = data;
        var send_data = JSON.stringify(message);
        ssh_c.send(send_data)
    });
    var message = {'status': 0, 'message': null, 'cols': null, 'rows': null};
    /*
    * status 为 0 时, 将用户输入的数据通过 websocket 传递给后台, data 为传递的数据, 忽略 cols 和 rows 参数
    * status 为 1 时, resize pty ssh 终端大小, cols 为每行显示的最大字数, rows 为每列显示的最大字数, 忽略 data 参数
    * */
    $(window).resize(function () {
        let cols = get_term_size().cols;
        let rows = get_term_size().rows;
        message['status'] = 1;
        message['cols'] = cols;
        message['rows'] = rows;
        let send_data = JSON.stringify(message);
        ssh_c.send(send_data);
        term.resize(cols, rows)
    });
});
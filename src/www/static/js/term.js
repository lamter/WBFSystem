/**
 * Created by lamter on 15/10/21.
 * 实时刷新伪终端的数据
 */

var
    term = null;


function stop () {
    // 停止刷新日志
    this.pause = true;
    this.fill('终端停止刷新');
}

function start () {
    // 开始刷新
    term.pause = false;
    term.clean();
    refresh()

}

function restart (url){
    // 根据新参数重新开始刷新
    this.url = arguments[0] ? arguments[0] : this.url;
    this.tag = null;
    // 重启 需要清空原来的 log
    this.clean();
    this.start()
}

function refresh () {
    // 正常地获取最新的日志
    $.getJSON(term.url, term.getRequestData()).done(function (data) {
        for(i in data.log){
            // 将新的日志逐条装填在尾部
            term.fill(data.log[i]);
            term.tag = data.tag; // 更新 log 标签
        }
        // 没暂停，1秒后重刷
        if (! term.pause) {
            setTimeout(refresh, 1000)
        }

    }
    ).fail(function (xhr, status) {
        alert('失败: ' + xhr.status + ', 原因: ' + status);
        if (! term.pause) {
            setTimeout(refresh, 1000)
        }
    }
    ).always()
}



function fill (log) {
    // 装填日志
    term.ul.append("<li>" + log + "</li>");
    if (term.getLogNum() > term.size) {
        term.ul.children('li').first().remove(); // 清掉最前面的log
    }
}

function clean () {
    this.ul.html('')
}



function Terminal (url, ul) {

    this.url = url;     // 获取 log 的地址
    this.ul = ul;       // 装填日志的标签
    this.pause = true;      // 是否暂停
    this.size = 100;            // 最大行数
    this.tag = null;            // 日志位置的标记

    this.start = start;
    this.stop = stop;
    this.restart = restart;
    //this.refresh = refresh;
    this.clean = clean;
    this.fill = fill;
    this.getLogNum = function () {
        return this.ul.children('li').length
    };
    this.getRequestData = function () {
        data = {
            tag: this.tag
            ,num:this.size
        };

        return data
    }
}

function newTerminal (url, ul) {

    if (! ul.hasClass('terminal')){
        alert('错误的ul')
    }
    term = new Terminal(url, ul);
    return term;
}
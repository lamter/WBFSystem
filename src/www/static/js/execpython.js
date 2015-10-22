/*
 * 提交要执行的 python 代码 - v1.1 - 9/15/2015
 * Shawn
 */


function execPython (url, code) {
    $.post(url, {code:code, dataType:"json"}).done(function (data) {

        }
    ).fail(function (xhr, status) {
            alert('失败: ' + xhr.status + ', 原因: ' + status);
        }
    ).always()
}


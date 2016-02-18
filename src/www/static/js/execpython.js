/*
 * 提交要执行的 python 代码 - v1.1 - 9/15/2015
 * Shawn
 */


function execPython (url, code, fill) {
    $.post(url,
        {code:code}
        ,function (data) {
            if (data.log){
                for(i in data.log){
                fill(data.log[i])
            }
            }
        }
        ,"json"
    ).fail(function (xhr, status) {
            alert('失败: ' + xhr.status + ', 原因: ' + status);
        }
    ).always()
}


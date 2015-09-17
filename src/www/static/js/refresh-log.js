/*
 * python 实时刷新log - v1.1 - 9/10/2015
 * cordial
 */

//var ERROR_STATUS_JQUERY = 1;


var log = {
    init: function(logs, docId, url, requestMethod , logNum) {
        logs.queryNum = 0;
        logs.logs = logs;
        logs.docId = docId;
        logs.url = url;
        logs.requestMethod = requestMethod;
        logs.logNum = logNum;
        logs.requestData = {};
        logs.tag = null;
        logs.logArray = [];
    },

};

function queryLog(logs) {
    logs.queryNum += 1;
    //alert(logs.queryNum);
    jQuery.ajax({
        type: logs.reqMethod,
        url: logs.url,
        timeout: 1000,
        dataType: 'json',
        data: jQuery.param(logs.requestData, true),
        error: function (errorData, status, error){
            // 查询日志后出错的回调
            logs.logArray.push('requestError:' + status);
            flushLog(logs);
            },
        success: function(data) {
            if(data.log){
                // data 数据格式 {tag 1, type 2001, log [logStr, ...]}
                logs.requestData.tag = data.tag; // 更新日志的标签标签
                for(var logStr in data.log){
                    addLog(logs, data.log[logStr]);
                }

            flushLog(logs);
            }
        },
    });
}

function flushLog(logs) {
    try{
        var docShow = jQuery(logs.docId);
        docShow.html();// 清空数据, 后他们刷新数据
        tmpHtml = '';
        for(var logStr in logs.logArray){
            tmpHtml = tmpHtml + logs.logArray[logStr] + '<br>';
        }
        docShow.html(tmpHtml)
    }
    catch(e) {
        alert('12141' + e)
    }

}


function addLog(logs, logStr) {
    if(logs.logArray.length > logs.logNum){
        // 如果大于log数量, 先踢出一个元素
        logs.logArray.shift()
    }
    logs.logArray.push(logStr)
}

function refreshLog(logs) {
    setInterval(queryLog, 1000, logs);
}


/*
 * python 实时刷新log - v1.1 - 9/10/2015
 * cordial
 */

//var ERROR_STATUS_JQUERY = 1;


var log = {
    init: function(logs, docId, url, requestMethod , logNum) {
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


//
//function Log(docId, url, reqMethod, logNum){
//    this.logArray = []; // 日志的序列
//    this.requestData = {}; // 用于查询时的请求数据
//    this.docId = docId;
//    this.url = url; // 日志的查询地址
//    this.reqMethod = reqMethod;
//    this.logNum = logNum; // 日志的行数
//
//    this.queryLog = function(){
//        // 循环请求log数据
//        alert(this.reqMethod);
//        alert(this.url);
//        jQuery.ajax({
//            type: this.reqMethod,
//            url: this.url,
//            timeout: 1000,
//            dataType: 'json',
//            data: jQuery.param(this.requestData, true),
//            error: this.errorCalbak,
//            success: this.successCalbak
//        });
//
//    };
//
//    this.flushLog = function(){
//        // 将获得的日志刷到页面上
//        var docShow = jQuery(this.docId);
//        docShow.html();// 清空数据, 后他们刷新数据
//        tmpHtml = '';
//        for(var logStr in this.logArray){
//            tmpHtml = tmpHtml + this.logArray[logStr] + '<br>';
//        }
//        docShow.html(tmpHtml)
//    };
//
//    this.refreshLog = function(){
//        // 循环获取日志
//        setInterval(this.queryLog, 1000);
//    };
//
//    this.errorCalbak = function(errorData, status, error){
//        // 查询日志后出错的回调
//        this.logArray.push('requestError:' + status);
//        this.flushLog();
//        };
//
//    this.successCalbak = function(data){
//        // 查询日志成功后的回调
//        if(data.log){
//            // data 数据格式 {tag 1, type 2001, log [logStr, ...]}
//            this.requestData.tag = data.tag; // 更新日志的标签标签
//
//            for(var logStr in data.log){
//                this.addLog(logStr);
//            }
//
//        this.flushLog();
//        }
//
//    };
//
//    this.addLog = function(logStr) {
//        if(this.logArray.length > this.logNum){
//            // 如果大于log数量, 先踢出一个元素
//            this.logArray.shift()
//        }
//        this.logArray.push(logStr)
//    };
//
//}
//
//function test() {
//    alert(1212);
//}
//

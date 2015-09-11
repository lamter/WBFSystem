/*
 * python 实时刷新log - v1.1 - 9/10/2015
 * cordial
 */

var logArray = []
var log = {
    refreshLog: function(docId, url, reqData, reqMethod, logNum){
        setInterval(this.showLog, 2000, docId, url, reqData, reqMethod, logNum)
    },

    showLog: function(docId, url, reqData, reqMethod, logNum){
        // 循环请求log数据
        alert(url)
        jQuery.ajax({
            type: reqMethod,
            url: url,
            timeout: 1000,
            dataType: 'json',
            data: jQuery.param(reqData, true),
            error: function(errorData, status, error){
                //alert(status)
                logArray.push('requestError:' + status)
            },
            success: function(data){
                if(data.log){
                    // data 数据格式 {tag 1, type 2001, log [logStr, ...]}
                    for(var logStr in data.log){
                        if(logArray.length > logNum){
                            // 如果大于log数量, 先踢出一个元素
                            logArray.shift()
                        }
                        logArray.push(data.log[logStr])
                    }
                    var docShow = jQuery(docId);
                    docShow.html();// 清空数据, 后他们刷新数据
                    tmpHtml = ''
                    for(var logStr in logArray){
                        tmpHtml = tmpHtml + logArray[logStr] + '<br>';
                    }
                    docShow.html(tmpHtml)
                }
                refreshLog(docId, url, reqData, logNum)
            }
        });
    }

}



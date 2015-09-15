/*
 * 提交要执行的 python 代码 - v1.1 - 9/10/2015
 * Shawn
 */


var execPython = {
    run: function(url, code){
        // 要传递的参数
        requestData = {};
        requestData.code = code

        jQuery.ajax({
            type: 'POST',
            url: url,
            timeout: 1000,
            dataType: 'json',
            data: jQuery.param(requestData, true),

            error: function(errorData, status, error){
                //alert(status)
                alert('requestError:' + status)
            },

        });
    }

}



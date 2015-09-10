/*
 * python jschart 图表demo - v1.1 - 8/18/2015
 * cordial
 */

(function(){
    window.pChart = {
        drawChart: function(divId, data){
            // 根据类型生成对应的图表
            if(!data){
                // 如果是空对象
                return
            }

            // 设置图表的显示的div, type与服务器端的type对应
            data.render = divId
            if(data.type == 'line2D'){
                drawLine2D(divId, data)
            }else if(data.type == 'pie2D'){
                drawPie2D(divId, data)
            }else if(data.type == 'bar2D'){
                drawBar2D(divId, data)
            }else if(data.type == 'area2D'){
                drawArea2D(divId, data)
            }else if(data.type == 'column2D'){
                drawColumn2D(divId, data)
            }else if(data.type == 'pie3D'){
                drawPie3D(divId, data)
            }else if(data.type == 'column3D'){
                drawColumn3D(divId, data)
            }


        },
    };
    function drawLine2D(divId, data){
		// 生成对象
		var chart = new iChart.LineBasic2D(data);
		chart.draw();

    };
    function drawPie2D(divId, data){
        var chart = new iChart.Pie2D(data);
		chart.draw();
    };
    function drawBar2D(divId, data){
        var chart = new iChart.Bar2D(data);
		chart.draw();
    };
    function drawArea2D(divId, data){
        var chart = new iChart.Area2D(data);
        chart.draw();
    };
    function drawColumn2D(divId, data){
        var chart = new iChart.Column2D(data);
        chart.draw();
    };
    function drawPie3D(divId, data){
        var chart = new iChart.Pie3D(data);
		chart.draw();
    };
    function drawColumn3D(divId, data){
        var chart = new iChart.Column3D(data);
        chart.draw();
    };

})();

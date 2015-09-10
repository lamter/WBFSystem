# coding:utf-8
"""
Created on 2015/8/14

图封装表的类, 框架是基于ichartjs 图表框架
由于此框架是开源免费的, 并且利用封装

操作实例
http://www.ichartjs.com/samples/index.html

@author: Cordial
"""

CHART_TYPE_LINE = "line2D"              # 折线图
CHART_TYPE_PIE_2D = "pie2D"             # 饼图
CHART_TYPE_BAR_2D = "bar2D"             # 条形图
CHART_TYPE_AREA_2D = "area2D"           # 区域图
CHART_TYPE_COLUMN_2D = "column2D"       # 柱状图
CHART_TYPE_PIE_3D = "pie3D"             # 3D饼图
CHART_TYPE_COLUMN_3D = "column3D"       # 3D柱状图


class BaseChart(object):
    """
    图表的基类
    """

    def __init__(self):
        """初始化数据, 先设置默认值"""

        self.title = {'text': ''}                               # 图表的标题
        self.data = []                                          # 数据
        self.height = 400                                       # 高度
        self.width = 800                                        # 宽度
        self.type = ''                                          # 图形类型
        self.extraDic = {}                                      # 自定义的dic, 这个要配合ichart用
        self.subtitle = {'text': ''}                            # 副标题
        self.footnote = {}                                      # 脚注


    def setTitle(self, title=''):
        """
        设置标题
        :param title: 标题 str
        """
        self.title['text'] = title


    def setSubTitle(self, title='', color='', fontsize=0):
        """
        设置副标题
        :param title:
        :return:
        """
        if title:
            self.subtitle['text'] = title
        if color:
            self.subtitle['color'] = color
        if fontsize:
            self.subtitle['fontsize'] = int(fontsize)


    def setFootNote(self, title='', color='', fontsize=0):
        """
        设置脚注
        :param title:
        :return:
        """
        if title:
            self.footnote['text'] = title
        if color:
            self.footnote['color'] = color
        if fontsize:
            self.footnote['fontsize'] = int(fontsize)


    def setTitleColor(self, color):
        """
        设置字体颜色
        :param color: 标题颜色 RGB 格式字符串
        """
        self.title['color'] = color


    def setTitleFontSize(self, fontSize):
        """
        设置标题的字体大小
        :param fontSize: 字体大小 int
        """
        self.title['fontsize'] = fontSize


    def setSize(self, widthSize, heightSize):
        """
        设置图片的div 的大小
        :param widthSize: 宽度(像素)
        :param heightSize: 高度(像素)
        """
        self.width = widthSize
        self.height = heightSize


    def addData(self, data=None):
        """
        设置数据, 在子类中重写
        :param data: 数据
        """
        pass


    def addExtraDic(self, dic):
        """
        增加额外的数据
        :param dic: 额外的配置数据
        """
        self.extraDic.update(dic)


    def setLegend(self, flag=True):
        """
        设置图例, 默认图例, 只设置开关
        :param flag: 开关
        """
        dic = {'legend': {'enable': True}}
        self.extraDic.update(dic)

    def toDic_data(self):
        """
        得到数据, 在子类中重写
        """
        return []


    def toDic_json(self):
        """
        组织的json数据
        """
        dic = {}
        dic["title"] = self.title
        dic["height"] = self.height
        dic["width"] = self.width
        dic["data"] = self.toDic_data()
        dic["type"] = self.type
        dic['footnote'] = self.footnote
        dic['subtitle'] = self.subtitle

        ''' 额外的配置数据 '''
        dic.update(self.extraDic)

        return dic



class Line2DChart(BaseChart):
    """
    折线图, 构建折线图数据
    """
    class lineData:
        def __init__(self, name, value, color, line_width):
            """
            折线图的数据类型
            :param name: 折线的名称
            :param value: 折线的值
            :param color: 折线的颜色
            :param line_width: 折线的大小
            :return:
            """
            self.name = name
            self.value = value
            self.color = color
            self.line_width = line_width

        def toDic(self):
            """
            todic
            :return:
            """
            dic = {}
            dic['name'] = self.name
            dic['value'] = self.value
            dic['color'] = self.color
            dic['line_width'] = self.line_width
            return dic


    def __init__(self):
        super(Line2DChart, self).__init__()

        """ 折线图特有的属性 """
        self.labels = []
        self.type = CHART_TYPE_LINE


    def addData(self, data):
        """
        设置数据, 可以设置多条, 可以直接调这个接口,
        :param data: 数据obj
        """
        if data == None or not isinstance(data, self.lineData):
            ''' 如果不是指定的对象, 直接返回 '''
            return

        self.data.append(data)


    def setLabels(self, labels=[]):
        """
        设置label
        :param labels:
        :return:
        """
        self.labels = labels


    def toDic_json(self):
        """
        重写todic
        :return:
        """
        dic = super(Line2DChart, self).toDic_json()
        if self.labels:
            ''' 下发labels '''
            dic['labels'] = self.labels

        return dic


    def toDic_data(self):
        """
        下发数据给客户端
        :return:
        """
        return [d.toDic() for d in self.data if d]


class Bar2DChart(BaseChart):
    """
    构建条形图
    """
    class barData:
        def __init__(self, name, value, color):
            """
            柱状图的数据类型
            :param name: 条形图名称
            :param value: 条形图的值
            :param color: 条形图的颜色
            :return:
            """
            self.name = name
            self.value = value
            self.color = color


        def toDic(self):
            """
            todic
            :return:
            """
            dic = {}
            dic['name'] = self.name
            dic['value'] = self.value
            dic['color'] = self.color
            return dic


    def __init__(self):
        super(Bar2DChart, self).__init__()

        """ 条形图特有的属性 """
        self.labels = []
        self.type = CHART_TYPE_BAR_2D


    def addData(self, data):
        """
        设置数据, 可以设置多条, 可以直接调这个接口,
        :param data: 数据obj
        """
        if data == None or not isinstance(data, self.barData):
            ''' 如果不是指定的对象, 直接返回 '''
            return

        self.data.append(data)


    def setLabels(self, labels=[]):
        """
        设置label
        :param labels:
        :return:
        """
        self.labels = labels


    def toDic_json(self):
        """
        重写todic
        :return:
        """
        dic = super(Bar2DChart, self).toDic_json()
        if self.labels:
            ''' 下发labels '''
            dic['labels'] = self.labels

        return dic


    def toDic_data(self):
        """
        下发数据给客户端
        :return:
        """
        return [d.toDic() for d in self.data if d]



class Pie2DChart(BaseChart):
    """
    饼图
    """
    class pieData:
        def __init__(self, name, value, color):
            """
            饼图的数据类型
            :param name: 名称
            :param value: 值
            :param color: 颜色
            :return:
            """
            self.name = name
            self.value = value
            self.color = color


        def toDic(self):
            """
            todic
            :return:
            """
            dic = {}
            dic['name'] = self.name
            dic['value'] = self.value
            dic['color'] = self.color
            return dic


    def __init__(self):
        super(Pie2DChart, self).__init__()

        """ 饼图有的属性 """
        self.type = CHART_TYPE_PIE_2D


    def addData(self, data):
        """
        设置数据, 可以设置多条, 可以直接调这个接口,
        :param data: 数据obj
        """
        if data == None or not isinstance(data, self.pieData):
            ''' 如果不是指定的对象, 直接返回 '''
            return

        self.data.append(data)


    def toDic_json(self):
        """
        重写todic
        :return:
        """
        dic = super(Pie2DChart, self).toDic_json()
        return dic


    def toDic_data(self):
        """
        下发数据给客户端
        :return:
        """
        return [d.toDic() for d in self.data if d]


class Area2DChart(BaseChart):
    """
    区域图
    """
    class areaData:
        def __init__(self, name, value, color, line_width):
            """
            区域图的数据类型
            :param name: 名称
            :param value: 值
            :param color: 颜色
            :return:
            """
            self.name = name
            self.value = value
            self.color = color
            self.line_width = line_width

        def toDic(self):
            """
            todic
            :return:
            """
            dic = {}
            dic['name'] = self.name
            dic['value'] = self.value
            dic['color'] = self.color
            dic['line_width'] = self.line_width
            return dic


    def __init__(self):
        super(Area2DChart, self).__init__()

        """ 区域图有的属性 """
        self.labels = []
        self.type = CHART_TYPE_AREA_2D


    def addData(self, data):
        """
        设置数据, 可以设置多条, 可以直接调这个接口,
        :param data: 数据obj
        """
        if data == None or not isinstance(data, self.areaData):
            ''' 如果不是指定的对象, 直接返回 '''
            return

        self.data.append(data)


    def setLabels(self, labels=[]):
        """
        设置label
        :param labels:
        :return:
        """
        self.labels = labels


    def toDic_json(self):
        """
        重写todic
        :return:
        """
        dic = super(Area2DChart, self).toDic_json()
        if self.labels:
            dic['labels'] = self.labels

        return dic


    def toDic_data(self):
        """
        下发数据给客户端
        :return:
        """
        return [d.toDic() for d in self.data if d]


class Column2DChart(BaseChart):
    """
    构建柱状图
    """
    class columnData:
        def __init__(self, name, value, color):
            """
            柱状图的数据类型
            :param name: 柱状名称
            :param value: 柱状的值
            :param color: 柱状的颜色RGB
            :return:
            """
            self.name = name
            self.value = value
            self.color = color


        def toDic(self):
            """
            todic
            :return:
            """
            dic = {}
            dic['name'] = self.name
            dic['value'] = self.value
            dic['color'] = self.color
            return dic


    def __init__(self):
        super(Column2DChart, self).__init__()

        """ 柱状图特有的属性 """
        self.labels = []
        self.type = CHART_TYPE_COLUMN_2D


    def addData(self, data):
        """
        设置数据, 可以设置多条, 可以直接调这个接口,
        :param data: 数据obj
        """
        if data == None or not isinstance(data, self.columnData):
            ''' 如果不是指定的对象, 直接返回 '''
            return

        self.data.append(data)


    def setLabels(self, labels=[]):
        """
        设置label
        :param labels:
        :return:
        """
        self.labels = labels


    def toDic_json(self):
        """
        重写todic
        :return:
        """
        dic = super(Column2DChart, self).toDic_json()
        if self.labels:
            ''' 下发labels '''
            dic['labels'] = self.labels

        return dic


    def toDic_data(self):
        """
        下发数据给客户端
        :return:
        """
        return [d.toDic() for d in self.data if d]


class Pie3DChart(Pie2DChart):
    def __init__(self):
        super(Pie3DChart, self).__init__()

        """ 3D饼图有的属性 """
        self.type = CHART_TYPE_PIE_3D


class Column3DChart(Column2DChart):
    def __init__(self):
        super(Column3DChart, self).__init__()

        """ 3D柱状图特有的属性 """
        self.type = CHART_TYPE_COLUMN_3D

# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1414406386.496681
_enable_loop = True
_template_filename = u'/Users/lamter/workspace/OpenSource/web.py-skeleton/skeleton/www/app/views/_base.html'
_template_uri = u'_base.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        title = context.get('title', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html>\n<html dir="ltr" lang="en">\n<head>\n  <meta charset="utf-8">\n  <title>')
        # SOURCE LINE 5
        __M_writer(filters.decode.utf8(title))
        __M_writer(u'</title>\n  <link rel="stylesheet" href="/static/css/style.css" />\n</head>\n<body>\n\n<nav></nav>\n\n<header></header>\n\n<section>')
        # SOURCE LINE 14
        __M_writer(filters.decode.utf8(self.container()))
        __M_writer(u'</section>\n\n<footer></footer>\n\n</body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()



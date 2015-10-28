#encoding:utf-8
__author__ = 'binpo'

import math


class Paginator():
    """
        系统查询分页工具
    """
    def __init__(self, url_func, page=1, total=0, page_size=50):

        self.url_func = url_func
        self.page = 1 if int(page) < 1 else int(page)
        self.total = int(total)
        self.page_size = int(page_size)
        self.page_num = (self.total%self.page_size==0) and self.total/self.page_size or int(math.ceil(self.total / self.page_size))+1
        self.page_bars = {}
        self.page_start=self.page*page_size
        self.page_end=self.page_start+page_size
        self.data = ()
        for _page in range(1, self.page_num + 1):
            _index = int(_page / 10)
            if not self.page_bars.has_key(_index):
                self.page_bars[_index] = {_page}
            else:
                self.page_bars[_index].add(_page)
        print self.page_num

    def render(self,form_id=None,paras=None):
        '''
        动态输出html内容
        '''
        page_bar = self.page_bars.get(int(self.page / 10))
        if page_bar is None:
            return ''

        _htmls = []
        if form_id:
            _htmls.append('''<script>
                function goto_page(form_id,page){
                    var form=document.getElementById(form_id);
                    var page_input = document.createElement("input");
                    page_input.type="hidden";
                    page_input.name="page";
                    page_input.value=page;
                    form.appendChild(page_input);
                    form.submit();
                }</script>''')
        _htmls.append('<ul class="pagination pull-right">')
        _htmls.append('\t<li class="disabled"><a >查询记录数 %s</a></li>' % self.total)
        current_start = self.page
        if current_start == 1:
            _htmls.append('\t<li class="disabled"><a >首页</a></li>')
            _htmls.append('\t<li class="disabled"><a >&larr; 上一页</a></li>')
        else:
            _htmls.append('\t<li><a href="%s">首页</a></li>' % self.url_func(1,form_id))
            _htmls.append('\t<li><a href="%s">&larr; 上一页</a></li>' % self.url_func(current_start - 1,form_id))

        for page in page_bar:
            _page_url = self.url_func(page,form_id)
            if page == self.page:
                _htmls.append('\t<li class="active"><span>%s <span class="sr-only">{current}</span></span></li>' % page)
            else:
                _htmls.append('\t<li><a href="%s">%s</a></li>' % (_page_url, page))

        current_end = self.page
        if current_end == self.page_num:
            _htmls.append('\t<li class="disabled"><a >下一页 &rarr;</a></li>')
            _htmls.append('\t<li class="disabled"><a >尾页</a></li>')
        else:
            _htmls.append('\t<li><a href="%s">下一页 &rarr;</a></li>' % self.url_func(current_end + 1,form_id))
            _htmls.append('\t<li><a href="%s">尾页</a></li>' % self.url_func(self.page_num,form_id))

        _htmls.append('</ul>')

        return '\r\n'.join(_htmls)

    def render_user_html(self,form_id=None):

        page_bar = self.page_bars.get(int(self.page / 10))
        if page_bar is None:
            return ''

        _htmls = []
        if form_id:
            _htmls.append('''<script>
                function goto_page(form_id,page){
                    var form=document.getElementById(form_id);
                    var page_input = document.createElement("input");
                    page_input.type="hidden";
                    page_input.name="page";
                    page_input.value=page;
                    form.appendChild(page_input);
                    form.submit();
                }</script>''')


        _htmls.append('\t<div class="row"><div class="col-md-12"><div class="bg-white clearfix pad10A"><div class="button-group mrg0A float-right">')

        current_start = self.page
        if current_start == 1:
             _htmls.append('\t<a class="btn small disabled ui-state-default" >首页</a>')
             _htmls.append('\t<a class="btn small disabled ui-state-default" ><i class="glyph-icon icon-chevron-left"></i></a>')
        else:
             _htmls.append('\t<a class="btn small ui-state-default" href="%s">首页</a>'% self.url_func(1,form_id))
             _htmls.append('\t<a class="btn small ui-state-default" href="%s"><i class="glyph-icon icon-chevron-left"></i></a>' % self.url_func(current_start - 1,form_id))

        for page in page_bar:
            _page_url = self.url_func(page,form_id)
            if page == self.page:
                _htmls.append('\t<a class="btn small disabled ui-state-default" >%s</a>' % page)
            else:
                _htmls.append('\t<a class="btn small ui-state-default" href="%s">%s</a>' % (_page_url, page))

        current_end = self.page
        if current_end == self.page_num:
            _htmls.append('\t<a class="btn small ui-state-default disabled" > <i class="glyph-icon icon-chevron-right"></i></a>')
            _htmls.append('\t<a class="btn small ui-state-default disabled" href="#">尾页</a>')
        else:
            _htmls.append('\t<a class="btn small ui-state-default" href="%s"> <i class="glyph-icon icon-chevron-right"></i></a>' % self.url_func(current_end + 1,form_id))
            _htmls.append('\t<a class="btn small ui-state-default" href="%s">尾页</a>' % self.url_func(self.page_num,form_id))

        _htmls.append('</div></div></div></div>')

        return '\r\n'.join(_htmls)

    def render_page_html(self,form_id=None,params={}):
        page_bar = self.page_bars.get(int(self.page / 10))
        if page_bar is None:
            return ''
        _htmls = []
        if form_id:
            _htmls.append('''<script>
                function goto_page(form_id,page){
                    var form=document.getElementById(form_id);
                    var page_input = document.createElement("input");
                    page_input.type="hidden";
                    page_input.name="page";
                    page_input.value=page;
                    form.appendChild(page_input);
                    form.submit();
                }</script>''')


        _htmls.append('\t<div class="row"><div class="col-md-12"><div class="bg-white clearfix pad10A"><div class="button-group mrg0A float-right">')
        every_pages=[4,5,10,15,20,30,40,50,100,200,500]

        _htmls.append('\t<tfoot><form action="" method="get"><tr><td colspan="12"><div style="float:right; clear:none;" class="page form-inline">共 <strong>%s</strong> 条记录，每页'%(self.total))
        options = ''.join([self.page_size==p and  '<option value="'+str(p)+'" selected="selected">'+str(p)+'</option>' or '<option value="'+str(p)+'">'+str(p)+'</option>'  for p in every_pages])
        _htmls.append('\t<strong><select name="page_size" id="page_size" class="w-60px">')
        _htmls.append(options)
        _htmls.append('\t</select>')
        _htmls.append('\t</strong> 条，页面：<strong>%s/%s</strong>'%(self.page,self.page_num))
        current_start = self.page
        if current_start == 1:
             _htmls.append('\t<a class="disabled" >首页</a>')
             _htmls.append('\t<a class="disabled" ><i class="glyph-icon icon-chevron-left"></i></a>')
        else:
             _htmls.append('\t<a href="%s">首页</a>'% self.url_func(1,form_id))
             _htmls.append('\t<a href="%s"><i class="glyph-icon icon-chevron-left"></i></a>' % self.url_func(current_start - 1,form_id))

        for page in page_bar:
            _page_url = self.url_func(page,form_id)
            if page == self.page:
                _htmls.append('\t<a class="disabled" >%s</a>' % page)
            else:
                _htmls.append('\t<a href="%s">%s</a>' % (_page_url, page))

        current_end = self.page
        if current_end == self.page_num:
            _htmls.append('\t<a class="disabled" > <i class="glyph-icon icon-chevron-right"></i></a>')
            _htmls.append('\t<a class="disabled" href="#">尾页</a>')
        else:
            _htmls.append('\t<a  href="%s"> <i class="glyph-icon icon-chevron-right"></i></a>' % self.url_func(current_end + 1,form_id))
            _htmls.append('\t<a href="%s">尾页</a>' % self.url_func(self.page_num,form_id))

        _htmls.append('<input type="text" id="page" value="%s" style="text-align:center;width:30px;">'%(str(self.page)))
        for key in params.keys():
            _htmls.append('<input type="hidden" value="'+params.get(key)+'"  name="'+key+'">')
        _htmls.append('<input type="submit" id="goto" value="Go!"  class="btn btn-default btn-xs">')

        _htmls.append('</div></td></tr></form></tfoot>')

        return '\r\n'.join(_htmls)

    """
    首页 上页 下页 末页
                        <input type="hidden" id="_recTotal" value="2">
                        <input type="hidden" id="_pageTotal" value="1">
                        <input type="text" id="_pageID" value="1" style="text-align:center;width:30px;">
                        <input type="button" id="goto" value="Go!" onclick="submitPage(&quot;changePageID&quot;);" class="btn btn-default btn-xs">
                    </div>
                </td>
            </tr>
        </tfoot>
    """
    def render_admin_html(self,form_id=None,params={}):
        return self.render_page_html()

    def render_admin_html2(self,form_id=None,params={}):
        page_bar = self.page_bars.get(int(self.page / 10))
        if page_bar is None:
            return ''

        _htmls = []
        _htmls.append('\t<div class="paginate clearfix">')
        #首页
        if self.page == 1:
            _htmls.append('\t<a class="btn-home border-box fl" href="#"><span class="icon-home"></span>首页</a>')
        else:
            _htmls.append('\t<a class="btn-home border-box fl" href="%s"><span class="icon-home"></span>首页</a>' % self.url_func(1,form_id))
        #尾页
        if self.page == self.page_num:
            _htmls.append('\t<a class="btn-last border-box fl" href="#"><span class="icon-last"></span>尾页</a>')
        else:
            _htmls.append('\t<a class="btn-last border-box fl" href="%s"><span class="icon-last"></span>尾页</a>' % self.url_func(self.page_num,form_id))
        #上一页
        if self.page == 1:
            _htmls.append('\t<a class="btn-prev border-box fl" href="#"><span class="icon-prev"></span></a>')
        else:
            _htmls.append('\t<a class="btn-prev border-box fl" href="%s"><span class="icon-prev"></span></a>' % self.url_func(self.page - 1,form_id))
        #下一页
        if self.page + 1 <= self.page_num:
            _htmls.append('\t<a class="btn-next border-box fl" href="%s"><span class="icon-next"></span></a>' % self.url_func(self.page + 1,form_id))
        else:
            _htmls.append('\t<a class="btn-next border-box fl" href="#"><span class="icon-next"></span></a>')
        _htmls.append('\t</div>')

        return '\r\n'.join(_htmls)

    def render_admin_html_web(self,form_id=None,params={}):
        _htmls = []
        if self.page == 1:
            _htmls.append('\t<li class="arrow"><span>上一页</span></li>')
        else:
            _htmls.append('\t<li class="arrow"><a href="%s">上一页</a></li>' % self.url_func(self.page-1,form_id))
        if self.page_num >= 9:
            if self.page >= 5:
                if self.page_num - self.page >= 4:
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(1,form_id),1))
                    _htmls.append('\t<li><span>&hellip;</span></li>')
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page-2,form_id),self.page-2))
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page-1,form_id),self.page-1))
                    _htmls.append('\t<li class="gzh-active"><span>%s</span></li>' % self.page)
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page+1,form_id),self.page+1))
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page+2,form_id),self.page+2))
                    _htmls.append('\t<li><span>&hellip;</span></li>')
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page_num,form_id),self.page_num))
                else:
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(1,form_id),1))
                    _htmls.append('\t<li><span>&hellip;</span></li>')
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page-2,form_id),self.page-2))
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page-1,form_id),self.page-1))
                    _htmls.append('\t<li class="gzh-active"><span>%s</span></li>' % self.page)
                    for page_num in range(self.page_num - self.page):
                        _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page+(page_num+1),form_id),self.page+(page_num+1)))
            else:
                for page_num in range(self.page-1):
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(page_num+1,form_id),page_num+1))
                _htmls.append('\t<li class="gzh-active"><span>%s</span></li>' % self.page)
                _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page+1,form_id),self.page+1))
                _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page+2,form_id),self.page+2))
                _htmls.append('\t<li><span>&hellip;</span></li>')
                _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page_num,form_id),self.page_num))
        else:
            for page_num in range(self.page_num):
                if self.page == int(page_num+1):
                    _htmls.append('\t<li class="gzh-active"><span>%s</span></li>' % int(page_num+1))
                else:
                    _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(page_num+1,form_id),int(page_num+1)))
        if self.page == self.page_num:
            _htmls.append('\t<li class="arrow"><span>下一页</span></li>')
        else:
            _htmls.append('\t<li class="arrow"><a href="%s">下一页</a></li>' % self.url_func(self.page+1,form_id))
        return '\r\n'.join(_htmls)


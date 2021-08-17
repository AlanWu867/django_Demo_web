from django.shortcuts import render
from django.shortcuts import HttpResponse
import json
from . import models
from django.core.paginator import Paginator
import math
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

def home(request):
    if request.method == "POST":
        username = request.POST.get("user")
        password = request.POST.get("pwd")
        ret = {"status": 0, 'url': ''}
        if username=='Alan' and password=='123456':
            ret['status'] = 1
            ret['url'] = '/home/Inquire/'
        return HttpResponse(json.dumps(ret))

    return render(request, "home.html")

def Inquire(request):
    if request.method == "POST":
        SourceIP = request.POST.get('SourceIP')
        models.search('SourceIP',SourceIP,1)
        ret = {"status": 1, 'url': '/home/Inquire/?page=1&SourceIP=%s'%SourceIP}
        return HttpResponse(json.dumps(ret))
    else:
        page = request.GET.get('page')
        SourceIP = request.GET.get('SourceIP')
        page = 1 if page == None else page
        SourceIP=None if SourceIP=="" else SourceIP
        try:
            topics=models.search('SourceIP', SourceIP,page)
            val_count=models.val_count('SourceIP', SourceIP)
        except:
            topics=models.search(None, None,page)
            val_count = models.val_count(None, None)
    limit = 50  # 每页显示的记录数
    all_page=math.ceil(val_count/limit)
    page_obj  = Paginator(topics, limit)
    pagerange1=[]
    # try:
    page_obj  = page_obj.page(1)
    object_list = page_obj.object_list
    pagerange = range(1, 6)
    has_other_pages = 1 if topics!=[] else 0
    has_next = 1 if 1< int(page)+1 < all_page else 0

    has_previous=1 if 0<int(page)-1 < all_page else 0
    if all_page-2>int(page)>3:
        pagerange = range(int(page)-2, int(page)+3)
    elif int(page)>=all_page-2:
        pagerange = range(all_page-4, all_page+1)
    previous_page_number=int(page)-1 if has_previous==1 else None
    next_page_number = int(page)+1 if has_next == 1 else None
    previous_page_number = str(previous_page_number) + "&SourceIP=%s" % SourceIP
    next_page_number = str(next_page_number) + "&SourceIP=%s" % SourceIP
    if SourceIP != None:
        for i in pagerange:
            pagerange1.append({'page':i,'SourceIP':SourceIP})
        pagerange=pagerange1

    else:
        for i in pagerange:
            pagerange1.append({'page': i, 'SourceIP': ""})
        pagerange =pagerange1
    # except PageNotAnInteger:  # 如果页码不是个整数
    #     page=1
    #     page_obj  = page_obj.page(1)  # 取第一页的记录
    #     object_list=page_obj.object_list
    #     has_other_pages=1 if page_obj.has_other_pages else 0
    #     has_next = 1 if page_obj.has_next() else 0
    #     has_previous=1 if page_obj.has_previous() else 0
    #     previous_page_number = page_obj.previous_page_number() if has_previous == 1 else None
    #     next_page_number = page_obj.next_page_number() if has_next == 1 else None
    #     pagerange = range(1, 6)
    #     if SourceIP != None:
    #         for i in pagerange:
    #             pagerange1.append({'page':i,'SourceIP':SourceIP})
    #         pagerange=pagerange1
    #         previous_page_number=str(previous_page_number)+"&SourceIP=%s"%SourceIP
    #         next_page_number = str(next_page_number) + "&SourceIP=%s" % SourceIP
    #     else:
    #         for i in pagerange:
    #             pagerange1.append({'page': i, 'SourceIP': ""})
    #         pagerange = pagerange1
    # except EmptyPage:  # 如果页码太大，没有相应的记录
    #     page_obj  = page_obj.page(page_obj .num_pages)  # 取最后一页的记录
    # print(pagerange[0])
    return render(request,'Inquire.html', {'page_obj ': page_obj, 'pagerange':pagerange,
                                           'has_other_pages':has_other_pages,'has_next':has_next,
                                           'has_previous':has_previous,'page':int(page),'next_page_number':next_page_number,
                                           'previous_page_number':previous_page_number,'object_list':object_list})
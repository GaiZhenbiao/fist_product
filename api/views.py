from fileinput import filename
from django.shortcuts import render
from django.http import HttpResponse
from numpy import average
from py import process
from .models import *
import traceback

import json, os, time
from io import BytesIO
import zipfile

def zip_files(files):
    outfile = BytesIO()  # io.BytesIO() for python 3
    with zipfile.ZipFile(outfile, 'w') as zf:
        for idx, f in enumerate(files):
            zf.writestr("compressed.zip",f)
    return outfile.getvalue()

def handle_uploaded_file(file):
    with open(f'files/{file.name}', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def handle_login(request):
    context = {"message": "未知错误", "status": 1}
    username = request.POST.get("username")
    passwd = request.POST.get("password")
    two_FA = request.POST.get("2fa")
    try:
        context["message"] = "没有该用户"
        user = User.objects.get(name=username)
        context["message"] = "密码或两步验证码错误"
        token = user.get_token(passwd, two_FA)
        assert token is not None
        context["token"] = token
        context["is_admin"] = user.is_admin
        context["username"] = username
        context["id"] = user.id
        context["message"] = "登录成功"
        context["status"] = 0
    except:
        pass
    return HttpResponse(json.dumps(context))

def handle_get_commented(request):
    context = {"message": "未知错误", "status": 1}
    try:
        token = request.POST.get("token")
        context["message"] = "没有该用户"
        user = User.objects.get(token=token)
        context["commented"] = user.get_commented()
        context["message"] = "查询成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_is_commented(request):
    context = {"message": "未知错误", "status": 1}
    try:
        token = request.POST.get("token")
        context["message"] = "没有该用户"
        user = User.objects.get(token=token)
        commented = user.get_commented()
        procedure = FistProcedure.objects.get(id=request.POST.get("procedure_id"))
        if procedure in commented:
            context["message"] = "已经评论过了"
            context["flag"] = 0
        else:
            context["message"] = "没有评论过"
            context["flag"] = 1
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_find_product(request):
    context = {"message": "未知错误", "status": 1}
    id = int(request.POST.get("id"))
    try:
        context["message"] = "没有该商品"
        product = Product.objects.get(pk=id)
        context["message"] = "查询成功"
        context["status"] = 0
        context["product"] = product.to_dict()
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_modify_product(request):
    context = {"message": "未知错误", "status": 1}
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    category = request.POST.get("category")
    stock = request.POST.get("stock")
    sold = request.POST.get("sold")
    user = request.POST.get("token")
    try:
        context["message"] = "没有该商品"
        id = request.POST.get("id")
        context["message"] = "找不到用户"
        user = User.objects.get(token=user)
        if id:
            product = Product.objects.get(pk=int(id))
            context["message"] = "修改成功"
        else:
            product = Product()
            context["message"] = "创建成功"
        product.name = name
        product.price = price
        product.description = description
        product.category = category
        product.stock = stock
        product.sold = sold
        product.save()
        context["id"] = product.id
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_get_all_products(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有商品"
        products = Product.objects.all()
        context["message"] = "查询所有产品成功"
        context["status"] = 0
        context["products"] = [product.to_dict() for product in products]
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_delete_product(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有该商品"
        id = request.POST.get("id")
        product = Product.objects.get(pk=int(id))
        product.delete()
        context["message"] = "删除成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))


def handle_create_procecure(request):
    try:
        context = {"message": "未知错误", "status": 1}
        name = request.POST.get("name")
        user = request.POST.get("user")
        context["message"] = "没有该用户"
        user = User.objects.get(token=user)
        content = request.POST.get("content")
        product = int(request.POST.get("product"))
        context["message"] = "没有该商品"
        product = Product.objects.get(pk=product)
        procedure = FistProcedure(name=name, user=user, content=content, product=product)
        context["message"] = "保存失败"
        procedure.save()
        context["id"] = procedure.id
        context["message"] = "创建成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_like_procedure(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有该工序"
        procedure = int(request.POST.get("procedure"))
        procedure = FistProcedure.objects.get(pk=procedure)
        context["message"] = "没有该用户"
        user = request.POST.get("token")
        user = User.objects.get(token=user)
        context["message"] = "加入评审团/退出评审团时失败"
        procedure.alter_like(user)
        context["likes"] = procedure.likes
        procedure.save()
        context["message"] = "成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_find_procedure(request):
    context = {"message": "未知错误", "status": 1}
    id = int(request.POST.get("id"))
    try:
        context["message"] = "没有该工序"
        procedure = FistProcedure.objects.get(pk=id)
        context["message"] = "查询成功"
        context["status"] = 0
        context["procedure"] = procedure.to_dict()
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_get_all_procedures(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有工序"
        procedures = FistProcedure.objects.all()
        context["message"] = "查询所有工序成功"
        context["status"] = 0
        context["procedures"] = [procedure.to_dict() for procedure in procedures]
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_upload(request):
    context = {"message": "上传失败TAT"}
    try:
        print(request.FILES)
        context["message"] = "没有文件"
        file = request.FILES["file"]
        context["message"] = "找不到用户"
        user = request.POST.get("token")
        user = User.objects.get(token=user)
        context["message"] = "没有指定名称"
        name = request.POST.get("name")
        procedure = int(request.POST.get("procedure"))
        procedure = FistProcedure.objects.get(pk=procedure)
        context["message"] = "保存失败"
        if request.method == 'POST':
            record = UserUploadedFile(
                name=name, file=f"files/{file.name}", procedure=procedure, user=user)
            record.save()
            handle_uploaded_file(file)
            context['message'] = "上传成功^_^"
        else:
            context['message'] = "上传失败TAT（奇怪的错误增加了！）"
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_goto_stage(request):
    context = {"message": "未知错误", "status": 1}
    id = int(request.POST.get("id"))
    stage = request.POST.get("stage")
    try:
        context["message"] = "没有该工序"
        procedure = FistProcedure.objects.get(pk=id)
        context["message"] = "跳转成功"
        procedure.stage = int(stage)
        context["stage"] = int(stage)
        context["status"] = 0
        procedure.save()
        context["procedure"] = procedure.to_dict()
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_comment_procedure(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有该流程"
        procedure = int(request.POST.get("procedure"))
        procedure = FistProcedure.objects.get(pk=procedure)
        context = procedure.comment(request.POST)
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))


def handle_finish_procedure(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有该流程"
        procedure = int(request.POST.get("id"))
        procedure = FistProcedure.objects.get(pk=procedure)
        procedure.finished = True
        context["message"] = "没说是不是拳头产品"
        fist = request.POST.get("fist")
        procedure.product.fist = bool(fist)
        procedure.product.save()
        procedure.save()
        context["message"] = "完成成功"
        context["status"] = 0
        context["procedure"] = procedure.to_dict()
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_cancel_fist(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有该产品"
        product = int(request.POST.get("id"))
        product = Product.objects.get(pk=product)
        context["message"] = "取消失败"
        product.fist = False
        product.save()
        context["message"] = "取消成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_set_as_approved(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有该流程"
        procedure = int(request.POST.get("id"))
        procedure = FistProcedure.objects.get(pk=procedure)
        procedure.approved = True
        procedure.save()
        context["message"] = "设置成功"
        context["status"] = 0
        context["procedure"] = procedure.to_dict()
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_schedule_meeting(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有该审批流程"
        procedure = int(request.POST.get("id"))
        procedure = FistProcedure.objects.get(pk=procedure)
        context["message"] = "没有 location 信息"
        location = request.POST.get("location")
        context["message"] = "没有 start_time 信息"
        start_time = request.POST.get("start_time")
        context["message"] = "没有 end_time 信息"
        end_time = request.POST.get("end_time")
        procedure.meeting_location = location
        procedure.meeting_start_time = start_time
        procedure.meeting_end_time = end_time
        procedure.save()
        context["message"] = "安排会议成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_add_news(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有填写标题"
        title = request.POST.get("title")
        context["message"] = "没有填写内容"
        content = request.POST.get("content")
        context["message"] = "没有填写链接"
        link = request.POST.get("link")
        context["message"] = "没有该产品"
        product = int(request.POST.get("product"))
        product = Product.objects.get(pk=product)
        context["message"] = "没有该用户"
        token = request.POST.get("token")
        author = User.objects.get(token=token)
        news = News(title=title, content=content, product=product, author=author)
        news.save()
        context["id"] = news.id
        context["message"] = "添加成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_delete_news(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有该新闻"
        news = int(request.POST.get("id"))
        news = News.objects.get(pk=news)
        news.delete()
        context["message"] = "删除成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_modify_graph(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有填写标题"
        title = request.POST.get("title")
        context["message"] = "没有填写 xs 信息"
        xs = request.POST.get("xs")
        context["message"] = "没有填写 ys 信息"
        ys = request.POST.get("ys")
        context["message"] = "没有填写 type 信息"
        type = request.POST.get("type")
        context["message"] = "没有填写 product 信息"
        product = int(request.POST.get("product"))
        product = Product.objects.get(pk=product)
        if request.POST.get("id"):
            graph = int(request.POST.get("id"))
            graph = Graph.objects.get(pk=graph)
            graph.title = title
            graph.xs = xs
            graph.ys = ys
            graph.type = type
            graph.product = product
        else:
            graph = Graph(title=title, xs=xs, ys=ys, type=type, product=product)
        graph.save()
        context["message"] = "添加成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_delete_graph(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有该图表"
        graph = int(request.POST.get("id"))
        graph = Graph.objects.get(pk=graph)
        graph.delete()
        context["message"] = "删除成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))\

def handle_calculate_grade(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "流程不存在"
        procedure = int(request.POST.get("id"))
        procedure = FistProcedure.objects.get(pk=procedure)
        context["message"] = "评委数量不足"
        likers = procedure.likers.split(",")
        likers = [int(i) for i in likers]
        likers = User.objects.filter(pk__in=likers)
        assert len(likers) >= 5
        context["message"] = "评委们没有都给出评分"
        assert len(likers) == procedure.likes
        context["message"] = "寻找评论时出错"
        comments = Comment.objects.filter(user__in=likers)
        context["message"] = "计算得分时出错"
        avg_grade = 0
        for comment in comments:
            avg_grade += comment.grade * comment.user.weight
        avg_grade /= procedure.likes
        avg_grade = min(avg_grade, 10)
        avg_grade *= 10
        product = procedure.product
        if avg_grade >= 60:
            product.fist = True
        else:
            product.fist = False
        product.grade = avg_grade
        product.save()
        context["grade"] = avg_grade
        context["message"] = "计算得分成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

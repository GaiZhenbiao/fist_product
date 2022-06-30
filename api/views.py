from fileinput import filename
from django.shortcuts import render
from django.http import HttpResponse
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
        context["message"] = "登录成功"
        context["status"] = 0
    except:
        pass
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
    try:
        context["message"] = "没有该商品"
        try:
            product = Product.objects.get(name=name)
            context["mode"] = "modify"
        except:
            product = Product(name=name)
            context["mode"] = "create"
        product.price = price
        product.description = description
        product.category = category
        product.stock = stock
        product.sold = sold
        product.save()
        context["id"] = product.id
        context["message"] = "修改成功"
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
    id = request.POST.get("id")
    try:
        context["message"] = "没有该商品"
        product = Product.objects.get(pk=id)
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
        user = User.objects.get(name=user)
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
        context["message"] = "点赞/取消赞时失败"
        procedure.alter_like(user)
        context["likes"] = procedure.likes
        procedure.save()
        context["message"] = "点赞成功"
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
        title = request.POST.get("title")
        content = request.POST.get("content")
        agree = request.POST.get("agree")
        context["message"] = "非布尔型"
        agree = bool(agree)
        context["message"] = "没有该用户"
        user = request.POST.get("token")
        user = User.objects.get(token=user)
        context["message"] = "评论创建失败"
        comment = Comment(title=title, content=content, agree=agree, user=user, procedure=procedure)
        comment.save()
        context["message"] = "评论成功"
        context["status"] = 0
        procedure.save()
        context["procedure"] = procedure.to_dict()
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))


def handle_finish_procedure(request):
    context = {"message": "未知错误", "status": 1}
    fist = request.POST.get("fist")
    try:
        context["message"] = "没有该流程"
        procedure = int(request.POST.get("id"))
        procedure = FistProcedure.objects.get(pk=procedure)
        procedure.finished = True
        procedure.product.fist = bool(fist)
        procedure.product.save()
        procedure.save()
        context["message"] = "完成成功"
        context["status"] = 0
        context["procedure"] = procedure.to_dict()
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
        procedure.location = location
        procedure.start_time = start_time
        procedure.end_time = end_time
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

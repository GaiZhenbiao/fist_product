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
    with open(f'sources/{file.name}', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def handle_upload(request):
    context = {"message": "上传失败TAT"}
    print(request.FILES)
    file = request.FILES["file"]
    user = request.POST.get("user")
    user = User.objects.get(name=user)
    procedure = request.POST.get("procedure")
    procedure = FistProcedure.objects.get(name=procedure)
    if request.method == 'POST':
        record = UserUploadedFile(
            name=file.name, file=f"files/{file.name}", procedure=procedure, user=user)
        record.save()
        handle_uploaded_file(file)
        context['message'] = "上传成功^_^"
    return HttpResponse(json.dumps(context))

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
    name = request.POST.get("name")
    try:
        context["message"] = "没有该商品"
        product = Product.objects.get(name=name)
        context["message"] = "查询成功"
        context["status"] = 0
        context["product"] = product.to_dict()
    except:
        print(traceback.format_exc())
    print(context)
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
        except:
            product = Product(name=name)
        product.price = price
        product.description = description
        product.category = category
        product.stock = stock
        product.sold = sold
        product.save()
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
    name = request.POST.get("name")
    try:
        context["message"] = "没有该商品"
        product = Product.objects.get(name=name)
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
        product = request.POST.get("product")
        context["message"] = "没有该商品"
        product = Product.objects.get(name=product)
        procedure = FistProcedure(name=name, user=user, content=content, product=product)
        context["message"] = "保存失败"
        procedure.save()
        context["message"] = "创建成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_like_procedure(request):
    context = {"message": "未知错误", "status": 1}
    name = request.POST.get("name")
    try:
        context["message"] = "没有该工序"
        procedure = FistProcedure.objects.get(name=name)
        procedure.likes += 1
        procedure.save()
        context["message"] = "点赞成功"
        context["status"] = 0
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

def handle_find_procedure(request):
    context = {"message": "未知错误", "status": 1}
    name = request.POST.get("name")
    try:
        context["message"] = "没有该工序"
        procedure = FistProcedure.objects.get(name=name)
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

def handle_goto_stage(request):
    context = {"message": "未知错误", "status": 1}
    name = request.POST.get("name")
    stage = request.POST.get("stage")
    try:
        context["message"] = "没有该工序"
        procedure = FistProcedure.objects.get(name=name)
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
        procedure = request.POST.get("name")
        context["message"] = "没有该流程"
        procedure = FistProcedure.objects.get(name=procedure)
        title = request.POST.get("title")
        content = request.POST.get("content")
        agree = request.POST.get("agree")
        context["message"] = "非布尔型"
        agree = bool(agree)
        user = request.POST.get("user")
        context["message"] = "没有该用户"
        user = User.objects.get(name=user)
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
        procedure = request.POST.get("name")
        context["message"] = "没有该流程"
        procedure = FistProcedure.objects.get(name=procedure)
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

def handle_schedule_meeting(request):
    context = {"message": "未知错误", "status": 1}
    try:
        context["message"] = "没有该审批流程"
        procedure = request.POST.get("procedure")
        procedure = FistProcedure.objects.get(name=procedure)
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
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(context))

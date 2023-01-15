from datetime import *
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from myappSuper.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from celery import Celery
from celery.schedules import crontab
from django.db.models import Q
from django.contrib import messages
from django.core.management import call_command
import json as simplejson
from django.http import HttpResponse


def call(req):
    nested_data = call_command('dumpdata', 'myappstaff', '--output=myapp.json')
    print(nested_data)
    return HttpResponse(
    simplejson.dumps(nested_data), 
    content_type='application/force-download'
)



@login_required
def admin_detail(req, id):
    if req.user.right != "ผู้ดูแลระบบ":
        return redirect('/') 
    AllUser = User.objects.filter(id=id).first()
    context = {
        "AllUser" : AllUser,
    }
    return render(req, "pages/admin_detail.html", context)

@login_required
def admin_addemail(req):
    if req.user.right != "ผู้ดูแลระบบ":
        return redirect('/') 
    if req.method == "POST":
        emailuser = req.POST.get("emailuser")
        obj = EmailUser(emailuser=emailuser)
        obj.save()
        messages.success(req, 'เพิ่มผู้ใช้งานสำเร็จ!')
        return redirect('/admin_addemail')   
    else:
        messages.success(req, 'เพิ่มผู้ใช้งานไม่สำเร็จ!')
        obj = EmailUser()   
    obj = EmailUser.objects.all()   
    AllEmailUser = EmailUser.objects.all()
    page_num = req.GET.get('page', 1)
    p = Paginator(AllEmailUser, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)        
    context = {
        "navbar" : "admin_addemail",
        "AllEmailUser" : EmailUser.objects.all(),
        "page" : page,
    }
    return render(req, "pages/admin_addemail.html", context)

@login_required
def admin_user_setting_detail(req, id):
    if req.user.right != "ผู้ดูแลระบบ":
        return redirect('/') 
    context = {
        "navbar" : "admin_user_setting_detail",
        "AllUser" : AllUser,
    }
    AllUser = User.objects.filter(id=id).first()
    return render(req, "pages/admin_user_setting_detail.html", context)

@login_required
def delete_user(req, id):
    if req.user.right != "ผู้ดูแลระบบ":
        return redirect('/') 
    obj = User.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบผู้ใช้สำเร็จ!')
    return redirect('/admin_user')

@login_required
def admin_user_status(req,id):
    if req.user.right != "ผู้ดูแลระบบ":
        return redirect('/') 
    obj = User.objects.get(id=id)
    obj.right = req.POST['right']
    obj.save()
    messages.success(req, 'เปลี่ยนสถานะสำเร็จ!')
    return redirect('/admin_user') 

@login_required
def admin_user_deadline(req, id):
    if req.user.right != "ผู้ดูแลระบบ":
        return redirect('/') 
    obj = User.objects.get(id=id)
    if datetime.now() > obj.deadline:
        obj.status = "Normal"
    else:
        obj.status = req.POST['status']
    obj.reason = req.POST['reason']
    deadline_str = req.POST['deadline']
    if deadline_str == '':
        obj.deadline = datetime.now() + timedelta(days=7)
    else:
        obj.deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
    obj.save()
    messages.success(req, 'จำกัดสิทธิ์สำเร็จ!')
    return redirect('/admin_block') 

@login_required
def admin_user(req):
    if req.user.right != "ผู้ดูแลระบบ":
        return redirect('/') 
    #gg_id = User.objects.filter(user=req.user, provider='google')[0].uid
    AllUserStudent = User.objects.filter(Q(right = "นักศึกษา") | Q(status = "ปกติ"))
    AllUserStudent_count = User.objects.filter(right = "นักศึกษา", status = "ปกติ") #count การแนะนำ
    context = {
        "navbar" : "admin_user",
        "AllUserStudent" : AllUserStudent,
        "AllUserStudent_count" :  AllUserStudent_count,
    }
    return render(req, "pages/admin_user.html", context)

@login_required
def admin_staff(req):
    if req.user.right != "ผู้ดูแลระบบ":
        return redirect('/') 
    AllUserStaff = User.objects.filter(Q(right = "เจ้าหน้าที่")  | Q(right = "ผู้ดูแลระบบ")  | Q(status = "ปกติ"))
    AllUser_count = User.objects.filter(right = "เจ้าหน้าที่", status = "ปกติ")
    AllUser_count_admin = User.objects.filter(right = "ผู้ดูแลระบบ", status = "ปกติ")
    context = {
        "navbar" : "admin_staff",
        "AllUserStaff" : AllUserStaff,
        "AllUserStaff_count" : AllUser_count,
        "AllUser_count_admin" : AllUser_count_admin,
    }
    return render(req, "pages/admin_staff.html", context)

@login_required
def admin_block(req):
    if req.user.right != "ผู้ดูแลระบบ":
        return redirect('/') 
    AllUser = User.objects.filter(status = "ถูกจำกัดสิทธิ์")
    AllUser_count = User.objects.filter(status = "ถูกจำกัดสิทธิ์")
    context = {
        "navbar" : "admin_block",
        "AllUser" : AllUser,
        "AllUser_count" : AllUser_count,
    }
    return render(req, "pages/admin_block.html", context)

@login_required
def admin_notifications(req):
    if req.user.right != "ผู้ดูแลระบบ":
        return redirect('/') 
    return render(req, "pages/admin_notifications.html")

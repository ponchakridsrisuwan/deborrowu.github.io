from datetime import *
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.contrib.auth.decorators import login_required
from myappstaff.forms import *
from django.utils import timezone
from django.core.paginator import Paginator
from myappstaff.models import *
from myapp.models import *
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.db.models import Max
from django.contrib import messages


@login_required
def staff_notifications(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    return render(req, "pages/staff_notifications.html")

def staff_setting_position(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    if req.method == "POST":
        nameposition = req.POST.get('nameposition')
        obj = SettingPosition(nameposition=nameposition)
        obj.save()
        messages.success(req, 'เพิ่มชั้นวางสำเร็จ!')
        return redirect('/staff_setting_position')   
    else:
        messages.success(req, 'เพิ่มชั้นวางไม่สำเร็จ!')
        obj = SettingPosition()   
    obj = SettingPosition.objects.all()   
    AllPosition = SettingPosition.objects.all()
    page_num = req.GET.get('page', 1)
    p = Paginator(AllPosition, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)        
    context = {
        "navbar" : "staff_setting_position",
        "AllSettingPosition": SettingPosition.objects.all(),
        "page" : page
    }
    return render(req, 'pages/staff_setting_position.html', context)

@login_required
def deletePosition(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    obj = SettingPosition.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบสำเร็จ!')
    return redirect('/staff_setting_position')

@login_required
def edit_position(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    obj = SettingPosition.objects.get(id=id)
    obj.nameposition = req.POST['nameposition']
    obj.save()
    messages.success(req, 'แก้ไขสำเร็จ!')
    return redirect('/staff_setting_position')


@login_required
def staff_setting(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    if req.method == "POST":
        name_CategoryType = req.POST.get('name_CategoryType')
        obj = CategoryType(name_CategoryType=name_CategoryType)
        obj.save()
        messages.success(req, 'เพิ่มหมวดหมู่สำเร็จ!')
        return redirect('/staff_setting')   
    else:
        messages.success(req, 'บันทึกไม่สำเร็จ!')
        obj = CategoryType()   
    obj = CategoryType.objects.all()   
    AllCategoryType = CategoryType.objects.all()
    page_num = req.GET.get('page', 1)
    p = Paginator(AllCategoryType, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)        
    context = {
        "navbar" : "staff_setting",
        "All_CategoryType": CategoryType.objects.all(),
        "page" : page
    }
    return render(req, 'pages/staff_setting.html', context)    

@login_required
def deleteCategoryType(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    obj = CategoryType.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบสำเร็จ!')
    return redirect('/staff_setting')

@login_required
def edit_staff_setting(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    obj = CategoryType.objects.get(id=id)
    obj.name_CategoryType = req.POST['name_CategoryType']
    obj.save()
    messages.success(req, 'แก้ไขสำเร็จ!')
    return redirect('/staff_setting')

# การตั้งค่าสถานะ
@login_required
def staff_setting_status(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    if req.method == "POST":
        name_CategoryStatus = req.POST.get('name_CategoryStatus')
        obj = CategoryStatus(name_CategoryStatus=name_CategoryStatus)
        obj.save()
        messages.success(req, 'เพิ่มสถานะสำเร็จ!')
        return redirect('/staff_setting_status')   
    else:
        messages.success(req, 'บันทึกไม่สำเร็จ!')
        obj = CategoryStatus()   
    obj = CategoryStatus.objects.all()   
    AllCategoryStatus = CategoryStatus.objects.all()
    page_num = req.GET.get('page', 1)
    p = Paginator(AllCategoryStatus, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)
    context = {
        "navbar" : "staff_setting_status",
        "All_CategoryStatus": CategoryStatus.objects.all(),
        "page" : page
    }    
    return render(req, 'pages/staff_setting_status.html', context)  

@login_required
def DeleteCategoryStatus(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    obj = CategoryStatus.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบสำเร็จ!')
    return redirect('/staff_setting_status')

@login_required
def edit_staff_setting_status(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    obj = CategoryStatus.objects.get(id=id)
    obj.name_CategoryStatus = req.POST['name_CategoryStatus']
    obj.save()
    messages.success(req, 'แก้ไขสำเร็จ!')
    return redirect('/staff_setting_status')

# การแนะนำวัสดุเข้าสู่ระบบ    
@login_required
def staff_introduction(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllRecList = ListFromRec.objects.filter(status='รออนุมัติ').order_by('name', 'datetime')
    page_num = req.GET.get('page', 1)
    p = Paginator(AllRecList, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)    
    context = {
        "navbar" : "staff_introduction",
        'page' :page,
    }            
    return render( req, 'pages/staff_introduction.html', context)

@login_required
def staff_introduction_update(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllRecList = ListFromRec.objects.filter(id=id).first()
    AllRecList.status = 'อนุมัติ'
    AllRecList.save()
    messages.success(req, 'อนุมัติสำเร็จ!')
    context = {
        "AllRecList" : AllRecList,
    }
    return redirect('/staff_introduction', context)

@login_required
def staff_introduction_history(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllRecList = ListFromRec.objects.filter(status='อนุมัติ').order_by('name', 'datetime')
    page_num = req.GET.get('page', 1)
    p = Paginator(AllRecList, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)    
    context =  {
        "navbar" : "staff_introduction_history",
        'page' : page
    }            
    return render( req, 'pages/staff_introduction_history.html', context)

# จัดการข้อมูลการแนะนำวัสดุเข้าสู่ระบบ
@login_required
def staff_introduction_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllRecList = ListFromRec.objects.filter(id=id).first()
    context = {
        "AllRecList" : AllRecList,
    }
    return render( req, 'pages/staff_introduction_detail.html', context)

# ประวัติการยืม
@login_required
def staff_borrowing_history(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='ยืมสำเร็จ'))
    context = {
        "navbar" : "staff_borrowing_history",
        "AllLoanParcel" : AllLoanParcel,
    }
    return render(req,'pages/staff_borrowing_history.html', context)
    
@login_required
def staff_borrowing_history_durable(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(Q(status='ไม่อนุมัติ') | Q(status='คืนสำเร็จ'))
    context =  {
        "navbar" : "staff_borrowing_history_durable",
        "AllLoanDurable" : AllLoanDurable,
    }
    return render(req,'pages/staff_borrowing_history_durable.html', context)    

# จัดการรายการยืม
@login_required
def staff_index_borrow(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(status='รออนุมัติ').order_by('name', 'date_add')
    context = {
        "navbar" : "staff_index_borrow",
        "AllLoanParcel" : AllLoanParcel,
    }
    return render(req,'pages/staff_index_borrow.html', context)

@login_required
def staff_index_borrow_durable(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(status='รออนุมัติ').order_by('name', 'date_add')
    context =  {
        "navbar" : "staff_index_borrow_durable",
        "AllLoanDurable" : AllLoanDurable,
    }
    return render(req,'pages/staff_index_borrow_durable.html', context)

# จัดการรายการยืม
@login_required
def staff_index_borrownow(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(Q(status='กำลังยืม'))
    context = {
        "navbar" : "staff_index_borrownow",
        "AllLoanDurable" : AllLoanDurable,
    }
    return render(req,'pages/staff_index_borrownow.html', context)

# จัดการรายการกำลังยืม
def staff_index_return(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการคืน'))
    context = {
        "navbar" : "staff_index_return",
        "AllLoanDurable" : AllLoanDurable,
    }
    return render(req,'pages/staff_index_return.html', context)

def staff_return_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    if AllLoanDurable is None:
        return redirect('/staff_index_return')
    AllLoanDurable.status = 'คืนสำเร็จ'
    AllLoanDurable.save()
    messages.success(req, 'คืนสำเร็จ!')
    return redirect('/staff_index_return')

def staff_unreturn_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    if AllLoanDurable is None:
        return redirect('/staff_index_return')
    AllLoanDurable.reasonfromstaff = req.POST['reasonfromstaff']
    AllLoanDurable.status = 'คืนไม่สำเร็จ'
    AllLoanDurable.save()
    messages.success(req, 'คืนไม่สำเร็จ!')
    return redirect('/staff_index_return')

def staff_borrow_parcel(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(id=id).first()
    if AllLoanParcel is None :
        return redirect('/staff_index_borrow')
    AllLoanParcel.reasonfromstaff = req.POST['reasonfromstaff']
    AllLoanParcel.status = 'รอยืนยันการรับ'
    AllLoanParcel.save()
    return redirect('/staff_index_borrow')

def staff_borrow_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    if AllLoanDurable is None:
        return redirect('/staff_index_borrow_durable')
    AllLoanDurable.reasonfromstaff = req.POST['reasonfromstaff']
    AllLoanDurable.status = 'รอยืนยันการรับ'
    AllLoanDurable.save()
    messages.success(req, 'รอยืนยันการรับ!')
    return redirect('/staff_index_borrow_durable')

def staff_unborrow_parcel(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(id=id).first()
    if AllLoanParcel is None:
        return redirect('/staff_index_borrow')
    AllLoanParcel.reasonfromstaff = req.POST['reasonfromstaff']
    AllLoanParcel.status = 'ไม่อนุมัติ'
    AllLoanParcel.save()
    messages.success(req, 'ไม่อนุมัติ!')
    return redirect('/staff_index_borrow')

def staff_unborrow_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    if AllLoanDurable is None:
        return redirect('/staff_index_borrow_durable')
    AllLoanDurable.reasonfromstaff = req.POST['reasonfromstaff']
    AllLoanDurable.status = 'ไม่อนุมัติ'
    AllLoanDurable.save()
    messages.success(req, 'ไม่อนุมัติ!')
    return redirect('/staff_index_borrow_durable')

# รายละเอียดจัดการวัสดุ-ครุภัณฑ์
@login_required
def staff_manage_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllParcel = Add_Parcel.objects.filter(id=id).first()
    waiting_qParcel = QueueParcel.objects.filter(queue_item=AllParcel).count()
    context = {
        "AllParcel" : AllParcel,
        "waiting_qParcel" : waiting_qParcel,
    }
    return render(req,'pages/staff_manage_detail.html', context)

@login_required
def staff_manage_detail_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllDurable = Add_Durable.objects.filter(id=id).first()
    waiting_qDurable = QueueDurable.objects.filter(queue_item=AllDurable).count()
    waiting_period = waiting_qDurable * AllDurable.numdate
    context = {
        "AllDurable" : AllDurable,
        "waiting_qDurable" : waiting_qDurable,
        "waiting_period": waiting_period
    }
    return render(req,'pages/staff_manage_detail_durable.html', context)

# จัดการวัสดุ
@login_required
def staff_manage_parcel(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    form = ParcelForm()

    if req.method == 'POST':
        form = ParcelForm(req.POST, req.FILES)
        if form.is_valid():
            if form.cleaned_data['quantitytype'] == "∞":
                form.cleaned_data['quantity'] += 1
            form.save()
            messages.success(req, 'เพิ่มรายการวัสดุสำเร็จ!')
            return redirect('/staff_manage_parcel')
    else:
        messages.success(req, 'เพิ่มรายการวัสดุไม่สำเร็จ!')
        form = ParcelForm()
    AllParcel = Add_Parcel.objects.all()
    page_num = req.GET.get('page', 1)
    p = Paginator(AllParcel, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)        
    context = {
        "navbar" : "staff_manage_parcel",
        "page" : page,
        "form" : form,
    }    
    return render(req, 'pages/staff_manage_parcel.html', context)


@login_required
def delete_staff_manage_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    obj = Add_Parcel.objects.get(id=id)
    obj.delete()
    return redirect('staff_manage_parcel')

@login_required
def edit_staff_manage_parcel(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllParcel = Add_Parcel.objects.get(id=id)
    form = ParcelForm(req.POST or None, req.FILES or None, instance=AllParcel) 
    if form.is_valid():
        for field in form.fields:
            if not form.cleaned_data[field]:
                form.cleaned_data[field] = getattr(AllParcel, field)
        form.save()
        messages.success(req, 'แก้ไขรายการวัสดุสำเร็จ!')
    context = {
        "AllParcel" : AllParcel,
        "form" : form
    }
    return redirect('/staff_manage_parcel', context)


@login_required
def delete_staff_manage_parcel(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    obj = Add_Parcel.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบรายการวัสดุสำเร็จ!')
    return redirect('staff_manage_parcel')

# จัดการครุภัณฑ์
@login_required
def staff_manage_durable(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    form = DurableForm()

    if req.method == 'POST':
        form = DurableForm(req.POST, req.FILES)
        if form.is_valid():
            if form.is_valid['quantitytype'] == "∞":
                form.is_valid['quantity'] = float("inf")
            form.save()
            messages.success(req, 'เพิ่มรายการครุภัณฑ์สำเร็จ!')
            return redirect('/staff_manage_durable')
    else:
        messages.success(req, 'เพิ่มรายการครุภัณฑ์ไม่สำเร็จ!')
        form = DurableForm()
    AllDurable = Add_Durable.objects.all()
    page_num = req.GET.get('page', 1)
    p = Paginator(AllDurable, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)   
    context =  {
        "navbar" : "staff_manage_durable",
        "page" : page,
        "form" : form
    }    
    return render(req, 'pages/staff_manage_durable.html', context) 

@login_required
def delete_staff_manage_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    obj = Add_Durable.objects.get(id=id)
    obj.delete()
    return redirect('staff_manage_durable') 

@login_required
def edit_staff_manage_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllDurable = Add_Durable.objects.get(id=id)
    form = DurableForm(req.POST or None, req.FILES or None, instance=AllDurable) 
    if form.is_valid():
        for field in form.fields:
            if not form.cleaned_data[field]:
                form.cleaned_data[field] = getattr(AllDurable, field)
        form.save()
        messages.success(req, 'แก้ไขรายการครุภัณฑ์สำเร็จ!')
    context = {
        "AllDurable" : AllDurable,
        "form" : form
    }
    return redirect('/staff_manage_durable', context)


def pdf_print(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllRecList = ListFromRec.objects.all()             
    context = {
        "AllRecList" : AllRecList,
    }
    return render( req, 'pages/pdf.html', context)

# แก่ไขข้อมูลส่วนตัว และจัดการข้อมูลส่วนตัว
@login_required
def staff_personal_info(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    return render(req, 'pages/staff_personal_info.html')  

@login_required
def staff_admin_user(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllUser = User.objects.all()
    AllUser_count = User.objects.filter(right = "นักศึกษา", status = "ปกติ") 
    context = {
        "navbar" : "staff_admin_user",
        "AllUser" : AllUser,
        "AllUser_count" : AllUser_count,
    }
    return render(req, "pages/staff_admin_user.html", context)

@login_required
def staff_admin_user_block(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllUser = User.objects.filter(status = "ถูกจำกัดสิทธิ์", right = "นักศึกษา")
    AllUser_count = User.objects.filter(status = "ถูกจำกัดสิทธิ์", right = "นักศึกษา")
    for AllUser in AllUser:
        if AllUser.deadline == 0:
            AllUser.status == "Normal"
        AllUser.save()
        messages.success(req, 'จำกัดสิทธิ์!')
    context = {
        "navbar" : "staff_admin_user_block",
        "AllUser" : AllUser,
        "AllUser_count" : AllUser_count,
    }    
    return render(req, "pages/staff_admin_user_block.html", context)

@login_required
def staff_user_deadline(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    obj = User.objects.get(id=id)
    obj.status = req.POST['status']
    obj.reasonfromstaff = req.POST['reasonfromstaff']
    deadline_str = req.POST['deadline']
    if deadline_str == '':
        obj.deadline = datetime.now() + timedelta(days=7)
    else:
        obj.deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
    obj.save()
    messages.success(req, 'จำกัดสิทธิ์!')
    return redirect('/staff_admin_user_block')

@login_required
def staff_personal_info_edit(req,id):
    obj = User.objects.get(id=id)
    phone = req.POST.get('phone')
    if phone:
        obj.phone = phone
        obj.save()
        messages.success(req, 'เพิ่มเบอร์โทรศัพท์สำเร็จ!')
    else:
        obj.phone = phone
        obj.save() 
        messages.success(req, 'เพิ่มเบอร์โทรศัพท์สำเร็จ!')
    return redirect('/staff_personal_info') 

@login_required
def staff_personal_info(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    return render(req,'pages/staff_personal_info.html')

# รายงานภาพรวมวัสดุ
@login_required
def staff_report(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllRecList_count = ListFromRec.objects.filter(status='รออนุมัติ') 
    AllLoanDurable_count = LoanDurable.objects.filter(status='รอยืนยันการคืน')
    AllLoanParcel_count_borrow = LoanParcel.objects.filter(status='รออนุมัติ')
    AllLoanDurable_count_borrow = LoanDurable.objects.filter(status='รออนุมัติ')
    AllLoanDurable_count_borrownow = LoanDurable.objects.filter(status='กำลังยืม')
    AllUser_count = User.objects.filter(right = "นักศึกษา", status = "ปกติ") 
    AllUser_count_block = User.objects.filter(status = "ถูกจำกัดสิทธิ์", right = "นักศึกษา")
    AllParcel_report = Add_Parcel.objects.all().aggregate(models.Count('id'))['id__count']
    AllDurable_report = Add_Durable.objects.all().aggregate(models.Count('id'))['id__count']
    MaxLoanParcel = Add_Parcel.objects.values("statustype","nametype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')[:3]
    MaxLoanDurable = Add_Durable.objects.values("statustype","nametype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')[:3]
    context = {
        "navbar" : "staff_report",
        "AllRecList_count" : AllRecList_count,
        "AllLoanDurable_count" : AllLoanDurable_count,
        "AllLoanParcel_count_borrow" : AllLoanParcel_count_borrow,
        "AllLoanDurable_count_borrow" : AllLoanDurable_count_borrow,
        "AllLoanDurable_count_borrownow" : AllLoanDurable_count_borrownow,
        "AllUser_count" :AllUser_count,
        "AllUser_count_block" : AllUser_count_block,
        "AllParcel_report" : AllParcel_report,
        "AllDurable_report" : AllDurable_report,
        "MaxLoanParcel" : MaxLoanParcel,
        "MaxLoanDurable" : MaxLoanDurable,
        
    }
    return render( req, 'pages/staff_report.html', context)

# รายงานการยืมทั้งหมด
@login_required
def staff_max_borrow(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    MaxLoanParcel = Add_Parcel.objects.values("statustype","nametype","quantitytype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
    context = {
        "MaxLoanParcel" : MaxLoanParcel,
    }
    return render(req,'pages/staff_max_borrow.html', context )

def staff_max_borrow_durable(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    MaxLoanDurable = Add_Durable.objects.values("statustype","nametype","quantitytype","quantity", "id","name").annotate(borrow_count=Max('borrow_count')).order_by('-borrow_count')
    context = {
        "MaxLoanDurable" : MaxLoanDurable,
    }
    return render(req,'pages/staff_max_borrow_durable.html', context )

def staff_queue(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllQueueParcel = QueueParcel.objects.all()
    context ={
        'navbar' : 'staff_queue',
        "AllQueueParcel" : AllQueueParcel,
    }
    return render(req, 'pages/staff_queue.html', context)

def staff_queue_durable(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllQueueDurable = QueueDurable.objects.all()
    context ={
        'navbar' : 'staff_queue_durable',
        "AllQueueDurable" : AllQueueDurable,
    }
    return render(req, 'pages/staff_queue_durable.html', context)

def staff_position(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.right == "นักศึกษา":
        return redirect('/')
    AllDurable = Add_Durable.objects.all()
    AllParcel = Add_Parcel.objects.all()
    AllPosition =  SettingPosition.objects.all()   
    items_position = {}
    for position in AllPosition:
        items_position[position] = []
    for AllParcel in AllParcel:
        items_position[AllParcel.nameposition].append(AllParcel)
    for AllDurable in AllDurable:
        items_position[AllDurable.nameposition].append(AllDurable)
    
    context ={
        'navbar' : 'staff_position',
        "items_position": items_position,
        "AllPosition" : AllPosition,
    }
    return render(req, 'pages/staff_position.html', context)

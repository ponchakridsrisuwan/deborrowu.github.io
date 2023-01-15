from asyncio import Queue
from datetime import *
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from myapp import forms
from myapp.admin import *
from django.utils import timezone
from django.core.paginator import Paginator
from myapp.forms import *
from myappSuper.models import *
from myappstaff.models import *
import datetime
from django.contrib import messages


#หน้าหลัก
def HomePage(req):
    if req.user.is_anonymous:
        return redirect('login/')
    AllParcel = Add_Parcel.objects.all()
    AllDurable = Add_Durable.objects.all()
    AllLoanParcel = LoanParcel.objects.filter(
        Q(status='รอยืนยันการรับ') , user=req.user).order_by('status')
    AllLoanDurable = LoanDurable.objects.filter(
        Q(status='รอยืนยันการรับ') , user=req.user).order_by('status')
    
    categoryID = req.GET.get('category')
    DurableID = req.GET.get('durable')
    if categoryID:
        DurableAll = Add_Durable.objects.filter(category_id = categoryID).order_by('id')
        ParcelAll = Add_Parcel.objects.filter(category_id = categoryID).order_by('id')
        categoryType = CategoryType.objects.all()

    elif 'q' in req.GET:
        q = req.GET['q']
        DurableAll = Add_Durable.objects.filter(name__icontains = q)
        categoryType = CategoryType.objects.all()
        ParcelAll = Add_Parcel.objects.filter(name__icontains = q)

    else:
        DurableAll = Add_Durable.objects.all()
        categoryType = CategoryType.objects.all()
        ParcelAll = Add_Parcel.objects.all()
    context = {
        "navbar" : "user_index",
        "categoryType" : categoryType,
        "ParcelAll" : ParcelAll,
        "DurableAll" : DurableAll,
        
        "AllParcel" : AllParcel,
        "AllDurable" : AllDurable,
        
        "AllLoanParcel" : AllLoanParcel,
        "AllLoanDurable" : AllLoanDurable,
    }    
    return render(req, 'pages/user_index.html', context)

def phone_add_number(req):
    if req.method == 'POST':
        phone = req.POST['phone']
        if phone is not None:
            req.user.phone = phone
            req.user.save()
            messages.success(req, 'เพิ่มเบอร์โทรศัพท์สำเร็จ!')
            return redirect('/')
        else: 
            messages.success(req, 'เพิ่มเบอร์โทรศัพท์ไม่สำเร็จ!')
            return redirect('/phone_add_number')
    else:
        return render(req, 'pages/phone_add_number.html')
    
def user_personal_info(req):
    return render(req, 'pages/user_personal_info.html')

#หน้ายืม
@login_required
def user_borrow(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(Q(status='รออนุมัติ') | Q(status='รอยืนยันการรับ'), user=req.user).order_by('status')
    context = {
        "navbar" : "user_borrow",
        "AllLoanParcel" : AllLoanParcel,
    }
    return render(req,'pages/user_borrow.html', context)
    
def user_borrow_durable(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    user = req.user
    AllLoanDurable = LoanDurable.objects.filter(
        Q(status='รอยืนยันการรับ') | Q(status='รออนุมัติ') | Q(status='คืนไม่สำเร็จ'), user=user).order_by('status')
    context = {
        "navbar" : "user_borrow_durable",
        "AllLoanDurable" : AllLoanDurable,
    }
    return render(req,'pages/user_borrow_durable.html', context)    

def confirm_parcel(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    AllLoanParcel = LoanParcel.objects.filter(id=id).first()
    AllLoanParcel.status = 'ยืมสำเร็จ'
    AllLoanParcel.save()
    messages.success(req, 'ยืมสำเร็จ!')
    return redirect('/user_history')

def confirm_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    AllLoanDurable.status = 'กำลังยืม'
    AllLoanDurable.save()
    messages.success(req, 'กำลังยืม!')
    return redirect('/user_borrowed')

def return_durable(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    AllLoanDurable = LoanDurable.objects.filter(id=id).first()
    AllLoanDurable.status = 'รอยืนยันการคืน'
    AllLoanDurable.save()
    messages.success(req, 'รอยืนยันการคืน!')
    return redirect('/user_borrowed')

#หน้าคืน
@login_required
def user_borrowed(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    user = req.user
    AllLoanDurable = LoanDurable.objects.filter(Q(status='รอยืนยันการคืน')| Q(status='คืนไม่สำเร็จ') | Q(status='กำลังยืม' ), user=user)
    context = {
        'navbar' : 'user_borrowed',
        "AllLoanDurable" : AllLoanDurable,
    }
    return render(req,'pages/user_borrowed.html', context)

#หน้าประวัติ
@login_required
def user_history(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    user = req.user
    AllLoanParcel = LoanParcel.objects.filter(Q(status='ไม่อนุมัติ')| Q(status='ยืมสำเร็จ'), user=user)
    context = {
        'navbar' : 'user_history',
        "AllLoanParcel" : AllLoanParcel,
    }
    return render(req,'pages/user_history.html', context)
    
@login_required
def user_history_durable(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    user = req.user
    AllLoanDurable = LoanDurable.objects.filter(Q(status='คืนสำเร็จ') | Q(status='ไม่อนุมัติ'), user=user)
    context = {
        'navbar' : 'user_history',
        "AllLoanDurable" : AllLoanDurable,
    }
    return render(req,'pages/user_history_durable.html', context)    

#หน้ายืม
def user_cart(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    AllCartParcel = CartParcel.objects.filter(user = req.user)
    AllCartDurable = CartDurable.objects.filter(user = req.user)
    AllCartParcel_sum = CartParcel.objects.filter(user = req.user).aggregate(Sum('quantity'))
    AllCartDurabl_sum = CartDurable.objects.filter(user = req.user).aggregate(Sum('quantity'))
    TotalParcel = AllCartParcel_sum.get('quantity__sum')
    TotalDurable = AllCartDurabl_sum.get('quantity__sum')

    context = {
        "AllCartParcel" : AllCartParcel,
        "AllCartDurable" : AllCartDurable,
        "TotalParcel" : TotalParcel,
        "TotalDurable" : TotalDurable,
    }
    return render(req, 'pages/user_cart.html',context)

def add_to_cart(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None:
        return redirect('/')
    parcel_item = Add_Parcel.objects.get(id=id)
    if parcel_item.quantity > 0 or parcel_item.quantitytype == "∞":
        if parcel_item.quantitytype == "∞":
            parcel_item.borrow_count += 1  
            parcel_item.save()
            messages.success(req, 'เพิ่มรายการสำเร็จ!')
        else :    
            parcel_item.quantity -= 1
            parcel_item.borrow_count += 1  
            parcel_item.save()
            messages.success(req, 'เพิ่มรายการสำเร็จ!')
        ex_cart_parcel = CartParcel.objects.filter(parcel_item=parcel_item, user=req.user)
        if ex_cart_parcel.exists():
            cart_parcel = ex_cart_parcel.first()
            cart_parcel.quantity += 1
            cart_parcel.name = parcel_item.name
            cart_parcel.type = parcel_item.nametype
            cart_parcel.statusParcel = parcel_item.statustype
            cart_parcel.nameposition = parcel_item.nameposition.nameposition
            if cart_parcel.quantity < 3:
                cart_parcel.save()
                messages.success(req, 'จำกัดจำนวนการยืมในแต่ละครั้ง กรุณาทำรายการใหม่อีกครั้ง!')
        else:
            cart_parcel = CartParcel.objects.create(user=req.user, parcel_item=parcel_item)
            cart_parcel.quantity = 1  
            cart_parcel.name = parcel_item.name
            cart_parcel.type = parcel_item.nametype
            cart_parcel.statusParcel = parcel_item.statustype
            cart_parcel.nameposition = parcel_item.nameposition.nameposition
            if cart_parcel.quantity < 3:
                cart_parcel.save()
                messages.success(req, 'จำกัดจำนวนการยืมในแต่ละครั้ง กรุณาทำรายการใหม่อีกครั้ง!')
        return redirect('/user_cart')
    else:
        queue_item = QueueParcel.objects.filter(user=req.user, queue_item=parcel_item).first()
        if queue_item:
            if parcel_item.quantity > 0 or parcel_item.quantitytype == "∞":
                if parcel_item.quantitytype == "∞":
                    parcel_item.borrow_count += 1  
                    parcel_item.save()
                else:    
                    parcel_item.quantity -= 1
                    parcel_item.borrow_count += 1  
                    parcel_item.save()
                ex_cart_parcel = CartParcel.objects.filter(parcel_item=parcel_item, user=req.user)
                if ex_cart_parcel.exists():
                    cart_parcel = ex_cart_parcel.first()
                    cart_parcel.quantity += 1
                    cart_parcel.name = parcel_item.name
                    cart_parcel.type = parcel_item.nametype
                    cart_parcel.statusParcel = parcel_item.statustype
                    cart_parcel.nameposition = parcel_item.nameposition.nameposition
                    if cart_parcel.quantity < 3:
                        cart_parcel.save()
                else:
                    cart_parcel = CartParcel.objects.create(user=req.user, parcel_item=parcel_item)
                    cart_parcel.quantity = 1
                    cart_parcel.name = parcel_item.name
                    cart_parcel.type = parcel_item.nametype
                    cart_parcel.statusParcel = parcel_item
                    cart_parcel.statusParcel = parcel_item.statustype
                    cart_parcel.nameposition = parcel_item.nameposition.nameposition
                    cart_parcel.borrow_count += 1
                    if cart_parcel.quantity < 3:
                        cart_parcel.save()
                queue_item.delete()
                return redirect('/user_cart')
        else:
            queue_item = QueueParcel.objects.create(user=req.user, queue_item=parcel_item, name=parcel_item.name, type=parcel_item.nametype)
            queue_item.name = parcel_item.name
            queue_item.type = parcel_item.nametype
            #queue_item.statusParcel = parcel_item.statusParcel
            queue_item.save()
            messages.success(req, 'จองคิวสำเร็จ!')
        return redirect('/user_queue')
    
    
def cart_update(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None:
        return redirect('/')
    parcel_item = Add_Parcel.objects.get(id=id)
    if parcel_item.quantity > 0 or parcel_item.quantitytype == "∞":
        cart_parcel = CartParcel.objects.get(parcel_item=parcel_item, user=req.user)
        if cart_parcel.quantity < 3:
            cart_parcel.quantity += 1
            cart_parcel.save()
            if parcel_item.quantitytype == "∞":  
                parcel_item.borrow_count += 1
                parcel_item.save()
            else:
                parcel_item.quantity -= 1
                parcel_item.save()
    return redirect('/user_cart')


def cart_notupdate(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None:
        return redirect('/')
    parcel_item = Add_Parcel.objects.get(id=id)
    if parcel_item.quantity > 0 or parcel_item.quantitytype == "∞":
        cart_parcel = CartParcel.objects.get(parcel_item=parcel_item, user=req.user)
        if cart_parcel.quantity > 0:
            parcel_item.quantity += 1
            parcel_item.borrow_count -= 1
            parcel_item.save()
            cart_parcel.quantity -= 1
            cart_parcel.save()
        elif cart_parcel.quantity < 1:
            cart_parcel.delete()
    return redirect('/user_cart')


def user_queue(req):
    AllQueueParcel = QueueParcel.objects.filter(user=req.user)
    context ={
        'navbar' : 'user_queue',
        "AllQueueParcel" : AllQueueParcel,
    }
    return render(req, 'pages/user_queue.html', context)

def add_multiple_to_borrow_parcel(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    description = req.POST.get('description')
    if not description or description == "":
        return redirect('/user_cart') 
    cart_parcels = CartParcel.objects.filter(user=req.user)
    start_date = req.POST.get('start_date')
    if start_date is None or start_date == "":
        start_date = date.today()
    else:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    for cart_parcel in cart_parcels:
        add_parcel = Add_Parcel.objects.get(id=cart_parcel.parcel_item.id)
        if start_date < date.today():
            pass
        else:
            loan_parcel = LoanParcel()
            loan_parcel.user = req.user
            loan_parcel.start_date = start_date
            loan_parcel.description = description
            loan_parcel.name = cart_parcel.name
            loan_parcel.parcel_item = add_parcel
            loan_parcel.quantity = cart_parcel.quantity
            loan_parcel.type = cart_parcel.type
            loan_parcel.statusParcel = cart_parcel.statusParcel
            loan_parcel.nameposition = cart_parcel.nameposition
            loan_parcel.save()
            cart_parcel.delete()
            messages.success(req, 'รอการอนุมัติ!')
    return redirect('/user_borrow')

def delete_borrow_parcel(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    try:
        loan_parcel = LoanParcel.objects.get(id=id)
        parcel = loan_parcel.parcel_item
        if parcel.quantitytype == "∞":
            parcel.borrow_count -= loan_parcel.quantity
            parcel.save()
            loan_parcel.delete()
            messages.success(req, 'ยกเลิกการยืม!')
            return redirect('/user_cart')
        else:
            parcel.quantity += loan_parcel.quantity
            parcel.borrow_count -= loan_parcel.quantity
            parcel.save()
            loan_parcel.delete()
            messages.success(req, 'ยกเลิกการยืม!')
            return redirect('/user_cart')
    except LoanParcel.DoesNotExist:
        return redirect('/user_cart')
    
    
def delete_add_to_cart(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    if CartParcel.objects.filter(id=id).exists():
        obj = CartParcel.objects.get(id=id)
        parcel_obj = obj.parcel_item
        if parcel_obj.quantitytype == "∞":
            parcel_obj.borrow_count -= obj.quantity
            parcel_obj.save()
            obj.delete()
            messages.success(req, 'ลบรายการสำเร็จ!')
            return redirect('/user_cart')
        else:
            parcel_obj.quantity += obj.quantity
            parcel_obj.borrow_count -= obj.quantity
            parcel_obj.save()
            obj.delete()   
            messages.success(req, 'ลบรายการสำเร็จ!')
            return redirect('/user_cart')
    else:
        return redirect('/user_cart')
    
def delete_queue(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    obj = QueueParcel.objects.get(id=id)
    obj.delete()
    return redirect('/user_queue')          

def add_to_cart_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    durable_item = Add_Durable.objects.get(id=id)
    if durable_item.quantity > 0 or durable_item.quantitytype == "∞":
        if durable_item.quantitytype == "∞":
            durable_item.borrow_count += 1  
            durable_item.save()
            messages.success(req, 'เพิ่มรายการสำเร็จ!')
        else:
            durable_item.quantity -= 1
            durable_item.borrow_count += 1  
            durable_item.save()
            messages.success(req, 'เพิ่มรายการสำเร็จ!')
            existing_cart_durable = CartDurable.objects.filter(durable_item=durable_item, user=req.user)
        if existing_cart_durable.exists():
            cart_durable = existing_cart_durable.first()
            cart_durable.quantity += 1
            cart_durable.name = durable_item.name
            cart_durable.type = durable_item.nametype
            cart_durable.statusDurable = durable_item.statustype
            cart_durable.nameposition = durable_item.nameposition.nameposition
            if cart_durable.quantity < 3:
                cart_durable.save()
                messages.success(req, 'จำกัดจำนวนการยืมในแต่ละครั้ง กรุณาทำรายการใหม่อีกครั้ง!')
        else:
            cart_durable = CartDurable.objects.create(user=req.user, durable_item=durable_item)
            cart_durable.quantity = 1  
            cart_durable.name = durable_item.name
            cart_durable.type = durable_item.nametype
            cart_durable.statusDurable = durable_item.statustype
            cart_durable.nameposition = durable_item.nameposition.nameposition
            if cart_durable.quantity < 3:
                cart_durable.save()
                messages.success(req, 'จำกัดจำนวนการยืมในแต่ละครั้ง กรุณาทำรายการใหม่อีกครั้ง!')
        return redirect('/user_cart')
    else:
        queue_item = QueueDurable.objects.filter(user=req.user, queue_item=durable_item).first()
        if queue_item:
            if durable_item.quantity > 0 or durable_item.quantitytype == "∞":
                if durable_item.quantitytype == "∞":
                    durable_item.borrow_count += 1  
                    durable_item.save()
                else:    
                    durable_item.quantity -= 1
                    durable_item.borrow_count += 1  
                    durable_item.save()
                existing_cart_durable = CartDurable.objects.filter(durable_item=durable_item, user=req.user)
                if existing_cart_durable.exists():
                    cart_durable = existing_cart_durable.first()
                    cart_durable.quantity += 1
                    cart_durable.name = durable_item.name
                    cart_durable.type = durable_item.nametype
                    cart_durable.statusDurable = durable_item.statustype
                    cart_durable.nameposition = durable_item.nameposition.nameposition
                    if cart_durable.quantity < 3:
                        cart_durable.save()
                else:
                    cart_durable = CartDurable.objects.create(user=req.user, durable_item=durable_item)
                    cart_durable.quantity = 1
                    cart_durable.name = durable_item.name
                    cart_durable.type = durable_item.nametype
                    cart_durable.statusDurable = durable_item
                    cart_durable.statusDurable = durable_item.statustype
                    cart_durable.nameposition = durable_item.nameposition.nameposition
                    cart_durable.borrow_count += 1
                    if cart_durable.quantity < 3:
                        cart_durable.save()
                queue_item.delete()
                return redirect('/user_cart')
        else:
            queue_item = QueueDurable.objects.create(user=req.user, queue_item=durable_item, name=durable_item.name, type=durable_item.nametype)
            queue_item.name = durable_item.name
            queue_item.type = durable_item.nametype
            queue_item.statusDurable = durable_item.statusDurable
            queue_item.save()
            messages.success(req, 'จองคิวสำเร็จ!')
        return redirect('/user_queue_durable')
    

def cart_update_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None:
        return redirect('/')
    durable_item = Add_Durable.objects.get(id=id)
    if durable_item.quantity > 0 or durable_item.quantitytype == "∞":
        cart_durable = CartDurable.objects.get(durable_item=durable_item, user=req.user)
        if cart_durable.quantity < durable_item.quantity:
            cart_durable.quantity += 1
            if cart_durable.quantity < 3:
                cart_durable.save()
            if durable_item.quantitytype == "∞":    
                durable_item.borrow_count += 1
                durable_item.save()
            else:
                durable_item.quantity -= 1
                if durable_item.quantity < 3:
                    durable_item.save()
    return redirect('/user_cart')


def cart_notupdate_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None:
        return redirect('/')
    durable_item = Add_Durable.objects.get(id=id)
    if durable_item.quantity > 0 or durable_item.quantitytype == "∞":
        cart_durable = CartDurable.objects.get(durable_item=durable_item, user=req.user)
        if cart_durable.quantity > 0:
            durable_item.quantity += 1
            durable_item.borrow_count -= 1
            durable_item.save()
            durable_item.quantity -= 1
            durable_item.save()
        elif cart_durable.quantity < 1:
            cart_durable.delete()
    return redirect('/user_cart')
    
def user_queue_durable(req):
    AllQueueDurable = QueueDurable.objects.filter(user=req.user)
    context = {
        'navbar' : 'user_queue_durable',
        "AllQueueDurable" : AllQueueDurable,
    }
    return render(req, 'pages/user_queue_durable.html', context)    
    
def add_multiple_to_borrow_durable(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    description = req.POST.get('description')
    if not description or description == "":
        return redirect('/user_cart') 
    cart_durable = CartDurable.objects.filter(user=req.user)
    start_date_input = req.POST.get('start_date')
    start_date = datetime.strptime(start_date_input, '%Y-%m-%d').date() if start_date_input else date.today()
    end_date_input = req.POST.get('end_date')
    for cart_durable in cart_durable:
        add_durable = Add_Durable.objects.get(id=cart_durable.durable_item.id)
        if end_date_input:
            end_date = datetime.strptime(end_date_input, '%Y-%m-%d').date()
        else:
            end_date = start_date + timedelta(days=add_durable.numdate)
        if start_date < date.today():
            pass
        elif end_date < start_date:
            pass
        else:
            loan_durable = LoanDurable()
            loan_durable.user = req.user
            loan_durable.start_date = start_date
            loan_durable.end_date = end_date
            loan_durable.description = description
            loan_durable.name = cart_durable.name
            loan_durable.durable_item = add_durable
            loan_durable.quantity = cart_durable.quantity
            loan_durable.type = cart_durable.type
            loan_durable.statusDurable = cart_durable.statusDurable
            loan_durable.nameposition = cart_durable.nameposition
            loan_durable.save()
            cart_durable.delete()
            messages.success(req, 'รออนุมัติการยืม!')
    return redirect('/user_borrow_durable')

def delete_borrow_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    try:
        loan_durable = LoanDurable.objects.get(id=id)
        durable = loan_durable.durable_item
        if durable.quantitytype == "∞":
            durable.borrow_count -= loan_durable.quantity
            durable.save()
            loan_durable.delete()
            messages.success(req, 'ยกเลิกการยืม!')
            return redirect('/user_cart')
        else:
            durable.quantity += loan_durable.quantity
            durable.borrow_count -= loan_durable.quantity
            durable.save()
            loan_durable.delete()
            messages.success(req, 'ยกเลิกการยืม!')
            return redirect('/user_cart')
    except LoanParcel.DoesNotExist:
        return redirect('/user_cart')
    
def delete_durable_add_to_cart(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    if CartDurable.objects.filter(id=id).exists():
        obj = CartDurable.objects.get(id=id)
        durable_obj = obj.durable_item
        if durable_obj.quantitytype == "∞":
            durable_obj.borrow_count -= obj.quantity
            durable_obj.save()
            obj.delete()
            messages.success(req, 'ลบรายการสำเร็จ!')
            return redirect('/user_cart')
        else:
            durable_obj.quantity += obj.quantity
            durable_obj.borrow_count -= obj.quantity
            durable_obj.save()
            obj.delete()
            messages.success(req, 'ลบรายการสำเร็จ!')
            return redirect('/user_cart')
    else:
        return redirect('/user_cart')  
    
def delete_queue_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    obj = QueueDurable.objects.get(id=id)
    obj.delete()
    return redirect('/user_queue_durable')      
    
#หน้ารายละเอียดวัสดุ
@login_required
def user_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    AllParcelAll = Add_Parcel.objects.all()
    AllDurableAll = Add_Durable.objects.all()
    AllParcel = Add_Parcel.objects.filter(id=id).first()
    waiting_qParcel = QueueParcel.objects.filter(queue_item=AllParcel).count()
    context = {
        "AllParcel" : AllParcel,
        "waiting_qParcel" : waiting_qParcel,
        "AllParcelAll" : AllParcelAll,
        "AllDurableAll" : AllDurableAll,
    }
    return render(req,'pages/user_detail.html',context)

def user_detail_durable(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    AllDurableAll = Add_Durable.objects.all()
    AllParcelAll = Add_Parcel.objects.all()
    AllDurable = Add_Durable.objects.filter(id=id).first()
    waiting_qDurable = QueueDurable.objects.filter(queue_item=AllDurable).count()
    if AllDurable is not None:
        waiting_period = waiting_qDurable * AllDurable.numdate
    else:
        waiting_period = None
    context = {
        "AllDurable" : AllDurable,
        "waiting_qDurable" : waiting_qDurable,
        "waiting_period": waiting_period,
        "AllDurableAll" : AllDurableAll,
        "AllParcelAll" : AllParcelAll,
    }
    return render(req,'pages/user_detail_durable.html',context)


#หน้ารายการวัสดุ
def user_durable_articles(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    categoryID = req.GET.get('category')
    DurableID = req.GET.get('durable')
    if categoryID:
        AllDurable = Add_Durable.objects.filter(category_id = categoryID).order_by('id')
        AllParcel = Add_Parcel.objects.filter(category_id = categoryID).order_by('id')
        categoryType = CategoryType.objects.all()

    elif 'q' in req.GET:
        q = req.GET['q']
        AllDurable = Add_Durable.objects.filter(name__icontains = q)
        categoryType = CategoryType.objects.all()
        AllParcel = Add_Parcel.objects.filter(name__icontains = q)

    else:
        AllDurable = Add_Durable.objects.all()
        categoryType = CategoryType.objects.all()
        AllParcel = Add_Parcel.objects.all()
    context =  {
        "navbar" : "user_durable_articles",
        "categoryType" : categoryType,
        "AllParcel" : AllParcel,
        "AllDurable" : AllDurable,
    }    
    return render(req, 'pages/user_durable_articles.html',context)

#หน้าจัดการแจ้งเตือน
@login_required
def user_notifications(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    return render(req,'pages/user_notifications.html')

@login_required
def user_recommend_history(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    AllRecList = ListFromRec.objects.filter(Q(status='รออนุมัติ'))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllRecList, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)        
    context = {
        "page" : page,
    }
    return render(req, 'pages/user_recommend_history.html', context)     

#หน้าแนะนำวัสดุ
@login_required
def user_recommend(req):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    if req.method == "POST":
        username = req.user
        name = req.POST.get('name')
        brand = req.POST.get('brand')
        quantity = req.POST.get('quantity')
        price = req.POST.get('price')
        link = req.POST.get('link')
        description = req.POST.get('description')
        datetime = timezone.now()
        obj = ListFromRec(username=username, name=name, brand=brand, quantity=quantity, 
                          price=price, link=link, description=description, datetime=datetime)
        obj.save()
        messages.success(req, 'แนะนำรายการสำเร็จ!')
        return redirect('/user_recommend')   
    else:
        messages.success(req, 'แนะนำรายการไม่สำเร็จ!')
        obj = ListFromRec()   
    obj = ListFromRec.objects.all()   
    AllRecList = ListFromRec.objects.filter(Q(status='รออนุมัติ'))
    page_num = req.GET.get('page', 1)
    p = Paginator(AllRecList, 10)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)        
    context = {
        "AllRecList" : ListFromRec.objects.filter(Q(status='รออนุมัติ')),
        "page" : page,
    }
    return render(req, 'pages/user_recommend.html', context)   

@login_required
def user_recommend_edit(req,id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    obj = ListFromRec.objects.get(id=id)
    obj.name = req.POST['name']
    obj.brand = req.POST['brand']
    obj.quantity = req.POST['quantity']
    obj.price = req.POST['price']
    obj.link = req.POST['link']
    obj.description = req.POST['description']
    obj.datetime = timezone.now()
    obj.save()
    messages.success(req, 'แก้ไขการแนะนำรายการสำเร็จ!')
    return redirect('/user_recommend') 

# รายงานสถานะข้อมูลการแนะนำวัสดุเข้าสู่ระบบ
@login_required
def user_recommend_detail(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    AllRecList = ListFromRec.objects.filter(id=id).first()
    context = {
        "AllRecList" : AllRecList,
    }
    return render( req, 'pages/user_recommend_detail.html', context)

def deleteRecList(req, id):
    if req.user.status == "ถูกจำกัดสิทธ์" or req.user.phone is None :
        return redirect('/')
    obj = ListFromRec.objects.get(id=id)
    obj.delete()
    messages.success(req, 'ลบการแนะนำรายการสำเร็จ!')
    return redirect('/user_recommend')

def user_position(req):
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
        'navbar' : 'user_position',
        "items_position": items_position,
        "AllPosition" : AllPosition,
    }
    return render(req, 'pages/user_position.html', context)
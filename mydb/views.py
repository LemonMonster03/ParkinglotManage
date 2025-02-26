from decimal import Decimal

from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from datetime import datetime
from .models import *
from django.contrib.auth.decorators import login_required


# 注册管理员
def register(request):
    user = User.objects.create_user(username='ypx',email='123456@qq.com',password='123456')
    # 可以增加新的管理员
    # 只需要像上面一样使用User.objects.create_user
    # 之后手动访问register触发该函数，返回HttpResponse的success即成功
    print("create user")
    return HttpResponse('success')


# 首页
def myindex(request):
    return render(request, 'myindex.html')


# 检测登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # 验证
        if user:
            return redirect('manage')   # 登录跳转
        else:
            return render(request, 'myindex.html', {'error': '账户或密码不正确'})   # 错误则重新渲染
    return render(request, 'myindex.html')  # 默认来到此页面


def manage(request):
    if request.method == 'POST':
        operation = request.POST.get('operation')
        if operation == 'car_list':
            return redirect('car_list')  # 跳转到汽车列表
        elif operation == 'record_list':
            return redirect('record_list')  # 跳转到记录列表
        elif operation == 'own':
            return redirect('own')  # 跳转到绑定列表
        elif operation == 'owner_list':
            return redirect('owner_list')  # 跳转到户主信息列表
        else:
            return redirect('myindex')  # 回到登录页面
    return render(request, 'manage.html')   # GET请求初始引导到控制页面


def car_list(request):
    # 获取搜索参数
    query_license_plate = request.GET.get('license_plate', '').strip()
    query_status = request.GET.get('status', '').strip()
    all_cars = Car.objects.all()

    # 根据搜索条件过滤
    if query_license_plate:
        all_cars = all_cars.filter(LicensePlate__icontains=query_license_plate)  # 根据车牌号过滤
    if query_status:
        if query_status == '已入库':
            all_cars = all_cars.filter(status=True)  # 只有 '已入库' 对应的条件
        elif query_status == '未入库':
            all_cars = all_cars.filter(status=False)  # 只有 '未入库' 对应的条件

    # 进行分页处理
    paginator = Paginator(all_cars, 5)  # 每页显示5条记录
    page_number = request.GET.get('page', 1)

    try:
        cars = paginator.page(page_number)
    except Exception as e:
        return HttpResponse(e)

    car_list = [
        {
            'LicensePlate': car.LicensePlate,
            'model': car.model,
            'color': car.color,
            'status': '已入库' if car.status else '未入库'  # 映射布尔值到字符串
        }
        for car in cars
    ]

    return render(request, 'car_list.html', {'cars': cars, 'car_list': car_list,
    'query_license_plate': query_license_plate, 'query_status': query_status})



# 添加视图
def add_car(request):
    if request.method == 'POST':
        try:
            license_plate = request.POST['license_plate']
            model = request.POST['model']
            color = request.POST['color']
            status = request.POST['status']
            Car.objects.create(LicensePlate=license_plate, model=model, color=color, status=status)
        except IntegrityError:
            return render(request, 'add_car.html',{"error":"添加了重复数据"})
        except Exception as e:
            return HttpResponse('发生以下错误:%s' % e)
        return redirect('car_list')
    return render(request, 'add_car.html')


# 编辑视图
def edit_car(request, license_plate):
    car = get_object_or_404(Car, LicensePlate=license_plate)
    if request.method == 'POST':
        car.model = request.POST['model']
        car.color = request.POST['color']
        car.status = request.POST['status']
        car.save()
        return redirect('car_list')
    return render(request, 'edit_car.html', {'car': car})


# 删除视图
def delete_car(request, license_plate):
    car = get_object_or_404(Car, LicensePlate=license_plate)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'delete_car.html', {'car': car})


def record_list(request):
    # 获取搜索参数
    query_admin_id = request.GET.get('admin_id', '').strip()
    query_plate = request.GET.get('plate', '').strip()
    query_parking_lot_id = request.GET.get('parking_lot_id', '').strip()
    query_spot_id = request.GET.get('spot_id', '').strip()
    all_records = Record.objects.all().prefetch_related(
        'where_set',
        'have_set',
        'manage_set'
    )

    # 根据搜索条件过滤
    if query_admin_id:
        all_records = all_records.filter(manage__admin__id=query_admin_id)  # 根据管理员ID过滤
    if query_plate:
        all_records = all_records.filter(have__car__LicensePlate=query_plate)  # 根据车牌号过滤
    if query_parking_lot_id:
        all_records = all_records.filter(where__parking_spot__parking_lot_id=query_parking_lot_id)  # 根据停车场ID过滤
    if query_spot_id:
        all_records = all_records.filter(where__parking_spot__spot_id=query_spot_id)  # 根据停车位ID过滤

    # 分页
    paginator = Paginator(all_records, 5)  # 每页显示5条记录
    page_number = request.GET.get('page', 1)

    try:
        records = paginator.page(page_number)
    except Exception as e:
        return HttpResponse(e)

    # 准备数据
    record_data = []
    for record in records:
        where_info = []
        for where in record.where_set.all():
            parking_spot = where.parking_spot
            where_info.append({
                'parking_lot_id': parking_spot.parking_lot_id,
                'spot_id': parking_spot.spot_id
            })

        have_info = []
        for have in record.have_set.all():
            have_info.append(have.car.LicensePlate)

        manage_info = []
        for manage in record.manage_set.all():
            manage_info.append(manage.admin.id)

        record_data.append({
            'record': record,
            'where_info': where_info,
            'have_info': have_info,
            'manage_info': manage_info,
        })

    return render(request, 'record_list.html', {
        'records': records,
        'record_data': record_data,
        'query_admin_id': query_admin_id,
        'query_plate': query_plate,
        'query_parking_lot_id': query_parking_lot_id,
        'query_spot_id': query_spot_id,
    })



def add_record(request):
    if request.method == 'POST':
        try:
            entry_time = request.POST['entry_time']
            exit_time = request.POST['exit_time']
            fee = request.POST['fee']
            lot_id = request.POST['lot_id']
            spot_id = request.POST['spot_id']
            license_plate = request.POST['license_plate']
            admin_id = request.POST['admin_id']

            car = Car.objects.filter(LicensePlate=license_plate).first()
            lot = ParkingSpot.objects.filter(parking_lot_id=lot_id, spot_id=spot_id).first()
            admin = Admin.objects.filter(id=admin_id).first()

            # 检验
            if entry_time:
                entry_time = datetime.strptime(entry_time, '%Y-%m-%dT%H:%M')
            else:
                raise ValueError("进入时间不能为空")

            if exit_time:
                exit_time = datetime.strptime(exit_time, '%Y-%m-%dT%H:%M')
            else:
                exit_time = None

            if not car:
                raise ValueError("没有相关车牌的汽车")
            elif car.status == 1:
                raise ValueError("该汽车已经入库")

            if not lot:
                raise ValueError("不存在该停车位")
            elif lot.status == 'Occupied':
                print(lot, lot.status)
                raise ValueError("该位置已经停有汽车")

            if not admin:
                raise ValueError("没有相关的负责人")

            if fee:
                fee = Decimal(fee)
            else:
                fee = None

            # 更新表
            Record.objects.create(entry_time=entry_time, exit_time=exit_time, fee=fee)
            record = Record.objects.get(entry_time=entry_time, exit_time=exit_time, fee=fee)
            Car.objects.filter(LicensePlate=license_plate).update(status=True)
            ParkingSpot.objects.filter(parking_lot_id=lot_id, spot_id=spot_id).update(status='Occupied')
            Have.objects.create(car_id=license_plate, record_id=record.id)
            Where.objects.create(record_id=record.id,parking_lot_id=lot_id,parking_spot_id=spot_id)
            Manage.objects.create(admin_id=admin_id, record_id=record.id)

        except IntegrityError:
            return render(request, 'add_record.html',{"error": "添加了重复数据"})
        except ValueError as ve:
            return render(request, 'add_record.html', {"error": str(ve)})
        except Exception as e:
            print(e)
            return render(request, 'add_record.html',{"error":str(e)})
        return redirect('record_list')
    return render(request, 'add_record.html')


def edit_record(request, record_id, LicensePlate, admin_id, lot_id, spot_id):
    record= get_object_or_404(Record, id=record_id)
    car = get_object_or_404(Car, LicensePlate=LicensePlate)
    admin = get_object_or_404(Admin, id=admin_id)
    parkingspot = get_object_or_404(ParkingSpot, parking_lot_id=lot_id, spot_id=spot_id)

    try:
        if request.method == 'POST':
            entry_time = request.POST['entry_time']
            exit_time = request.POST['exit_time']
            fee = request.POST['fee']
            new_license_plate = request.POST['license_plate']
            new_admin_id = request.POST['admin_id']
            new_lot_id = int(request.POST['lot_id'])
            new_spot_id = int(request.POST['spot_id'])

            new_car = Car.objects.filter(LicensePlate=new_license_plate).first()
            new_lot = ParkingSpot.objects.filter(parking_lot_id=new_lot_id, spot_id=new_spot_id).first()
            new_admin = Admin.objects.filter(id=new_admin_id).first()

            # 检验
            if entry_time:
                entry_time = datetime.strptime(entry_time, '%Y-%m-%dT%H:%M')
            else:
                raise ValueError("进入时间不能为空")

            if exit_time:
                exit_time = datetime.strptime(exit_time, '%Y-%m-%dT%H:%M')
            else:
                exit_time = None

            if not new_car:
                raise ValueError("没有相关车牌的汽车")
            elif new_license_plate != LicensePlate and new_car.status == 1:
                raise ValueError("该汽车已经入库")

            if not new_lot:
                raise ValueError("不存在该停车位")
            elif (new_lot_id != lot_id or new_spot_id != spot_id) and new_lot.status == 'Occupied':
                raise ValueError("该位置已经停有汽车")

            if not new_admin:
                raise ValueError("没有相关的负责人")

            if fee:
                fee = Decimal(fee)
            else:
                fee = None
            # 更新数据
            record.entry_time = entry_time
            record.exit_time = exit_time
            record.fee = fee
            record.save()
            Have.objects.filter(car_id=LicensePlate, record_id=record.id).update(car_id=new_license_plate)
            Manage.objects.filter(admin_id=admin_id, record_id=record.id).update(admin_id=new_admin_id)
            Where.objects.filter(record_id=record.id).update(parking_lot_id=new_lot_id,parking_spot_id=new_spot_id)
            return redirect('record_list')
    except Exception as e:
        return render(request, 'edit_record.html',
                      {'record': record, 'car': car, 'admin': admin, 'parkingspot': parkingspot, 'error': e})
    return render(request, 'edit_record.html', {'record': record, 'car': car, 'admin': admin, 'parkingspot':parkingspot})


def delete_record(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    record_data = []
    where_info = []
    for where in record.where_set.all():
        parking_spot = where.parking_spot
        where_info.append({
            'parking_lot_id': parking_spot.parking_lot_id,
            'spot_id': parking_spot.spot_id
        })
    have_info = []
    for have in record.have_set.all():
        have_info.append(have.car.LicensePlate)
    manage_info = []
    for manage in record.manage_set.all():
        manage_info.append(manage.admin.id)
    record_data.append({
        'record': record,
        'where_info': where_info,
        'have_info': have_info,
        'manage_info': manage_info,
    })
    if request.method == 'POST':
        if not record.exit_time:
            ParkingSpot.objects.filter(parking_lot_id=record.where_set.first().parking_spot.parking_lot_id,
                                       spot_id=record.where_set.first().parking_spot.spot_id).update(status='Available')
        Car.objects.filter(LicensePlate=record.have_set.first().car.LicensePlate).update(status=0)
        record.delete()
        return redirect('record_list')
    return render(request, 'delete_record.html', {'record_data': record_data})



def owner_list(request):
    query_id = request.GET.get('id', '').strip()
    query_name = request.GET.get('name', '').strip()
    all_owners = Owner.objects.all()
    # 根据搜索条件过滤
    if query_id:
        all_owners = all_owners.filter(id=query_id)
    if query_name:
        all_owners = all_owners.filter(name__icontains=query_name)

    paginator = Paginator(all_owners, 5)  # 每页5个户主
    page_number = request.GET.get('page', 1)
    try:
        owners = paginator.page(page_number)
    except Exception as e:
        return HttpResponse(e)

    owner_data = [
        {
            'id': owner.id,
            'name': owner.name,
            'phone_number': owner.phone_number,
            'address': owner.address,
            'gender': '男' if owner.gender == 'Male' else '女'
        }
        for owner in owners
    ]

    return render(request, 'owner_list.html', {'owners': owners, 'owner_data': owner_data,
    'query_id': query_id,'query_name': query_name})



# 添加视图
def add_owner(request):
    if request.method == 'POST':
        try:
            id = request.POST['id']
            name = request.POST['name']
            gender = request.POST['gender']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            Owner.objects.create(id=id, name=name, phone_number=phone_number, address=address, gender=gender)
        except IntegrityError:
            return render(request, 'add_owner.html',{"error":"添加了重复数据"})
        except Exception as e:
            return HttpResponse('发生以下错误:%s' % e)
        return redirect('owner_list')
    return render(request, 'add_owner.html')


# 编辑视图
def edit_owner(request, owner_id):
    owner = get_object_or_404(Owner, id=owner_id)
    if request.method == 'POST':
        owner.id = request.POST['id']
        owner.name = request.POST['name']
        owner.gender = request.POST['gender']
        owner.phone_number = request.POST['phone_number']
        owner.address = request.POST['address']
        owner.save()
        return redirect('owner_list')
    return render(request, 'edit_owner.html', {'owner': owner})


# 删除视图
def delete_owner(request, owner_id):
    owner = get_object_or_404(Owner, id=owner_id)
    if request.method == 'POST':
        owner.delete()
        return redirect('owner_list')
    return render(request, 'delete_owner.html', {'owner': owner})


def own(request):
    query_owner_id = request.GET.get('owner_id', '').strip()
    query_license_plate = request.GET.get('license_plate', '').strip()
    # 查询 Own 记录
    all_owns = Own.objects.select_related('owner', 'car')

    # 过滤
    if query_owner_id:
        all_owns = all_owns.filter(owner__id=query_owner_id)
    if query_license_plate:
        all_owns = all_owns.filter(car__LicensePlate__icontains=query_license_plate)

    # 提交新记录
    if request.method == 'POST':
        owner_id = request.POST.get('owner_id', '').strip()
        license_plate = request.POST.get('license_plate', '').strip()

        try:
            owner = Owner.objects.get(id=owner_id)
            car = Car.objects.get(LicensePlate=license_plate)
            # 检查是否已经存在该关系
            if not Own.objects.filter(owner=owner, car=car).exists():
                Own.objects.create(owner=owner, car=car)
                return redirect('own')  # 重定向回列表
            else:
                return render(request, 'own.html', {'error': '该关系已经存在。', 'owns': all_owns})
        except Owner.DoesNotExist:
            return render(request, 'own.html', {'error': '指定的 owner_id 不存在。', 'owns': all_owns})
        except Car.DoesNotExist:
            return render(request, 'own.html', {'error': '指定的车牌号不存在。', 'owns': all_owns})
    return render(request, 'own.html', {
        'owns': all_owns,
        'query_owner_id': query_owner_id,
        'query_license_plate': query_license_plate,
    })



def delete_own(request, own_id):
    own = get_object_or_404(Own, pk=own_id)

    if request.method == 'POST':
        own.delete()
        return redirect('own')  # 删除后重定向回列表

    return render(request, 'delete_own.html', {'own': own})
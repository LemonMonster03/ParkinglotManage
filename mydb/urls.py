# myapp/urls.py
from django.urls import path
from .views import *

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', myindex, name='myindex'),
    path('register', register, name='register'),    # 注册用户
    path('manage', manage, name='manage'),  # 管理界面
    path('login/', login, name='login'),        # 登录
    path('car_list', car_list, name='car_list'),  # car_list视图
    path('add_car/', add_car, name='add_car'),  # 添加汽车
    path('edit_car/<str:license_plate>/', edit_car, name='edit_car'),  # 编辑汽车
    path('delete_car/<str:license_plate>/', delete_car, name='delete_car'),  # 删除汽车
    path('record_list', record_list, name='record_list'),
    path('add_record', add_record, name='add_record'),
    path('edit_record/<str:record_id>/<str:LicensePlate>/<str:admin_id>/<int:lot_id>/<int:spot_id>', edit_record, name='edit_record'),
    path('delete_record/<str:record_id>', delete_record, name='delete_record'),
    path('owner_list', owner_list, name='owner_list'),
    path('add_owner', add_owner, name='add_owner'),
    path('edit_owner/<str:owner_id>', edit_owner, name='edit_owner'),
    path('delete_owner/<str:owner_id>', delete_owner, name='delete_owner'),
    path('own', own, name='own'),
    path('own/delete/<int:own_id>/', delete_own, name='delete_own'),
]
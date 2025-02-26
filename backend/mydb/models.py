from django.db import models


# Create your models here.


class Owner(models.Model):
    id = models.CharField(max_length=18, primary_key=True)  # ID
    name = models.CharField(max_length=20)   # 姓名
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')])  # 性别
    phone_number = models.CharField(max_length=15, null=True)  # 联系方式
    address = models.CharField(max_length=150, null=True)       # 居住地址

    class Meta:
        db_table = 'owner'

    def __str__(self):
        return self.id


class Car(models.Model):
    LicensePlate = models.CharField(max_length=20, primary_key=True)  # 车牌号
    model = models.CharField(max_length=100, null=True)                 # 车辆型号
    color = models.CharField(max_length=50, null=True)                  # 车身颜色
    status = models.BooleanField(default=False)     # 是否入库

    class Meta:
        db_table = 'car'

    def __str__(self):
        return self.LicensePlate


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    entry_time = models.DateTimeField()  # 进入时间
    exit_time = models.DateTimeField(null=True, blank=True)  # 离开时间
    fee = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 停车费用

    class Meta:
        db_table = 'record'

    def __str__(self):
        return f"Record {self.id}"


class ParkingSpot(models.Model):
    parking_lot_id = models.IntegerField()  # 停车场编号
    spot_id = models.IntegerField()          # 停车位编号
    status = models.CharField(max_length=9, choices=[('Available', 'Available'), ('Occupied', 'Occupied')], default='Available')  # 停车位状态

    class Meta:
        db_table = 'parkingspot'
        unique_together = (('parking_lot_id', 'spot_id'),)

    def __str__(self):
        return f"Spot {self.spot_id} in Lot {self.parking_lot_id}"


class Admin(models.Model):
    id = models.CharField(max_length=16, primary_key=True)  # 身份证ID
    name = models.CharField(max_length=20)   # 姓名
    contact_info = models.CharField(max_length=20, null=True)  # 联系方式

    class Meta:
        db_table = 'admin'

    def __str__(self):
        return self.id


class Own(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)  # 户主
    car = models.ForeignKey(Car, on_delete=models.CASCADE)      # 车

    class Meta:
        db_table = 'own'
        # unique_together = (('owner.', 'car'),)  # 联合主键

    def __str__(self):
        return f"{self.owner.name} owns {self.car.LicensePlate}"


class Have(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # 车
    record = models.ForeignKey(Record, on_delete=models.CASCADE)  # 记录

    class Meta:
        db_table = 'have'
        # unique_together = (('car', 'record'),)  # 联合主键

    def __str__(self):
        return f"{self.car.LicensePlate} has record {self.record.id}"


class Where(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)  # 记录
    parking_lot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='where_parking_lot')  # 停车场
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='where_parking_spot', default=1)  # 停车场

    class Meta:
        db_table = 'where'
        # unique_together = (('record', 'parking_lot'),)  # 联合主键

    def __str__(self):
        return f"Record {self.record.id} at {self.parking_lot}"


class Manage(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)  # 管理员身份
    record = models.ForeignKey(Record, on_delete=models.CASCADE)  # 记录编号

    class Meta:
        db_table = 'manage'
        # unique_together = (('admin', 'record'),)  # 联合主键

    def __str__(self):
        return f"Admin {self.admin.name} manages record {self.record.id}"

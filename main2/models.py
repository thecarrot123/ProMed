from django.utils import timezone
from django.db import models
from main.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator

TRANSFER_STATUS_CHOICES = [
    ('C', 'Confirmed'),
    ('U', 'Unconfirmed'),
]

EXPANSES_PAYMENT_CHOICES = [
    ('P', 'Paid'),
    ('U', 'Unpaid'),
]

class Library(models.Model):
    name = models.CharField(max_length=70,default='')
    library_fee = models.IntegerField(default = 0,validators=[MaxValueValidator(100),MinValueValidator(0)])
    total_profit = models.IntegerField(default = 0)
    def __str__(self):
        return str(self.name)

class LibraryTransfer(models.Model):
    user = models.ForeignKey(User, on_delete = CASCADE, null=True,verbose_name='المستخدم')
    amount = models.IntegerField("قيمة الحوالة")
    points = models.IntegerField("النقاط",default=0)
    library_id = models.ForeignKey(Library,on_delete=CASCADE,null=True,verbose_name='المكتبة')
    status = models.CharField(max_length=1,choices=TRANSFER_STATUS_CHOICES,default='U')
    def __str__(self):
        return str(self.user) + ' ' + str(self.amount)

class AlharamTransfer(models.Model):
    user = models.ForeignKey(User, on_delete = CASCADE, null=True)
    amount = models.IntegerField("قيمة الحوالة")
    points = models.IntegerField("النقاط",default=0)
    status = models.CharField(max_length=1,choices=TRANSFER_STATUS_CHOICES,default='U')
    receipt_number = models.IntegerField("رقم الايصال", unique = True, error_messages={
            'unique': ("تم ارسال رقم هذا الايصال مسبقاً."),
        })
    def __str__(self):
        return str(self.user) + ' ' + str(self.amount)

class Expanse(models.Model):
    amount = models.IntegerField()
    title = models.CharField(max_length=50)
    discription  = models.CharField(max_length = 300)
    date = models.DateTimeField(default=timezone.now)
    paid = models.CharField(max_length=1,choices=EXPANSES_PAYMENT_CHOICES,default='U')
    status = models.CharField(max_length=1,choices=TRANSFER_STATUS_CHOICES,default='U')
    def __str__(self):
        return str(self.title)

class Record(models.Model):
    name = models.CharField(max_length=7, default='record', unique=True)
    total_points = models.IntegerField(default=0)
    total_income = models.IntegerField(default=0)
    total_expanses = models.IntegerField(default=0)
    total_paid_expanses = models.IntegerField(default=0)
    def __str__(self):
        return str(self.name)
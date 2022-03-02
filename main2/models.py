from django.utils import timezone
from django.db import models
from main.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator

class Library(models.Model):
    name = models.CharField(max_length=50,default='')
    library_fee = models.IntegerField(default = 0,validators=[MaxValueValidator(100),MinValueValidator(0)])
    def __str__(self):
        return str(self.name)

class Transfer(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,null = True)
    points = models.IntegerField("النقاط",null = True)
    amount = models.IntegerField("قيمة الحوالة")
    library = models.ForeignKey(Library,on_delete=CASCADE,null=True)
    library_fee = models.IntegerField(default = 0)
    receipt_number = models.CharField("رقم الايصال",max_length=20, blank=True, error_messages={
            'unique': ("تم ارسال رقم هذا الايصال مسبقاً."),
        })
    def __str__(self):
        return str(self.user) + ' ' + str(self.amount)

class Expanse(models.Model):
    amount = models.IntegerField()
    discription  = models.CharField(max_length = 300)
    date = models.DateTimeField(default=timezone.now)
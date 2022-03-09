from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import IntegerField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.exceptions import ValidationError

# class Record(models.Model):
#     total_points = models.IntegerField()
#     total_income = models.IntegerField()
#     total_expanses = models.IntegerField()

class Author(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("حجم الصورة يجب ان تكون اصغر من %sMB" % str(megabyte_limit))
    name = models.CharField(max_length=100)
    total_points = models.IntegerField(default = 0)
    total_income = models.IntegerField(default = 0)
    extracted = models.IntegerField(default = 0)
    left = models.IntegerField(default = 0)
    description = models.CharField(max_length=1000,default="")
    image = models.ImageField(upload_to = "images/",validators=[validate_image],blank=True)
    #taxes = models.IntegerField(default = 0) #todo make it percent
    def __str__(self):
        return self.name

class Lecture(models.Model):
    name = models.CharField(max_length=60)
    code_name = models.CharField(max_length=200,default='code_name')
    author = models.ForeignKey(Author,on_delete=SET_NULL,null=True)
    price = models.IntegerField(default=10000)
    date_added = models.DateTimeField(('date added'), default=timezone.now)
    is_open = models.BooleanField(default=False)
    def __str__(self):
        return self.code_name
#    total_number_of_per

class Subject(models.Model):
    author = models.ForeignKey(Author,on_delete=SET_NULL,null=True)
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to = 'images/',help_text = 'image size must be: 25X30',blank=True)
    description = models.TextField(max_length = 165,default='')
    date_add = models.DateTimeField(('creating date'),default = timezone.now)
    lectures = models.ManyToManyField(Lecture)
    price = models.IntegerField(default=10000)
    icon = models.ImageField(help_text = 'image MUST be a square',upload_to = 'images/',blank=True)
    year = models.IntegerField(default=1)
    def __str__(self):
        return self.name

class Video(models.Model):
    lecture = models.ForeignKey(Lecture,on_delete=SET_NULL,null=True)
    order_in_lecture = models.IntegerField(default=1)
    name = models.CharField(max_length=60)
    code_name = models.CharField(max_length=200,default='code_name')
    embed = models.CharField(max_length = 500,blank=True,default='')
    low = models.CharField(max_length=300,blank=True)
    medium = models.CharField(max_length=300,blank=True)
    high = models.CharField(max_length=300,blank=True)
    def __str__(self):
        return self.code_name

class User(AbstractUser):
    email = models.EmailField("البريد الاكتروني", unique = True)
    phone = PhoneNumberField("رقم الهاتف",null = True, unique = True)
    points = models.IntegerField("النقاط",default=0,blank = True)
    verify_code = models.CharField(max_length = 10,default='-1',blank=True)
    verified = models.BooleanField(default=True)
    REQUIRED_FIELDS = ['email','first_name','last_name','points','phone']
    def __str__(self):
        return self.username + ' ' + self.first_name + ' ' + self.last_name

class UserLecture(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    lecture = models.ForeignKey(Lecture,on_delete=CASCADE)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.user) + ' ' + str(self.lecture)

class PointsPrice(models.Model):
    created = models.DateTimeField(default=timezone.now)
    point_price = IntegerField(default=100)

# class UsersTransaction(models.Model):
#     user_id = models.ForeignKey(User,on_delete=SET_NULL,null=True)
#     points = models.IntegerField()
#     price = models.IntegerField()
#     date = models.DateTimeField(default = timezone.now)

# class AuthorsTransaction(models.Model):
#     author_id = models.ForeignKey(Author)
#     points = models.IntegerField()
#     price = models.IntegerField()
#     date = models.DateTimeField(default = timezone.now)


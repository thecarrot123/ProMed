from re import search
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Lecture, PointsPrice, User, Subject, Author, UserLecture, Video

class SubjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('lectures',)
    readonly_fields = ['show_image']
    def show_image(self, obj):
        return  mark_safe('<img src="{url}" width="100" height=120/>'.format(url =obj.image.url))

class AuthorAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['name','description','total_points','total_income','extracted','left'],
        }),
        ('Image', {
            'fields': ['image','show_image'],
        })
    )
    readonly_fields = ['total_income','extracted','left','show_image']
    def show_image(self, obj):
        return  mark_safe('<img src="{url}" width="100" height=120/>'.format(url =obj.image.url))

class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('معلومات المستخدم', {
            'fields': ['username','first_name','last_name','email','password','phone','date_joined','last_login'],
        }),
        ('معلومات الحساب', {
            'fields': ['points','verify_code','verified'],
        })
    )
    search_fields = ['username']

admin.site.register(User,UserAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Video)
admin.site.register(Lecture)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(UserLecture)
admin.site.register(PointsPrice)
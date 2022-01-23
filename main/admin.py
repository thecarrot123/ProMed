from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Lecture, PointsPrice, Transfer, User, Subject, Author, UserLecture, Video

class TransferAdmin(admin.ModelAdmin):
    readonly_fields = ['show_image']
    def show_image(self, obj):
        return  mark_safe('<img src="{url}" width="100" height=120/>'.format(url =obj.image.url))

class SubjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('lectures',)
    readonly_fields = ['show_image']
    def show_image(self, obj):
        return  mark_safe('<img src="{url}" width="100" height=120/>'.format(url =obj.image.url))


admin.site.register(User)
admin.site.register(Author)
admin.site.register(Video)
admin.site.register(Lecture)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(UserLecture)
admin.site.register(PointsPrice)
admin.site.register(Transfer,TransferAdmin)
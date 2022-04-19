from pydoc import describe
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from main.models import PointsPrice
from django.urls import reverse
from django.utils.html import format_html

from main2.models import AlharamTransfer, Library, LibraryTransfer, Expanse, Record

@admin.action(description='Confirm selected transfers')
def AlharamConfirm(modeladmin, request, queryset):
    for obj in queryset:
        if obj.status == 'U':
            point_price = PointsPrice.objects.latest('created').point_price
            obj.user.points = obj.user.points + obj.amount / point_price
            obj.user.save()
            
    queryset.update(status = 'C')

@admin.action(description='Confirm selected transfers')
def LibraryConfirm(modeladmin, request, queryset):
    for obj in queryset:
        if obj.status == 'U':
            point_price = PointsPrice.objects.latest('created').point_price
            expanse = Expanse (
                amount = (obj.amount / point_price) * obj.library_id.library_fee / 100,
                title = "ضريبة تحويل عم طريق مكتبة",
                discription = "ضريبة تحويل لمكتبة <" + str(obj.library_id) + "> بمقدار " + str((obj.amount / point_price) * obj.library_id.library_fee / 100),
                )
            expanse.save()
            obj.user.points = obj.user.points + obj.amount / point_price
            obj.user.save()
            
    queryset.update(status = 'C')

class AlharamTransferAdmin(admin.ModelAdmin):
    readonly_fields = ['amount','points','status']
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
    }
    list_display = ['user', 'amount', 'status']
    actions = [AlharamConfirm]

class LibraryTransferAdmin(admin.ModelAdmin):
    fields = ['user','library_id','amount','points','status']
    readonly_fields = ['amount','points','status']
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
    }
    list_display = ['user', 'amount', 'status']
    actions = [LibraryConfirm]


@admin.action(description='Mark selcted expanses as paid')
def ExpansePay(modeladmin, request, queryset):
    for obj in queryset:
        if obj.paid == 'U':
            rec = Record.objects.last()
            rec.total_paid_expanses = rec.total_paid_expanses + obj.amount
            rec.save()
            obj.paid = 'P'
            obj.save()

@admin.action(description='Mark selcted expanses as confirmed')
def ExpanseConfirm(modeladmin, request, queryset):
    for obj in queryset:
        if obj.status == 'U':
            rec = Record.objects.last()
            rec.total_expanses = rec.total_expanses + obj.amount
            rec.save()
            obj.status = 'C'
            obj.save()


class ExpanseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
    }
    list_display = ['title','amount','paid','status']
    actions = [ExpansePay,ExpanseConfirm]

admin.site.register(AlharamTransfer,AlharamTransferAdmin)
admin.site.register(LibraryTransfer,LibraryTransferAdmin)
admin.site.register(Library)
admin.site.register(Expanse,ExpanseAdmin)
admin.site.register(Record)

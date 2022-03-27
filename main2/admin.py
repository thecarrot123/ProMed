from pydoc import describe
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from main2.models import AlharamTransfer, Library, LibraryTransfer, Expanse

@admin.action(description='Mark selected transfer as confirmed')
def AlharamConfirm(modeladmin, request, queryset):
    queryset.update(status = 'C')

@admin.action(description='Mark selected transfer as confirmed')
def LibraryConfirm(modeladmin, request, queryset):
    for obj in queryset:
        if obj.status == 'U':
            expanse = Expanse(
                amount = obj.amount * obj.library_id.library_fee / 100,
                title = "ضريبة تحويل عم طريق مكتبة",
                discription = "ضريبة تحويل لمكتبة <" + str(obj.library_id) + "> بمقدار " + str(obj.amount * obj.library_id.library_fee / 100),
                )
            expanse.save()
    queryset.update(status = 'C')

class AlharamTransferAdmin(admin.ModelAdmin):
    readonly_fields = ['amount','points','status']
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
    }
    list_display = ['user', 'amount', 'status']
    actions = [AlharamConfirm]

class LibraryTransferAdmin(admin.ModelAdmin):
    readonly_fields = ['amount','points','status']
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
    }
    list_display = ['user', 'amount', 'status']
    actions = [LibraryConfirm]

class ExpanseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
    }

admin.site.register(AlharamTransfer,AlharamTransferAdmin)
admin.site.register(LibraryTransfer,LibraryTransferAdmin)
admin.site.register(Library)
admin.site.register(Expanse,ExpanseAdmin)

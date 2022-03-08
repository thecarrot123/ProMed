from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from main2.models import AlharamTransfer, Library, LibraryTransfer

# Register your models here.

class TransferAdmin(admin.ModelAdmin):
    readonly_fields = ['amount','points']
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
    }


admin.site.register(AlharamTransfer,TransferAdmin)
admin.site.register(LibraryTransfer,TransferAdmin)
admin.site.register(Library)

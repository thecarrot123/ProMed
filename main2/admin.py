from django.contrib import admin

from main2.models import AlharamTransfer, Library, LibraryTransfer

# Register your models here.

admin.site.register(AlharamTransfer)
admin.site.register(LibraryTransfer)
admin.site.register(Library)

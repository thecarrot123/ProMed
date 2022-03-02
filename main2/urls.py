from django.urls import path
from django.urls.conf import include

from main2.views import LibraryView, TransferDescriptionView, TransferFromAlharamView, TransferFromLibraryView



urlpatterns = [
    path('alharamtransfer/',TransferFromAlharamView),
    path('librarytransfer/',TransferFromLibraryView),
    path('transferdescription/',TransferDescriptionView),
    path('libraries/',LibraryView),
]
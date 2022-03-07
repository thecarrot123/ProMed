from rest_framework import serializers
from main2.models import AlharamTransfer, Library, LibraryTransfer

class TransferFromAlharamSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlharamTransfer
        fields = ['user','receipt_number','amount']
        extra_kwargs = {
            'receipt_number': {'required': True},
            'amount': {'required': True},
        }

class TransferFromLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryTransfer
        fields = ['user','library','amount']
        extra_kwargs = {
            'library': {'required': True},
            'amount': {'required': True},
        }

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id','name']
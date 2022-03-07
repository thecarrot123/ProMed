from rest_framework import serializers
from main2.models import Library, Transfer

class TransferFromAlharamSerializer(serializers.ModelSerializer):
    #image = Base64ImageField(max_length=None,represent_in_base64 = True)
    class Meta:
        model = Transfer
        fields = ['user','receipt_number','amount']
        extra_kwargs = {
            'receipt_number': {'required': True},
            'amount': {'required': True},
        }

class TransferFromLibrarySerializer(serializers.ModelSerializer):
    #image = Base64ImageField(max_length=None,represent_in_base64 = True)
    class Meta:
        model = Transfer
        fields = ['user','library','amount']
        extra_kwargs = {
            'library': {'required': True},
            'amount': {'required': True},
        }

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id','name']
from rest_framework import serializers
from main2.models import Library, Transfer

class TransferFromAlharamSerializer(serializers.ModelSerializer):
    #image = Base64ImageField(max_length=None,represent_in_base64 = True)
    def validate(self, attrs):
        data = super().validate(attrs)
        if(Transfer.objects.filter(receipt_number = data['receipt_number']).exists()):
            raise serializers.ValidationError(".يجب ان يكون رقم الايصال فريد. الرجاء التاكد من صحة المعلومات")
        return data
    class Meta:
        model = Transfer
        fields = ['user','receipt_number','amount']

class TransferFromLibrarySerializer(serializers.ModelSerializer):
    #image = Base64ImageField(max_length=None,represent_in_base64 = True)
    def validate(self, attrs):
        data = super().validate(attrs)
        return data
    class Meta:
        model = Transfer
        fields = ['user','library','amount']

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id','name']
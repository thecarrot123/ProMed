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
    library = serializers.CharField(max_length = 300)
    class Meta:
        model = LibraryTransfer
        fields = ['user','library','amount']
        extra_kwargs = {
            'library': {'required': True},
            'amount': {'required': True},
        }
    def save(self):
        trans = LibraryTransfer(
            library_id = Library.objects.get( name = self.validated_data['library'] ),
            amount = self.validated_data['amount'],
            user = self.validated_data['user'],
        )
        LibraryTransfer.save(trans)
        return trans
        

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id','name']
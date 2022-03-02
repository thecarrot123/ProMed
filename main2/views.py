from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from main.models import PointsPrice
from main2.models import Library
from main2.serializers import LibrarySerializer, TransferFromAlharamSerializer, TransferFromLibrarySerializer
from main2.utils import transfer_description

@api_view(["POST",])
@permission_classes([IsAuthenticated])
def TransferFromAlharamView(request):
    user = request.user
    serializer = TransferFromAlharamSerializer(data = request.data)
    if serializer.is_valid():
        serializer.validated_data['points'] = int(serializer.validated_data['amount'] / PointsPrice.objects.latest('created').point_price)
        serializer.validated_data['user'] = user
        serializer.save()
        data = {
            'Response': 'تمت عملية التحويل بنجاح. يرجى الانتظار حتى يقوم احد المشرفين بتاكيد عملية التحويل.',
        }
        return Response(data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def TransferFromLibraryView(request):
    user = request.user
    serializer = TransferFromLibrarySerializer(data = request.data)
    if serializer.is_valid():
        serializer.validated_data['points'] = int(serializer.validated_data['amount'] / PointsPrice.objects.latest('created').point_price)
        serializer.validated_data['user'] = user
        #print(serializer.validated_data)
        serializer.save()

        data = {
            'Response': 'تمت عملية التحويل بنجاح. يرجى الانتظار حتى يقوم احد المشرفين بتاكيد عملية التحويل.',
        }
        return Response(data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LibraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

LibraryView = LibraryViewSet.as_view({'get': 'list'})

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def TransferDescriptionView(request):
    data = {
        'description': transfer_description
    }
    return Response(data,status = status.HTTP_200_OK)
    

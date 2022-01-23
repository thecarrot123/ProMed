from rest_framework.response import Response
from ProMed.settings import LAST_VERSION, DOWNLOAD_LINK
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from main.models import Subject, User, Video
from rest_framework import status, viewsets
from .serializers import CostumTokenObtainPairSerializer, EmailValidateSerializer, SubjectSerializer, SubjectsNamesSerializer, UserSerializer, VideoSerializer
from rest_framework.parsers import JSONParser, MultiPartParser
from django.db.models import Q

class SubjectsNamesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectsNamesSerializer

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer  

class CostumTokenObtainPairView(TokenObtainPairView):
    serializer_class = CostumTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        if request.version != LAST_VERSION:
            return Response({'version': 'الرجاء تحديث التطبيق من هذا الرابط:/n' + DOWNLOAD_LINK + '\n ثم اعادة المحاولة.'},status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            user = User.objects.get(Q(username__iexact=request.data['username']) | Q(email__iexact=request.data['username']))
        except User.DoesNotExist:
            return super().post(request,args,kwargs)
        if user.verified == False:
                return Response({'unverified user': 'الرجاء تاكيد البريد الاكتروني اولاً.','username': user.username},status=status.HTTP_400_BAD_REQUEST)
        return super().post(request,args,kwargs)

class EmailValidateView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmailValidateSerializer

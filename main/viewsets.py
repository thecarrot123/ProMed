from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from ProMed.settings import LAST_VERSION, DOWNLOAD_LINK
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from main.models import Author, Subject, User, Video
from rest_framework import status, viewsets
from .serializers import AuthorsSerializer, CostumTokenObtainPairSerializer, EmailValidateSerializer, SubjectSerializer, SubjectsNamesSerializer, UserSerializer, VideoSerializer
from rest_framework.parsers import JSONParser, MultiPartParser
from django.db.models import Q

class SubjectsNamesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectsNamesSerializer

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer  

class AuthorsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer

class CostumObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        if request.version != LAST_VERSION:
            return Response({'version': 'الرجاء تحديث التطبيق من هذا الرابط:/n' + DOWNLOAD_LINK + '\n ثم اعادة المحاولة.'},status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.verified == False:
            return Response({'unverified user': 'الرجاء تاكيد البريد الاكتروني اولاً.','username': user.username},status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'access': token.key,'username': user.username,'points': user.points})

class EmailValidateView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmailValidateSerializer

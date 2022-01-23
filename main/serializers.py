from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt import authentication
from main.models import Subject, User, Video, Transfer
import string,secrets
from django.db.models import Q
from drf_extra_fields.fields import Base64ImageField

def create_code():
    alphabet = string.ascii_lowercase + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    return password

def strong_password(password):
    a=0
    b=0
    c=0
    d=0
    if password == 'israel':
        return { 'status': False,
        'report': 'لا يمكن ان تكون كلمة السر فارغة.'}
    if password.isprintable() == False:
        return { 'status': False,
        'report': 'يجب ان تستوفي كلمة السر شرطين من الشروط الاتية على الاقل: ان تحتوي على حرف صغير, حرف كبير, رقم, محرف خاص.'}
    if len(password) < 8:
        return { 'status': False,
            'report': 'يجب ان تحتوي كلمة السر على ثمان محارف على الاقل.'}
    for ch in password:
        if ch.islower():
            a = 1
        elif ch.isupper():
            b = 1
        elif ch.isdigit():
            c = 1
        else:
            d = 1
    if a+b+c+d < 2:
        return { 'status': False,
            'report': 'يجب ان تستوفي كلمة السر شرطين من الشروط الاتية على الاقل: ان تحتوي على محرف صغير, محرف كبير, رقم, محرف خاص.'}
    return {'status': True}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','phone','email','password','password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def save(self):
        user = User(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            password = self.validated_data['password'],
            phone = self.validated_data['phone'],
            verify_code = create_code(),
            verified = False,
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password':'كلمتا المرور غير متطابقتان!'})
        is_strong = strong_password(password)
        if is_strong['status'] == False:
            raise serializers.ValidationError({'password': is_strong['report']})
        User.save(user)
        return user
        
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class SubjectsNamesSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    icon = Base64ImageField(max_length=None,represent_in_base64 = True, read_only=True)
    class Meta:
        model = Subject
        fields = ['id','name','author','icon']
    
class SubjectSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None,represent_in_base64 = True, read_only=True)
    class Meta:
        model = Subject
        fields = ['id','name','author','description','date_add','price','image']

class CostumTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = str(self.user.get_username())
        data['points'] = str(self.user.points)

        update_last_login(None, self.user)

        return data

class EmailValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 30)
    verify_code = serializers.CharField(max_length = 10)
    def validate(self, data):
        if User.objects.filter(username = data['username']).exists() == False:
            raise serializers.ValidationError("اسم المستخدم غير صحيح. يرجى التواصل مع احد القائمين على التطبيق لحل هذه المشكلة")
        if len(data['verify_code']) != 8:
            raise serializers.ValidationError("يجب ان يكون الرمز مكون من ثمان خانات")
        return data

class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 30)
    def validate(self, data):
        try:
            user = User.objects.get(Q(username__iexact = data['username']) | Q(email__iexact = data['username']))
        except User.DoesNotExist:
            raise serializers.ValidationError("البريد الالكتروني غير صحيح يرجى اعادة المحاولة.")
        else:
            return data
            
class ResetPasswrodSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verify_code = serializers.CharField(max_length = 10)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    def validate(self, data):
        if User.objects.filter(email = data['email']).exists() == False:
            raise serializers.ValidationError("البريد الالكتروني غير صحيح يرجى اعادة المحاولة.")
        if len(data['verify_code']) != 8:
            raise serializers.ValidationError("يجب ان يكون الرمز مكون من ثمان خانات")
        if data['password'] != data['password2']:
            raise serializers.ValidationError("كلمتا السر غير متطابقتان")
        is_strong = strong_password(data['password'])
        if is_strong['status'] == False:
            raise serializers.ValidationError({'password': is_strong['report']})
        return data

class TransferSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None,represent_in_base64 = True)
    class Meta:
        model = Transfer
        fields = ['receipt_number','full_name','amount','phone','image']

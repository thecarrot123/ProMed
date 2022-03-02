from base64 import b64encode
from django.utils import timezone
from main.models import Author, Lecture, PointsPrice, Subject, User, UserLecture, Video
from .utils import Util
from rest_framework.permissions import IsAuthenticated
from main.serializers import EmailValidateSerializer, ForgotPasswordSerializer, RegistrationSerializer, ResetPasswrodSerializer, VideoSerializer, create_code
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from datetime import timedelta
from ProMed.settings import DOWNLOAD_LINK, LAST_VERSION
from django.http import HttpResponse
from django.http import Http404


def get_owened(user):
    end_date = timezone.now()
    start_date = end_date - timedelta(days = 366)
    return UserLecture.objects.filter(user = user.id,date__range = (start_date,end_date))


@api_view(['POST',])
def registraion_view(request):
    if request.method == 'POST':
        if request.version != LAST_VERSION:
            return Response({'version': 'الرجاء تحديث التطبيق من هذا الرابط:/n' + DOWNLOAD_LINK + '\n ثم اعادة المحاولة.'},status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        
        if serializer.is_valid() and request.data['phone'] != '' and request.data['first_name'] !='' and request.data['last_name']:
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            data['response'] = 'تم تسجيل المستخدم بنجاح.'
            data['email'] = user.email
            data['username'] = user.username
            print('---------------------------------')
            print(Util.email_verifier(user))
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            if request.data['phone'] == '':
                data['phone'] ='لا يمكن لهذا الحقل ان يكون فارغاً.'
            if request.data['first_name'] == '':
                data['first_name'] ='لا يمكن لهذا الحقل ان يكون فارغاً.'
            if request.data['last_name'] == '':
                data['last_name'] ='لا يمكن لهذا الحقل ان يكون فارغاً.'
            return Response(data,status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def verify_email(request):
    if request.method == 'POST':
        serializer = EmailValidateSerializer(data = request.data)
        if serializer.is_valid():
            user = User.objects.get(username = serializer.validated_data['username'])
            if user.verify_code == serializer.validated_data['verify_code']:
                User.objects.filter(username = user.username).update(verified = True)
                User.objects.filter(username = user.username).update(verify_code = create_code())
                tok = RefreshToken.for_user(user)
                data = {
                    'response': 'Accepted Code',
                    'refresh': str(tok),
                    'access': str(tok.access_token),
                    'points': user.points
                }
                return Response(data,status=status.HTTP_202_ACCEPTED)
            data = {
                'response': 'الرمز غير صحيح.',
            }
            return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
        data = {
            'resopnse': 'Invalid data',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)



@api_view(['POST',])
def ForgotPasswordView(request):
    if request.method == 'POST':
        serializer = ForgotPasswordSerializer(data = request.data)
        if serializer.is_valid():
            user = User.objects.get(Q(username__iexact = serializer.validated_data['username']) |
             Q(email__iexact = serializer.validated_data['username']))
            data = {'email': user.email}
            Util.email_verifier(user)
            return Response(data,status=status.HTTP_200_OK)
        data = {
            'Response': 'Wrong email'
        }
        return Response(data,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def ResetPasswordView(request):
    if request.method == 'POST':
        serializer = ResetPasswrodSerializer(data = request.data)
        if serializer.is_valid():
            user = User.objects.get(email = serializer.validated_data['email'])
            if user.verify_code != serializer.validated_data['verify_code']:
                data = {
                    'Response': 'الرمز غير صحيح.'
                }
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            user.set_password(serializer.validated_data['password'])
            print(serializer.validated_data['password'])
            user.save()
            data = {
                'Response': 'تم تغيير كلمة السر بنجاح',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
            return Response(data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'],)
@permission_classes([IsAuthenticated])
def LecturesView(request):
    user = request.user
    course = Subject.objects.get(id = request.data['course'])
    lectures = []
    owned = get_owened(user)
    for i in course.lectures.all():
        lecture = {
            'id': i.id,
            'name': i.name,
            'price': i.price,
            'open': (i.is_open or user.is_superuser or owned.filter(lecture = i.id).exists()),
        }
        lectures.append(lecture)
    return Response(lectures)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def LectureView(request):
    user = request.user
    owned = get_owened(user)
    if (owned.filter(lecture = request.data['lecture']).exists() == False and user.is_superuser == False 
    and Lecture.objects.get(id = request.data['lecture']).is_open == False):
        return Response({'error':'UNAUTHORIZE please contact the admins'},status = status.HTTP_401_UNAUTHORIZED)
    data=[]
    videos = Video.objects.filter(lecture = request.data['lecture']).order_by('order_in_lecture')
    for i in videos:
        video = {
            'id': i.id,
            'name': i.name,
        }
        data.append(video)
    return Response(data,status = status.HTTP_200_OK)

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def VideoView(request):
    user = request.user
    owned = get_owened(user)
    video = Video.objects.get(id = request.data['video'])
    lecture = video.lecture
    if (owned.filter(lecture = lecture.id).exists() == False and user.is_superuser == False 
    and Lecture.objects.get(id = lecture.id).is_open == False):
        return Response({'error':'UNAUTHORIZE please contact the admins'},status = status.HTTP_401_UNAUTHORIZED)
    data = {}
    if video.low != '':
        data ['low']=video.low
    if video.medium != '':
        data ['medium']=video.medium
    if video.high != '':
        data ['high']=video.high
    if video.embed != '':
        data = {
            'embed':video.embed,
        }
    return Response(data,status=status.HTTP_200_OK)

# add to UserTransaction 
@api_view(['POST',])
@permission_classes([IsAuthenticated]) 
def PurchaseLectureView(request):   
    user = request.user
    lecture = Lecture.objects.get(id = request.data['lecture'])
    owned = get_owened(user)
    if owned.filter(lecture = lecture.id).exists():
        return Response({'error': 'لا يمكنك شراء ترخيص المحاضرة قبل انتهاء الترخيص السابق'},status= status.HTTP_400_BAD_REQUEST)
    if user.points < lecture.price:
        return Response({'error': 'ليس لديك رصيد كافي'},status= status.HTTP_400_BAD_REQUEST)
    user.points = user.points - lecture.price
    user.save()
    UserLecture.objects.create(user = user, lecture = lecture, date=timezone.now())
    author = Author.objects.get(id = lecture.author.id)
    author.total_points = author.total_points + lecture.price
    author.save()
    data = {
        'Response': 'تمت عملية الشراء بنجاح.',
        'points': user.points,
    }
    return Response(data,status=status.HTTP_202_ACCEPTED)

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def GetPoints(request):
    user = request.user
    data = {
        'points': user.points,
    }
    return Response(data,status=status.HTTP_200_OK)

@api_view(['GET',])
def ShareAapp(request):
    data = {
        'link': 'قم بتحميل تطبيق ProMed الطبي التعليمي مجاناََ و استفد من كورساتنا الإلكترونية المتنوعة عبر هذا الرابط:\n' + DOWNLOAD_LINK
    }
    return Response(data,status=status.HTTP_200_OK)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def VideoDetails(request):
    id = request.data['video']
    video = Video.objects.get(id = id)
    data = {
        'name': video.name 
    }
    if Video.objects.filter(lecure = video.lecture,order_in_lecture = video.order_in_lecture - 1).exists():
        data['previous'] = Video.objects.get(lecure = video.lecture,order_in_lecture = video.order_in_lecture - 1).id
    if Video.objects.filter(lecure = video.lecture,order_in_lecture = video.order_in_lecture + 1).exists():
        data['next'] = Video.objects.get(lecure = video.lecture,order_in_lecture = video.order_in_lecture + 1).id
    return Response(data,status=status.HTTP_200_OK)

def VideoEmbedHtmlPage(request,id):
    try:
        video = Video.objects.get(id=id)
    except:
        raise Http404("الفيديو غير موجود")
    html = f"<html><body>{video.embed}</body></html>"
    return HttpResponse(html)

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def AuthorView(request):
    author = Author.objects.get(id = request.data['id'])
    data = {
        'name': author.name,
        'description': author.description,
        'image': b64encode(author.image.read())
    }
    return Response(data,status = status.HTTP_200_OK)
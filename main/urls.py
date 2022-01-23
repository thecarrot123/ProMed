from main.viewsets import CostumTokenObtainPairView, SubjectViewSet
from django.urls import path
from django.urls.conf import include
from .views import GetPoints, LecturesView, ForgotPasswordView, PurchaseLectureView, ResetPasswordView, LectureView, ShareAapp, TransferView, VideoDetails, VideoView, registraion_view, verify_email, VideoEmbedHtmlPage
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .viewsets import EmailValidateView, SubjectViewSet, SubjectsNamesViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('subjects',SubjectsNamesViewSet)
router.register('subject',SubjectViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('registration/' ,registraion_view, name = 'registration'),
    path('verify_email/', verify_email, name='verify_email'),
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', CostumTokenObtainPairView.as_view(), name='login'),
    path('lecture/',LectureView),
    path('forgot_password/',ForgotPasswordView),
    path('reset_password/',ResetPasswordView),
    path('lectures/',LecturesView),
    path('video/',VideoView),
    path('purchase_lecture/',PurchaseLectureView),
    path('transfer/',TransferView),
    path('points/',GetPoints),
    path('share/',ShareAapp),
    path('details/',VideoDetails),
    path('video_embed_html_page/<int:id>/',VideoEmbedHtmlPage)
]

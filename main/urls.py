from main.viewsets import AuthorsViewSet, SubjectViewSet, CostumObtainAuthToken, SubjectViewSet, SubjectsNamesViewSet
from django.urls import path
from django.urls.conf import include
from main.views import GetPoints, LecturesView, ForgotPasswordView, PurchaseLectureView, ResetPasswordView, LectureView, ShareAapp, VideoDetails, VideoView, registraion_view, verify_email, VideoEmbedHtmlPage
from rest_framework import routers

router = routers.DefaultRouter()
router.register('subjects',SubjectsNamesViewSet)
router.register('subject',SubjectViewSet)
router.register('authors',AuthorsViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('registration/' ,registraion_view, name = 'registration'),
    path('verify_email/', verify_email, name='verify_email'),
    path('login/', CostumObtainAuthToken.as_view(), name='login'),
    path('lecture/',LectureView),
    path('forgot_password/',ForgotPasswordView),
    path('reset_password/',ResetPasswordView),
    path('lectures/',LecturesView),
    path('video/',VideoView),
    path('purchase_lecture/',PurchaseLectureView),
    path('points/',GetPoints),
    path('share/',ShareAapp),
    path('details/',VideoDetails),
    path('video_embed_html_page/<int:id>/',VideoEmbedHtmlPage),
]

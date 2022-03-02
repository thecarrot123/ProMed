from ProMed.settings import EMAIL_HOST_USER
from main.serializers import create_code
from main.models import User
from django.core.mail import send_mail


class Util:
    @staticmethod
    def send_email(data):
        return send_mail(subject=data['subject'],message=data['body'],recipient_list=[data['email'],],fail_silently=False,from_email=EMAIL_HOST_USER)


    @staticmethod
    def email_verifier(user):
        User.objects.filter(username = user.username).update(verify_code = create_code())
        user = User.objects.get(username = user.username)
        sdata = {'body': 'مرحبا بك الدكتور/ة '+ user.first_name + ' ' + user.last_name +' المحترم/ة,\n رمز التفعيل الخاص بك: \n' + user.verify_code,
        'email': user.email, 'subject': 'Verify your email'} #todo
        return Util.send_email(sdata)

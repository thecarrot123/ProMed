from main.serializers import create_code
from main.models import User
from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['subject'],body=data['body'],to=[data['email'],])
        email.send()

    @staticmethod
    def email_verifier(user):
        User.objects.filter(username = user.username).update(verify_code = create_code())
        user = User.objects.get(username = user.username)
        sdata = {'body': 'مرحبا بك الدكتور/ة '+ user.first_name + ' ' + user.last_name +' المحترم/ة,\n رمز التفعيل الخاص بك: \n' + user.verify_code,
        'email': user.email, 'subject': 'Verify your email'} #todo
        Util.send_email(sdata)

from django.core.mail import EmailMessage
from main.models import User
import string,secrets

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['subject'],body=data['body'],to=[data['email'],])
        email.send()

    @staticmethod
    def email_verifier(user):
        User.objects.filter(username = user.username).update(verify_code = create_code())
        user = User.objects.get(username = user.username)
        sdata = {
            'body': 'مرحبا بك الدكتور/ة '+ user.first_name + ' ' + user.last_name +' المحترم/ة,\n رمز التفعيل الخاص بك: \n' + user.verify_code,
            'email': user.email, 
            'subject': 'Verify your email'
        }
        Util.send_email(sdata)

def create_code():
    password = ''.join(secrets.choice(string.digits) for i in range(6))
    return password

def strong_password(password):
    a=0
    b=0
    c=0
    d=0
    if password == 'israel':
        return { 'status': False,
        'report': 'لا يمكن ان تكون كلمة السر فارغة.'}
        #password can't be empty string
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
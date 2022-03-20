from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import User, Merchandise, Image
import random
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from testdj import settings
# Create your views here.
def index(request):
    
    return render(request, 'mainpage.html')

def reg(request):
    
    if request.method == 'POST':
        flag = request.POST.get('submit')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(email, username, password)

        # check whether this email or username has been used
        p = User.objects.raw('SELECT * FROM user a WHERE a.name=\'%s\' or a.email=\'%s\'' % (username, email))
        if len(p) != 0:
            print('Used email or name')
            return render(request, 'registration.html')    #end check

        # when user click submit
        if flag == 'yes':
            print(flag)
            #compare the sent_veriCode and input_veriCode
            input_veriCode = request.POST.get('verify')
            sent_veriCode=request.POST.get('sent_veriCode')
            for x in range(len(sent_veriCode)):
                if sent_veriCode[x] != input_veriCode[x]:
                    print("Verification Failed, click SEND again to get another email")
                    return render(request, 'registration.html', locals())
            #store the user information into database
            user = User()
            user.sid = email[0:10]
            user.name = username
            user.email = email
            user.password = password
            user.save()
            return render(request, 'registration.html', locals())

        # when user click send
        else:
            #randomly get a sent_vericode
            sent_veriCode = '%d%d%d%d%d%d' % (
            random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9),
            random.randint(0, 9), random.randint(0, 9))
            subject = 'CuSell VeriCode'
            message = '[CuSell] Your Verification Code for resgistrition is %s.\nUse this code to finish registrition' %sent_veriCode + '\n\nPlease ignore this mail if it is not performed by yourself.' + '\n\nIf there is any confusion or recommandation, please feel free to contact us at cusell2022@163.com'
            #send email to the user
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            return render(request, 'registration.html', locals())

    if request.method == 'GET':
        return render(request, 'registration.html')



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)

        # check whether such a user exist
        users = User.objects.all(email=email)
        if len(user)==0:
            print('no such user,please regisiter')
        else:
            for user in users:

                #check whether the email match the password
                if user.password == password:
                    print('Logined in')
                    break
                else:
                    print('Wrong password! Please Try Again to use "Get Back Password"')
                    break
    return render(request,'login.html')

def error(request):
    return render(request,'error.html')

def profile(request):
    if request.method == 'GET':
        return render(request, 'profile.html')

    elif request.method == 'POST':
        user_id = request.GET.get('')
        try:
            user = User.objects.get(sid=user_id)
        except Exception as e:
            print('Get user error is %s' % e)
    return render(request,'profile.html',locals())
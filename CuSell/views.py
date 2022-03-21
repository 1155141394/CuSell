from django.shortcuts import redirect, render
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
        submit_button = request.POST.get('submit')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(email, username, password)

        # check whether this email or username has been used
        check_user = User.objects.raw('SELECT * FROM user a WHERE a.email=\'%s\'' % email)
        if len(check_user) != 0:
            print('Used email, please try to get back your preset password')
            return render(request, 'registration.html')    #end check

        # when user click submit
        if submit_button == 'yes':
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
    error = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # check whether such a user exist
        try:
            user = User.objects.get(email=email)

            # check whether the email match the password
            if user.password == password:
                print('Logined in')
                rep = redirect('/templates/profile.html/')
                #set the cookie that user has been login (max_age's unit is second)
                rep.set_cookie('is_login',True,max_age=2000)
                rep.set_cookie('sid',email[0:10],max_age=2000)
                return rep
            else:
                error = 'Wrong password! Please Try Again or click Forget? button'
                print('Wrong password! Please Try Again or use "Get Back Password"')

        except Exception as e:
            error = 'No such user, try again or sign up'
            print('No such user, try again or sign up')
            return render(request,'login.html',locals())

    return render(request,'login.html',locals())

def error(request):
    return render(request,'error.html')

def profile(request):
    error = ''
    #check whether user is login
    is_login = request.COOKIES.get('is_login')
    #if not, get back to login page
    if not is_login:
        print('user have not login ')
        error = 'User has not login, please log in or sign up your account first'
        return render(request,'mainpage.html',locals())

    if request.method == 'GET':
        #get the user information from cookie and database
        sid = request.COOKIES.get('sid')
        print(sid)
        return render(request, 'profile.html')

    elif request.method == 'POST':
        user_id = request.GET.get('')
        try:
            user = User.objects.get(sid=user_id)
        except Exception as e:
            print('Get user error is %s' % e)
    return render(request,'profile.html',locals())
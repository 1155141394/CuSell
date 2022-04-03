from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from .models import User, Merchandise, Liked
import random
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from testdj import settings
import numpy as np

def merch_order():
    # Get all merchandise
    all_merchandise = Merchandise.objects.all()
    # Get a random list of merchandise id
    number = len(all_merchandise)
    user_view_order = np.arange(number)
    for x in range(number):
        user_view_order[x] = all_merchandise[x].mid
    np.random.shuffle(user_view_order)
    # Get first 6 merchandise according to the user_view_order
    runout = False
    return user_view_order

user_view_order = merch_order()
count = 0   # Count indicates how many times user clicks "show more"

# Up is global variable

# Create your views here.
def index(request):
    dict = {
        'error': ''
    }
    # get the user information from cookie and database
    user_id = request.COOKIES.get('sid')
    try:
        user = User.objects.get(sid=user_id)
    except Exception as e:
        print('Get user error is %s ' % e)
    
    
    if request.method == 'GET':
        # Initialize global count to 6 
        count = 6
        # Merchandise is a list
        merchandise = []
        for order in user_view_order:
            tmpt = Merchandise.objects.get(mid = order)
            merchandise.append(tmpt)
            if len(merchandise) == count:
                break
        return render(request, 'mainpage.html', locals())

    # Get the post information from front end.
    elif request.method == 'POST':
        
        # If user click signout
        if 'signout' in request.POST:
            rep = redirect('/templates/mainpage.html/')
            rep.set_cookie('is_login', 'False')
            rep.delete_cookie("sid")
            return rep

        if 'show_more' in request.POST:
            count = int(request.POST.get('count'))
            print(count)
            if count >= len(user_view_order) + 6:
                dict['error'] = 'You have been browse all merchandises'
            merchandise = []
            for order in user_view_order:
                tmpt = Merchandise.objects.get(mid = order)
                merchandise.append(tmpt)
                if len(merchandise) == count:
                    break
    return render(request, 'mainpage.html',locals())


def reg(request):
    dict = {
        'error': ''
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(email, username, password)

        # Check whether this email or username has been used
        check_user = User.objects.raw('SELECT * FROM user a WHERE a.email=\'%s\'' % email)
        if len(check_user) != 0:
            print('Used email, please try to get back your preset password')
            dict['error'] = 'Used email, please try to get back your preset password'
            return render(request, 'registration.html', dict)  # end check

        # When user click submit
        if 'submit' in request.POST:
            # compare the sent_veriCode and input_veriCode
            input_veriCode = request.POST.get('verify')
            sent_veriCode = request.POST.get('sent_veriCode')
            # Check the vericode and check wether user has gotten the code
            if sent_veriCode != input_veriCode or len(sent_veriCode) != 6:
                print('Verification Failed, click SEND again to get another email')
                dict['error'] = 'Verification Failed, click SEND again or use another email'
                return render(request, 'registration.html', dict)
            # Store the user information into database
            user = User()
            user.sid = email[0:10]
            user.name = username
            user.email = email
            user.password = password
            user.save()
            rep = redirect('/templates/profile.html/')
            # set the cookie that user has been login (max_age's unit is second)
            rep.set_cookie('is_login', 'True', max_age=1000)
            rep.set_cookie('sid', email[0:10], max_age=1000)
            return rep

        # When user click send
        else:
            # Randomly get a sent_vericode
            sent_veriCode = '%d%d%d%d%d%d' % (
                random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9),
                random.randint(0, 9), random.randint(0, 9))
            subject = 'CuSell VeriCode'
            message = '[CuSell] Your Verification Code for resgistrition is %s.\nUse this code to finish registrition' % sent_veriCode + '\n\nPlease ignore this mail if it is not performed by yourself.' + '\n\nIf there is any confusion or recommandation, please feel free to contact us at cusell2022@163.com'
            # Send email to the user
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            return render(request, 'registration.html', locals())

    if request.method == 'GET':
        return render(request, 'registration.html')


def login(request):
    dict = {
        'error': ''
    }
    if request.method == 'GET':
        return render(request, 'login.html', dict)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if 'forget_button' in request.POST :
            check_user = User.objects.raw('SELECT * FROM user a WHERE a.email=\'%s\'' % email)
            if len(check_user)==0:
                print('No such user, try again')
                dict['error'] = 'No such user, try again'
            else:
                dict['error'] = 'info'
                for x in check_user:
                    subject = 'CuSell Password'
                    message = '[CuSell] Please ignore this emain if the operation is not done by yourself!\nYour Passowrd is %s.\nUse this code to login' % x.password + '\n\nIf there is any confusion or recommandation, please feel free to contact us at cusell2022@163.com'
                    # Send email to the user
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                    break
            return render(request, 'login.html', dict)
        # Check whether such a user exist
        try:
            user = User.objects.get(email=email)

            # Check whether the email match the password
            if user.password == password:
                print('Logined in')
                rep = redirect('/templates/profile.html/')
                # Set the cookie that user has been login (max_age's unit is second)
                rep.set_cookie('is_login', 'True', max_age=1000)
                rep.set_cookie('sid', email[0:10], max_age=1000)
                return rep
            else:
                dict['error'] = 'Wrong password! Please Try Again or click Forget? button'
                print('Wrong password! Please Try Again or use "Get Back Password"')
                return render(request, 'login.html', dict)

        except Exception as e:
            dict['error'] = 'No such user, try again or sign up'
            print('No such user, try again or sign up')
            return render(request, 'login.html', dict)


def error(request):
    return render(request, 'error.html')


def profile(request):
    # Check whether user is login
    is_login = request.COOKIES.get('is_login')
    # If not, get back to login page
    print(is_login)
    if is_login != 'True':
        print('user have not login')
        rep = redirect('/templates/login.html/')
        return rep

    # Return the profile page and user information back to front end
    if request.method == 'GET':
        # get return page
        # get user_id from cookie
        user_id = request.COOKIES.get('sid')
        try:
            # get user object and merchandise_set from database
            user = User.objects.get(sid=user_id)
            merchandises = user.merchandise_set.all()
        except Exception as e:
            print('Get user error is %s ' % e)
        # return the page and user information and merchandise information
        return render(request, 'profile.html', locals())

    elif request.method == 'POST':
        # If user click signout
        if 'signout' in request.POST :
            rep = redirect('/templates/mainpage.html/')
            rep.set_cookie('is_login','False')
            rep.delete_cookie("sid")
            return rep
        

        user_id = request.COOKIES.get('sid')
        try:
            user = User.objects.get(sid=user_id)
        except Exception as e:
            print('Get user error is %s' % e)
        # Update user introduction
        if request.POST.get('introduction') is not None:
            new_introduction = request.POST.get('introduction')
            user.introduction = new_introduction
        # Update user name
        elif request.POST.get('name') is not None:
            new_name = request.POST.get('name')
            user.name = new_name
        # Update user portrait
        elif request.FILES.get('img') is not None:
            new_portrait = request.FILES['img']
            if user.portrait == 'default/default.jpg':
                user.portrait = new_portrait
            else:
                user.portrait.delete()
                user.portrait = new_portrait
        # Update user password
        elif request.POST.get('new_password') is not None:
            new_password = request.POST.get('new_password')
            user.password = new_password
        user.save()
        rep = redirect('/templates/profile.html')
    return rep


# Test for the picture uploading
def test_upload(request):
    if request.method == 'GET':
        return render(request, 'test_upload.html')
    elif request.method == 'POST':
        title = request.POST['title']
        myfile = request.FILES['my_file']
        User.objects.create(sid=3, portrait=myfile)
        return HttpResponse('Success')

def post_mech(request):
    # Check whether user is login
    is_login = request.COOKIES.get('is_login')
    # If not, get back to login page
    if is_login != 'True':
        print('user have not login')
        rep = redirect('/templates/login.html/')
        return rep

    # Return the post page and user information back to front end
    if request.method == 'GET':
        # Get the user information from cookie and database
        user_id = request.COOKIES.get('sid')
        try:
            user = User.objects.get(sid=user_id)
        except Exception as e:
            print('Get user error is %s ' % e)
        return render(request, 'post.html', locals())

    elif request.method == 'POST':
        # If user click signout
        if 'signout' in request.POST :
            rep = redirect('/templates/mainpage.html/')
            rep.set_cookie('is_login', 'False')
            rep.delete_cookie("sid")
            return rep
        # Get the merchandise information from front end
        user_id = request.COOKIES.get('sid')
        merchandise_name=request.POST.get('postName')
        price = request.POST.get('postPrice')
        keyword = request.POST.get('postKeyword')
        description = request.POST.get('description')
        image_1 = request.FILES.get('pic-1')
        image_2 = request.FILES.get('pic-2')
        image_3 = request.FILES.get('pic-3')
        image_4 = request.FILES.get('pic-4')
        # Put the information into database
        merchandise = Merchandise()
        merchandise.sid_id = user_id
        merchandise.name = merchandise_name
        merchandise.price = price
        merchandise.keyword = keyword
        merchandise.description = description
        merchandise.image_1 = image_1
        merchandise.image_2 = image_2
        merchandise.image_3 = image_3
        merchandise.image_4 = image_4
        merchandise.save()
        # After user post the merhcandise, refresh the global order
        global user_view_order 
        user_view_order = merch_order()
        rep = redirect('/templates/profile.html/')
        return rep
    return render(request, 'post.html')

# user can view his saved merchandise in "Like"/"Shopping Cart"
def Like(request):
    # Check whether user is login
    is_login = request.COOKIES.get('is_login')
    # If not, get back to login page
    if is_login != 'True':
        print('user have not login')
        rep = redirect('/templates/login.html/')
        return rep
    # Return first 6 Liked Merchandise when first open this
    if request.method == 'GET':
        sid = request.COOKIES.get('sid')
        show_number = 0;    # show_number indicates how many merchandises will be shown in Like
        all_liked = Liked.objects.raw("select * from Liked where sid = %s"%sid)     # all_liked contains all merchandises liked by this sid
        total = len(all_liked)  # total indicates how many merhchandises this sid like.
        like = [];  # like will contain the merchandise return to client
        # if this sid like less than 6 merchandise
        if total<6:
            show_number = total
            like = all_liked[:total]
            return render(request, 'like.html',locals())
        # if this sid like more than 6 merchandise
        else:
            show_number = 6
            like = all_liked[:6]
            return render(request, 'like.html', locals())
    elif request.method == 'POST':
        # If user click signout
        if 'signout' in request.POST:
            rep = redirect('/templates/mainpage.html/')
            rep.set_cookie('is_login', 'False')
            rep.delete_cookie("sid")
            return rep

        # If user click Show More
        if 'show_more' in request.POST:
            sid = request.COOKIES.get('sid')
            show_number = int(request.POST.get('show_number'))      # please do increase this variable when user clicks show more
            print(show_number)
            all_liked = Liked.objects.raw(
                "select * from Liked where sid = %s" % sid)  # all_liked contains all merchandises liked by this sid
            like = []
            if show_number >= len(all_liked) + 6:
                dict['error'] = 'You have been browse all merchandises you like'
                like = all_liked
                return render(request, 'like.html',locals())
            else:
                like = all_liked[:all_liked]
                return render(request, 'like.html',locals())





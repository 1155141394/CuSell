from django.db.models import F
from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from .models import *
import random
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from testdj import settings
import numpy as np

'''
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


count = 0  # Count indicates how many times user clicks "show more"
'''

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
        user_view_order = merch_order()
        for order in user_view_order:
            good = Merchandise.objects.get(mid=order)
            merchandise.append(good)
            if len(merchandise) == count:
                break
        return render(request, 'mainpage.html', locals())

    # Get the post information from front end.
    elif request.method == 'POST':

        # If user click signout
        user_view_order = merch_order()
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
                good = Merchandise.objects.get(mid=order)
                merchandise.append(good)
                if len(merchandise) == count:
                    break
    return render(request, 'mainpage.html', locals())


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
        check_user = User.objects.filter(email=email)
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
            user_id = ''
            for letter in email:
                if letter != '@':
                    user_id = user_id + letter
                else:
                    break
            user.sid = user_id
            user.name = username
            user.email = email
            user.password = password
            user.save()
            rep = redirect('/templates/profile.html/')
            # set the cookie that user has been login (max_age's unit is second)
            rep.set_cookie('is_login', 'True', max_age=2000)
            rep.set_cookie('sid', user_id, max_age=2000)
            return rep

        # When user click send
        else:
            error = 'Vericode has been sent to your email.'
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

        if 'forget_button' in request.POST:
            check_user = User.objects.raw('SELECT * FROM user a WHERE a.email=\'%s\'' % email)
            if len(check_user) == 0:
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
                user_id = ''
                for letter in email:
                    if letter != '@':
                        user_id = user_id + letter
                    else:
                        break
                rep.set_cookie('is_login', 'True', max_age=2000)
                rep.set_cookie('sid', user_id, max_age=2000)
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
        if 'signout' in request.POST:
            rep = redirect('/templates/mainpage.html/')
            rep.set_cookie('is_login', 'False')
            rep.delete_cookie("sid")
            return rep

        user_id = request.COOKIES.get('sid')
        try:
            user = User.objects.get(sid=user_id)
        except Exception as e:
            print('Get user error is %s' % e)
        # Delete merchandise
        if 'delete' in request.POST:
            del_mid = int(request.POST.get('delete'))
            merchandise = Merchandise.objects.get(mid=del_mid)
            like_relation = Liked.objects.filter(mid=merchandise.mid)
            like_relation.delete()
            merchandise.delete()
        # Update user introduction
        if request.POST.get('introduction') is not None:
            new_introduction = request.POST.get('introduction')
            user.introduction = new_introduction
        # Update user name
        elif request.POST.get('UserName') is not None:
            new_name = request.POST.get('UserName')
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
        if 'signout' in request.POST:
            rep = redirect('/templates/mainpage.html/')
            rep.set_cookie('is_login', 'False')
            rep.delete_cookie("sid")
            return rep
        # Get the merchandise information from front end
        user_id = request.COOKIES.get('sid')
        merchandise_name = request.POST.get('postName')
        price = request.POST.get('postPrice')
        contact = request.POST.get('postContact')
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
        merchandise.contact = contact
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


# merchandise view function
def merchandise(request, mid):
    # Check whether user is login
    is_login = request.COOKIES.get('is_login')
    # If not, get back to login page
    print(is_login)
    if is_login != 'True':
        print('user have not login')
        rep = redirect('/templates/login.html/')
        return rep

    if request.method == 'GET':
        # get user information
        sid = request.COOKIES.get('sid')
        user = User.objects.get(sid=sid)
        # get merchandise information
        merchandise = Merchandise.objects.get(mid=mid)
        # put image into one list
        image = []
        # if image is not none add into list
        if merchandise.image_1 != '':
            image.append(merchandise.image_1)
        if merchandise.image_2 != '':
            print(merchandise.image_2)
            image.append(merchandise.image_2)
        if merchandise.image_3 != '':
            image.append(merchandise.image_3)
        if merchandise.image_4 != '':
            image.append(merchandise.image_4)
        # get owner information
        owner_id = merchandise.sid_id
        owner = User.objects.get(sid=owner_id)
        # check whether user has liked this merchandise
        user_liked = Liked.objects.filter(sid=sid, mid=merchandise.mid)
        if user_liked:
            isLiked = 'True'
        else:
            isLiked = 'False'
        return render(request, 'merchandise.html', locals())

    elif request.method == 'POST':
        user_id = request.COOKIES.get('sid')
        # If user click signout
        if 'signout' in request.POST:
            resp = redirect('/templates/mainpage.html/')
            resp.set_cookie('is_login', 'False')
            resp.delete_cookie("sid")
            return resp
        # if user click like button
        if request.POST.get('merchandiseLiked') == 'beLiked':
            # get the merchandise information
            merchandise = Merchandise.objects.get(mid=mid)
            merchandise.Liked = F('Liked') + 1
            # add the relation into liked table
            like_relation = Liked()
            like_relation.sid = user_id
            like_relation.mid = merchandise.mid
            like_relation.save()
            merchandise.save()
        # if user click dislike button
        if request.POST.get('merchandiseLiked') == 'beDisliked':
            # get the merchandise information
            merchandise = Merchandise.objects.get(mid=mid)
            merchandise.Liked = F('Liked') - 1
            # delete from the liked table
            like_relation = Liked.objects.filter(sid=user_id, mid=merchandise.mid)
            like_relation.delete()
            merchandise.save()
        resp = redirect('/merchandise/%d' % mid)
        return resp


def my_liked(request):
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
            like_relation = Liked.objects.filter(sid=user_id)
            merchandises = []
            for i in like_relation:
                m = Merchandise.objects.get(mid=i.mid)
                merchandises.append(m)
        except Exception as e:
            print('Get user error is %s ' % e)
        # return the page and user information and merchandise information
        return render(request, 'liked.html', locals())

    if request.method == 'POST':
        user_id = request.COOKIES.get('sid')
        user = User.objects.get(sid=user_id)
        if 'dislike' in request.POST:
            merchandise_id = int(request.POST.get('dislike'))
            merchandise = Merchandise.objects.get(mid=merchandise_id)
            merchandise.Liked = F('Liked') - 1
            merchandise.save()
            like_relation = Liked.objects.filter(sid=user_id, mid=merchandise.mid)
            like_relation.delete()
        if request.POST.get('introduction') is not None:
            new_introduction = request.POST.get('introduction')
            user.introduction = new_introduction
        # Update user name
        elif request.POST.get('userName') is not None:
            new_name = request.POST.get('userName')
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
    resp = redirect('/templates/liked.html')
    return resp



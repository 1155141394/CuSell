from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import User, Merchandise, Image
# Create your views here.
def index(request):
    
    return render(request, 'mainpage.html')

def reg(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(email,username,password) 
    return render(request,'registration.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
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





    return render(request,'profile.html',dic)
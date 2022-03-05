from django.shortcuts import render
from django.shortcuts import HttpResponse
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
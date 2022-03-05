from django.shortcuts import render

# Create your views here.
def index(request):
    
    return render(request, 'mainpage.html')

def reg(request):
    return render(request,'registration.html')

def log(request):
    return render(request,'login.html')
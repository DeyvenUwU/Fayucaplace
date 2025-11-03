from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def singUp(request):
    return render(request, 'singUp.html')

def singIn(request):
    return render(request, 'login.html')

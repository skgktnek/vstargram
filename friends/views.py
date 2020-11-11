from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# render: 어떤 템플릿을 그릴 것인지

def index(request):
    #return HttpResponse("Hello V !")
    return render(request, 'friends/index.html')

# def new(request):
#     return HttpResponse("write my posts!")

# def lists(request):
#     return HttpResponse("my_post lists!")
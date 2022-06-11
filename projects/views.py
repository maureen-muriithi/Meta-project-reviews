from re import I
from django.shortcuts import render

# Create your views here.

def index(request):
    message = 'I love Django!!'

    args = {
        "message": message,
    }

    return render(request, 'projects/index.html', args)



# from django.http import HttpResponse
from django.shortcuts import render

def index_public(request):
    return render(request, 'cbar_db/index.html')

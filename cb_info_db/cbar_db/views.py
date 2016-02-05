from django.http import HttpResponse


def index_public(request):
    return HttpResponse("Welcome to the C-Bar Horsemanship TRC information database!")

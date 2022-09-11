from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse('App Page "Apartaments"')

def categories(request, catid):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")
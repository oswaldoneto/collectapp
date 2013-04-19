from django.http import HttpResponse

def collect_config(request):
    html = "<html><body>Em desenvolvimento...</body></html>" 
    return HttpResponse(html)
from django.shortcuts import render

# Create your views here.

def snippets_page(request):
    return render(request, 'snippets.html')
from django.shortcuts import render

def index (request): 
    return render(request, 'main/index.html')
def innerpage (request): 
    return render(request, 'main/inner-page.html')
def login (request): 
    return render(request, 'main/login.html')
def portfolio (request): 
    return render(request, 'main/portfolio-details.html')

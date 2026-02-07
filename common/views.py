from django.shortcuts import render


def home_page(request):
    return render(request, "common/home.html")

def about_page(request):
    return render(request, "common/about.html")

def custom_404(request, exception):
    return render(request, "404.html", status=404)

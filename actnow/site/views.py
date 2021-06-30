from django.shortcuts import render


def index(request):
    """View function for home page of site."""

    return render(request, "index.html")

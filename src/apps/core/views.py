"""Views"""

from django.shortcuts import render


def home(request):
    """Home"""

    return render(request, 'home.html')

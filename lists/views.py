from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    """
    Доашняя страница

    :param request:
    :return:
    """

    return render(request, 'lists/home_page.html')

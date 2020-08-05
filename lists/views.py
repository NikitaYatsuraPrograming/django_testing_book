from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    """
    Доашняя страница
    :param request:
    :return:
    """

    return HttpResponse('<html><title>To-Do lists</title></html>')

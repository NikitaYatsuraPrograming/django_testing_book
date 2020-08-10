from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):
    """
    Доашняя страница

    :param request:
    :return:
    """

    return render(request, 'lists/home_page.html')


def view_list(request):
    """
    Предсставление списка
    :param request:
    :return:
    """

    items = Item.objects.all()

    return render(request, 'lists/list.html', {'items': items})


def new_list(request):
    """
    Новый список
    :param request:
    :return:
    """
    list_ = List.objects.create()

    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/единственный-в-своем-роде-список-в-мире/')

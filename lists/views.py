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


def view_list(request, pk):
    """
    Предсставление списка
    :param pk:
    :param request:
    :return:
    """
    list_ = List.objects.get(pk=pk)

    return render(request, 'lists/list.html', {'list': list_})


def new_list(request):
    """
    Новый список
    :param request:
    :return:
    """
    list_ = List.objects.create()

    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.pk}/')


def add_item(request, pk):
    """
    Добавить элемент в созданный список
    :param pk:
    :param request:
    :return:
    """

    list_ = List.objects.get(pk=pk)

    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.pk}/')

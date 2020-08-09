from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    """
    Доашняя страница

    :param request:
    :return:
    """

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()

    return render(request, 'lists/home_page.html', {'items': items})

from django.urls import path

from lists.views import home_page, view_list, new_list

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/new', new_list, name='new_list'),
    path('lists/единственный-в-своем-роде-список-в-мире/', view_list, name='view_list'),
]

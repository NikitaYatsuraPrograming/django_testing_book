from django.urls import path

from lists.views import home_page, view_list

urlpatterns = [
    path('', home_page, name='home'),
    path('lists/единственный-в-своем-роде-список-в-мире/', view_list, name='view_list'),
]

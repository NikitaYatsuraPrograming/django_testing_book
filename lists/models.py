from django.db import models


class List(models.Model):
    """
    Модель списка
    """

    pass


class Item(models.Model):
    """
    Модель задач
    """

    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

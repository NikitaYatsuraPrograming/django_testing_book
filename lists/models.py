from django.db import models


class Item(models.Model):
    """
    Модель задач
    """

    text = models.TextField(default='')

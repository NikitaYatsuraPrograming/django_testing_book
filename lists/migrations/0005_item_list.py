# Generated by Django 3.0.9 on 2020-08-10 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_remove_list_lists_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='list',
            field=models.TextField(default=''),
        ),
    ]

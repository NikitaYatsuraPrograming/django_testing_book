from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item
from urllib.parse import quote


class HomePageTest(TestCase):
    """
    Тест домашней страницы
    """

    def test_user_home_template(self):
        """
        Тест: используеся домашний шаблон
        :return:
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home_page.html')

    def test_can_save_a_POST_request(self):
        """
        Тест: можно сохранить post-запрос
        :return:
        """
        self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        Тест: переадресует после post-запроса
        :return:
        """

        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], quote('/lists/единственный-в-своем-роде-список-в-мире/'))

    def test_only_saves_items_when_necessary(self):
        """
        Тест: сохраняет элементы, только когда нужно
        :return:
        """

        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    """
    Тест: модели элемента списка
    """

    def test_saving_and_retrieving_items(self):
        """
        Тест: сохранение и получение элемента списка
        :return:
        """

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):
    """
    Тест представления списка
    """

    def test_user_list_template(self):
        """
        Тест использьзуется шаблон списка
        :return:
        """

        response = self.client.get('/lists/единственный-в-своем-роде-список-в-мире/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_all_items(self):
        """
        Тест: отображаются все элементы списка
        :return:
        """

        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/единственный-в-своем-роде-список-в-мире/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item


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
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'lists/home_page.html')


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

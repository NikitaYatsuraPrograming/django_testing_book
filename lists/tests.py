from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item, List
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


class ListAndItemModelTest(TestCase):
    """
    Тест: модели элемента списка
    """

    def test_saving_and_retrieving_items(self):
        """
        Тест: сохранение и получение элемента списка
        :return:
        """

        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)

        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    """
    Тест представления списка
    """

    def test_uses_list_template(self):
        """
        Тест использьзуется шаблон списка
        :return:
        """
        list_ = List.objects.create()

        response = self.client.get(f'/lists/{list_.pk}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        """
        Тест: отображаются элементы только для этого списка
        :return:
        """

        correct_list = List.objects.create()

        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)

        other_list = List.objects.create()

        Item.objects.create(text='item 1(new list)', list=other_list)
        Item.objects.create(text='item 2(new list)', list=other_list)

        response = self.client.get(f'/lists/{correct_list.pk}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

        self.assertNotContains(response, 'item 1(new list)')
        self.assertNotContains(response, 'item 2(new list)')

    def test_passes_correct_list_to_tamplate(self):
        """
        Тест: передается правильный шаблон
        :return:
        """

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.pk}/')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    """
    Тест нового списка
    """

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, quote(f'/lists/{new_list.pk}/'))


class NewItemTest(TestCase):
    """
    Тест нового списка
    """
    def test_can_save_a_POST_request_to_an_existing_list(self):
        """
        Тест: можно сохранить post-запрос в существующий список
        :return:
        """

        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.pk}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """
        Тест: переадресация в представление списка
        :return:
        """

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.pk}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        # quote кодирует строку в URL(пример: %b%BJ%J%)
        self.assertRedirects(response, quote(f'/lists/{correct_list.pk}/'))

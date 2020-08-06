from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):
    """
    Тест домашней страницы
    """

    def test_home_page_returns_correct_html(self):
        """
        Тест: домашняя страница возвращает правильный html
        :return:
        """

        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))

        self.assertTemplateUsed(response, 'lists/home_page.html')

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

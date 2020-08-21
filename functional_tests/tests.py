import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

MAX_WAIT = 15


class NewVisitorTest(StaticLiveServerTestCase):
    """
    Тест нового посетителя
    """

    def setUp(self):
        """
        Устаноовка
        :return:
        """

        self.browser = webdriver.Firefox(
            firefox_binary='/home/nikita/firefox/firefox'
        )

        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        """
        Демонтаж
        :return:
        """
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """
        Ожидать строку в таблице списка
        :param row_text:
        :return:
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        """
        Тест: можно начать список для одного пользователя
        :return:
        """

        self.browser.get(self.live_server_url)

        self.assertIn('To-Do lists', self.browser.title)
        header_test = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_test)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Купить павлиньи перья')

        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')

        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

    def test_multiple_users_can_starts_lists_at_different_urls(self):
        """
        Тест: многочисленные пользователи могут начать список по разным url
        :return:
        """

        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Получение уникального URL адресса
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # После мы искуственно создаем нового пользователя с полностью очищенным cookie
        # используя новый сеанс
        self.browser.quit()
        self.browser = webdriver.Firefox(
            firefox_binary='/home/nikita/firefox/firefox'
        )

        # Проходит проверка, что новый пользователь не видит списка других
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку из павлиньих перьев', page_text)

        # Новый пользователь создает свой список дел
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Прочитать книгу')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Прочитать книгу')

        # Получение уникального URL адресса
        new_users_list_url = self.browser.current_url
        self.assertRegex(new_users_list_url, '/lists/.+')
        self.assertNotEqual(new_users_list_url, edith_list_url)

        # Проверка не содержит ли он чужой список
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Прочитать книгу', page_text)

    def test_layout_and_styling(self):
        """
        Тест макета и стилевого оформления
        :return:
        """

        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Проверка на отцентрированную страницу
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # Проверка на отцентрирование списка задач
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

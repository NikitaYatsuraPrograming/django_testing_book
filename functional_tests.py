from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest


import unittest


class NewVisitorTest(unittest.TestCase):
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

    def tearDown(self):
        """
        Демонтаж
        :return:
        """
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """
        Проверка на вхождение строки в таблицу списка
        :param row_text:
        :return:
        """

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        """
        Текст: можно начать список и получить его позже
        :return:
        """

        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')

        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Купить павлиньи перья')
        self.check_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        self.fail('Закончить тест')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

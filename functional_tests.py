from selenium import webdriver

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

    def test_can_start_a_list_and_retrieve_it_later(self):
        """
        Текст: можно начать список и получить его позже
        :return:
        """

        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        self.fail('Закончить тест')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

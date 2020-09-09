from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

MAX_WAIT = 15


class NewVisitorTest(FunctionalTest):
    """
    Тест нового посетителя
    """

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

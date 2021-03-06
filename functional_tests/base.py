import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

import time

MAX_WAIT = 15


class FunctionalTest(StaticLiveServerTestCase):
    """
    Функциональный тест
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

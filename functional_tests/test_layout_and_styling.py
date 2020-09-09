from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

MAX_WAIT = 15


class LayoutAndStylingTest(FunctionalTest):
    """
    Тест макета и стилевого оформления
    """

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

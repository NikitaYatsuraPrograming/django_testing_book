from functional_tests.base import FunctionalTest

MAX_WAIT = 15


class ItemValidationTest(FunctionalTest):
    """
    Тест валидации элемента списка
    """

    def test_cannot_add_empty_list_item(self):
        """
        Тест: нельзя добавить пустые элементы списка
        :return:
        """

        self.fail('Напиши меня')

import unittest
from telegram import ReplyKeyboardMarkup, KeyboardButton
from utils.keyboard import create_keyboard  # замените на реальное имя модуля

class TestCreateKeyboard(unittest.TestCase):

    def test_single_button_per_row(self):
        categories = ["Cat1", "Cat2", "Cat3", "Cat4"]
        result = create_keyboard(categories)

        # Проверяем, что клавиатура имеет нужный формат
        self.assertEqual(len(result.keyboard), len(categories))  # каждая категория должна быть в своей строке
        self.assertEqual([button.text for button in result.keyboard[0]], ["Cat1"])
        self.assertEqual([button.text for button in result.keyboard[1]], ["Cat2"])
        self.assertEqual([button.text for button in result.keyboard[2]], ["Cat3"])
        self.assertEqual([button.text for button in result.keyboard[3]], ["Cat4"])

    def test_two_buttons_per_row(self):
        categories = ["Cat1", "Cat2", "Cat3", "Cat4"]
        result = create_keyboard(categories, two_per_row=True)

        # Проверяем, что клавиатура имеет два элемента в каждой строке
        self.assertEqual(len(result.keyboard), 2)
        self.assertEqual([button.text for button in result.keyboard[0]], ["Cat1", "Cat2"])
        self.assertEqual([button.text for button in result.keyboard[1]], ["Cat3", "Cat4"])

    def test_odd_number_of_categories(self):
        categories = ["Cat1", "Cat2", "Cat3"]
        result = create_keyboard(categories, two_per_row=True)

        # Проверяем, что клавиатура с нечетным количеством категорий добавляет одну категорию в последнюю строку
        self.assertEqual(len(result.keyboard), 2)
        self.assertEqual([button.text for button in result.keyboard[0]], ["Cat1", "Cat2"])
        self.assertEqual([button.text for button in result.keyboard[1]], ["Cat3"])

    def test_empty_categories(self):
        categories = []
        result = create_keyboard(categories)

        # Проверяем, что при пустом списке категорий, клавиатура не имеет кнопок
        self.assertEqual(len(result.keyboard), 0)

if __name__ == '__main__':
    unittest.main()

from bot import User, KeyboardLanguage, Button, Keyboard
from unittest import TestCase, main
from telegram import InlineKeyboardButton
from emoji import emojize


class TestUser(TestCase):

    def setUp(self):
        self.user = User('max', 'Madiyor', 'Abdukhashimov')


    def test_username(self):
        self.assertEqual(self.user.pr_username, 'max')

    def test_first_name(self):
        self.assertEqual(self.user.pr_first_name, 'Madiyor')

    def test_last_name(self):
        self.assertEqual(self.user.pr_last_name, 'Abdukhashimov')

    # test with integration of keyboard
    def test_default_keyboard(self):
        self.assertEqual(self.user.lang_opt.language, 'en')

    def test_set_a_new_language(self):
        new_language_option = 'ru'
        self.user.lang_opt.language = 'ru'
        self.assertEqual(self.user.lang_opt.language, 'ru')

    def test_not_available_language(self):
        not_available_language = 'kz'
        with self.assertRaises(ValueError):
            self.user.lang_opt.language = not_available_language


class TestKeyboardLanguage(TestCase):
    def setUp(self):
        self.keyboard_language = KeyboardLanguage('en')

    def test_language_option(self):
        self.assertEqual(self.keyboard_language.language, 'en')

    def test_setting_new_language(self):
        self.keyboard_language.language = 'ru'
        self.assertEqual(self.keyboard_language.language, 'ru')

    def test_setting_not_available_language(self):
        with self.assertRaises(ValueError):
            self.keyboard_language.language = 'kz'


class TestButton(TestCase):
    def setUp(self):
        self.button = Button('Logo Design', '1')

    def test_name(self):
        self.assertEqual(self.button.button_name_pr, 'Logo Design')

    def test_inline_keyboard_created(self):
        self.assertEqual(type(self.button.inline_pr), InlineKeyboardButton)

    def test_callback_data(self):
        self.assertEqual(self.button.callback_data_pr, '1')

    def test_toggle_funcionality(self):
        self.button.toggle('1')
        self.assertIn('{}'.format(emojize(':white_check_mark:',
                                          use_aliases=True)),
                      self.button.inline.text)

    def test_toggle_2_times(self):
        self.button.toggle('1')
        self.button.toggle('1')
        self.assertEqual(self.button.button_name_pr, 'Logo Design')


class TestKeyboard(TestCase):

    def setUp(self):
        self.keyboard = Keyboard()

    def test_keyboard(self):
        self.keyboard.start_keyboard()
        self.assertEqual(len(self.keyboard.get_keyboard()), 7)
        self.assertEqual(type(self.keyboard.get_keyboard()), list)

    def test_double_start(self):
        self.keyboard.start_keyboard()
        self.keyboard.start_keyboard()
        self.assertEqual(len(self.keyboard.get_keyboard()), 7)
        self.assertEqual(type(self.keyboard.get_keyboard()), list)

    def item_included(self):
        self.keyboard.start_keyboard()
        keyboard = self.keyboard.get_keyboard()
        self.assertIn('Logo Design', keyboard[0].button_name_pr)

if __name__ == "__main__":
    main()

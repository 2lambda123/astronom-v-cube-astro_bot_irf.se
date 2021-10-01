from vk_api.keyboard import VkKeyboard, VkKeyboardColor


keyboard = VkKeyboard(one_time = True)

keyboard.add_button('Графики', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Команды', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()  # Переход на вторую строку
keyboard.add_button('Сейчас', color=VkKeyboardColor.PRIMARY)

keyboard_two = VkKeyboard()

keyboard_two.add_button('Подписаться', color=VkKeyboardColor.POSITIVE)
keyboard_two.add_button('Отписаться', color=VkKeyboardColor.SECONDARY)
keyboard_two.add_button('Стоп', color=VkKeyboardColor.NEGATIVE)
keyboard_two.add_line()  # Переход на вторую строку
keyboard_two.add_button('Уровни Q', color=VkKeyboardColor.PRIMARY)
keyboard_two.add_button('Графики', color=VkKeyboardColor.PRIMARY)
keyboard_two.add_line()  # Переход на вторую строку
keyboard_two.add_button('Баг-репорт', color=VkKeyboardColor.NEGATIVE)
keyboard_two.add_button('В начало', color=VkKeyboardColor.NEGATIVE)

keyboard_three = VkKeyboard()

keyboard_three.add_button('Primary', color=VkKeyboardColor.SECONDARY)
keyboard_three.add_button('Secondary (DMI)', color=VkKeyboardColor.POSITIVE)
keyboard_three.add_line()  # Переход на вторую строку
keyboard_three.add_button('K&Q index', color=VkKeyboardColor.NEGATIVE)
keyboard_three.add_button('All graphs', color=VkKeyboardColor.PRIMARY)
keyboard_three.add_line()  # Переход на вторую строку
keyboard_three.add_button('В начало', color=VkKeyboardColor.NEGATIVE)

keyboard_four = VkKeyboard()

keyboard_four.add_button('1', color=VkKeyboardColor.SECONDARY)
keyboard_four.add_button('2', color=VkKeyboardColor.SECONDARY)
keyboard_four.add_button('3', color=VkKeyboardColor.SECONDARY)
keyboard_four.add_line()  # Переход на вторую строку
keyboard_four.add_button('4', color=VkKeyboardColor.POSITIVE)
keyboard_four.add_button('5', color=VkKeyboardColor.POSITIVE)
keyboard_four.add_button('6', color=VkKeyboardColor.POSITIVE)
keyboard_four.add_line()  # Переход на вторую строку
keyboard_four.add_button('7', color=VkKeyboardColor.PRIMARY)
keyboard_four.add_button('8', color=VkKeyboardColor.PRIMARY)
keyboard_four.add_button('9', color=VkKeyboardColor.PRIMARY)
keyboard_four.add_line()  # Переход на вторую строку
keyboard_four.add_button('Уровни Q', color=VkKeyboardColor.SECONDARY)
keyboard_four.add_button('В начало', color=VkKeyboardColor.NEGATIVE)

keyboard_five = VkKeyboard()

keyboard_five.add_button('Про 1', color=VkKeyboardColor.SECONDARY)
keyboard_five.add_button('Про 2', color=VkKeyboardColor.SECONDARY)
keyboard_five.add_button('Про 3', color=VkKeyboardColor.SECONDARY)
keyboard_five.add_line()  # Переход на вторую строку
keyboard_five.add_button('Про 4', color=VkKeyboardColor.POSITIVE)
keyboard_five.add_button('Про 5', color=VkKeyboardColor.POSITIVE)
keyboard_five.add_button('Про 6', color=VkKeyboardColor.POSITIVE)
keyboard_five.add_line()  # Переход на вторую строку
keyboard_five.add_button('Про 7', color=VkKeyboardColor.PRIMARY)
keyboard_five.add_button('Про 8', color=VkKeyboardColor.PRIMARY)
keyboard_five.add_button('Про 9', color=VkKeyboardColor.PRIMARY)
keyboard_five.add_line()  # Переход на вторую строку
keyboard_five.add_button('В начало', color=VkKeyboardColor.NEGATIVE)

keyboard_six = VkKeyboard()

keyboard_six.add_button('1', color=VkKeyboardColor.SECONDARY)
keyboard_six.add_button('2', color=VkKeyboardColor.SECONDARY)
keyboard_six.add_button('3', color=VkKeyboardColor.SECONDARY)
keyboard_six.add_line()  # Переход на вторую строку
keyboard_six.add_button('4', color=VkKeyboardColor.POSITIVE)
keyboard_six.add_button('5', color=VkKeyboardColor.POSITIVE)
keyboard_six.add_button('6', color=VkKeyboardColor.POSITIVE)
keyboard_six.add_line()  # Переход на вторую строку
keyboard_six.add_button('7', color=VkKeyboardColor.PRIMARY)
keyboard_six.add_button('8', color=VkKeyboardColor.PRIMARY)
keyboard_six.add_button('9', color=VkKeyboardColor.PRIMARY)
keyboard_six.add_line()  # Переход на вторую строку
keyboard_six.add_button('В начало', color=VkKeyboardColor.NEGATIVE)
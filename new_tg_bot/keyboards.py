from telebot import types
from emoji import emojize

standart_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
standart_keyboard.add(emojize(":chart_increasing: Графики :chart_increasing:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass_not_done: Сейчас :hourglass_not_done:"))

graphs_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
graphs_keyboard.add("Primary", "Secondary (DMI)").add("K&Q index", "All graphs")

commands_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
commands_keyboard.add(emojize(":bell: Подписаться :bell:"), emojize(":bell_with_slash: Отписаться :bell_with_slash:")).add(emojize(":bar_chart: Уровни Q :bar_chart:"), emojize(":chart_increasing: Графики :chart_increasing:")).add(emojize(":warning: Баг-репорт :warning:"), emojize(":counterclockwise_arrows_button: В начало :counterclockwise_arrows_button:"))

subscribe_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
subscribe_keyboard.add(emojize(":keycap_1:"), emojize(":keycap_2:"), emojize(":keycap_3:")).add(emojize(":keycap_4:"), emojize(":keycap_5:"), emojize(":keycap_6:")).add(emojize(":keycap_7:"), emojize(":keycap_8:"), emojize(":keycap_9:")).add(emojize(":bar_chart: Уровни Q :bar_chart:"), emojize(":counterclockwise_arrows_button: В начало :counterclockwise_arrows_button:"))

unsubscribe_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
unsubscribe_keyboard.add(emojize(":keycap_1:"), emojize(":keycap_2:"), emojize(":keycap_3:")).add(emojize(":keycap_4:"), emojize(":keycap_5:"), emojize(":keycap_6:")).add(emojize(":keycap_7:"), emojize(":keycap_8:"), emojize(":keycap_9:")).add( emojize(":counterclockwise_arrows_button: В начало :counterclockwise_arrows_button:"))

def emojize_decryption(msg):

    if msg in [emojize(":keycap_1:"), '1']:
        return (1)

    elif msg in [emojize(":keycap_2:"), '2']:
        return (2)

    elif msg in [emojize(":keycap_3:"), '3']:
        return (3)

    elif msg in [emojize(":keycap_4:"), '4']:
        return (4)

    elif msg in [emojize(":keycap_5:"), '5']:
        return (5)

    elif msg in [emojize(":keycap_6:"), '6']:
        return (6)

    elif msg in [emojize(":keycap_7:"), '7']:
        return (7)

    elif msg in [emojize(":keycap_8:"), '8']:
        return (8)

    elif msg in [emojize(":keycap_9:"), '9']:
        return (9)

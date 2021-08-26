from telebot import types
from emoji import emojize

standart_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
standart_keyboard.add(emojize(":chart_increasing: Графики :chart_increasing:"), emojize(":memo: Команды :memo:")).add(emojize(":hourglass_not_done: Сейчас :hourglass_not_done:"))

graphs_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
graphs_keyboard.add("Primary", "Secondary (DMI)").add("K&Q index", "All graphs")

commands_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
commands_keyboard.add(emojize(":bell: Подписаться :bell:")).add(emojize(":bell_with_slash: Отписаться :bell_with_slash:"), emojize(":cross_mark: Стоп :cross_mark:")).add(emojize(":bar_chart: Уровни Q :bar_chart:"), emojize(":chart_increasing: Графики :chart_increasing:")).add(emojize(":warning: Баг-репорт :warning:"), emojize(":counterclockwise_arrows_button: В начало :counterclockwise_arrows_button:"))

subscribe_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
subscribe_keyboard.add(emojize(":keycap_1:"), emojize(":keycap_2:"), emojize(":keycap_3:")).add(emojize(":keycap_4:"), emojize(":keycap_5:"), emojize(":keycap_6:")).add(emojize(":keycap_7:"), emojize(":keycap_8:"), emojize(":keycap_9:")).add(emojize(":counterclockwise_arrows_button: В начало :counterclockwise_arrows_button:"))

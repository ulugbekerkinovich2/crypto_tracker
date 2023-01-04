import telebot


def send_notify(message):
    bot = telebot.TeleBot("5821284135:AAHpPGbrqy4412hSsB2NjvO3Pib7KzwMZYI")
    bot.send_message(1791124119, message)


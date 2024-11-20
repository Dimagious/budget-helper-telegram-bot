from telegram import ReplyKeyboardMarkup

def create_keyboard(categories):
    buttons = [[category] for category in categories]
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

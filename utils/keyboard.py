from telegram import ReplyKeyboardMarkup

def create_keyboard(categories):
    buttons = [[category] for category in categories]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

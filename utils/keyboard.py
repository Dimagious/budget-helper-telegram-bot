from telegram import ReplyKeyboardMarkup

def create_keyboard(categories, two_per_row=False):
    buttons = []

    if two_per_row:
        for i in range(0, len(categories), 2):
            buttons.append(categories[i:i+2])
    else:
        buttons = [[category] for category in categories]
    
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

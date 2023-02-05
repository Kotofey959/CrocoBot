from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_back_category: KeyboardButton = KeyboardButton('⬅️ Назад к выбору категории')
button_back_iphone: KeyboardButton = KeyboardButton('⬅️ Назад к выбору модели')
button_back: KeyboardButton = KeyboardButton('⬅️ Назад')
button_start_menu: KeyboardButton = KeyboardButton('⬅️ Главное меню')
button_contact: KeyboardButton = KeyboardButton('Написать менеджеру')

# Стартовая клавиатура
start_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True,
                                                          resize_keyboard=True,
                                                          row_width=2)
button_new: KeyboardButton = KeyboardButton('Новые устройства')
button_used: KeyboardButton = KeyboardButton('Б/У Устройства')

start_keyboard.add(button_new, button_used, button_contact)

# Клавиатура выбора категории новых устройств под заказ

new_categories_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                   resize_keyboard=True,
                                                                   row_width=2)
button_iphone_new: KeyboardButton = KeyboardButton('📱 iPhone')
button_ipad_new: KeyboardButton = KeyboardButton('📲 iPad')
button_mac_new: KeyboardButton = KeyboardButton('💻 MacBook')
button_watch_new: KeyboardButton = KeyboardButton('⌚️ Watch')
button_AirPods_new: KeyboardButton = KeyboardButton('🎧 AirPods')
button_other_new: KeyboardButton = KeyboardButton('Прочие устройства')

new_categories_keyboard.add(button_iphone_new, button_ipad_new, button_mac_new, button_watch_new,
                            button_AirPods_new, button_other_new, button_back)

# Клавиатура выбора модели iPhone

iphone_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True,
                                                           resize_keyboard=True,
                                                           row_width=1)

button_iphone_11: KeyboardButton = KeyboardButton('iPhone 11/Pro/Max')
button_iphone_12: KeyboardButton = KeyboardButton('iPhone 12/Pro/Max')
button_iphone_13: KeyboardButton = KeyboardButton('iPhone 13/Pro/Max')
button_iphone_14: KeyboardButton = KeyboardButton('iPhone 14/Pro/Max')

iphone_keyboard.add(button_iphone_14, button_iphone_13, button_iphone_12, button_iphone_11, button_back_category)

# Клавиатура выбора в наличии/под заказ

choose_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True,
                                                           resize_keyboard=True,
                                                           row_width=2)

button_stock: KeyboardButton = KeyboardButton('В наличии')
button_order: KeyboardButton = KeyboardButton('Под заказ')

choose_keyboard.add(button_stock, button_order, button_start_menu)

# Возврат в главное меню или связь с менеджером

main_or_contact_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                    resize_keyboard=True,
                                                                    row_width=1)


main_or_contact_keyboard.add(button_contact, button_start_menu)

# Назад к выбору модели iPhone  или связь с менеджером

iphone_contact_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                   resize_keyboard=True,
                                                                   row_width=1)

iphone_contact_keyboard.add(button_contact, button_back_iphone)

# Назад к выбору категории или связь с менеджером

category_contact_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                     resize_keyboard=True,
                                                                     row_width=1)


category_contact_keyboard.add(button_contact, button_back_category)

# Назад к выбору Б/У/Новые или связь с менеджером

back_contact_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                 resize_keyboard=True,
                                                                 row_width=1)

back_contact_keyboard.add(button_contact, button_back)
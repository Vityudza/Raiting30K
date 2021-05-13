import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from functions import statistic_of_group
import telebot
from telebot import types

scope = ['https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

client = gspread.authorize(credentials=credentials)

sheet = client.open('Рейтинг груп').worksheet('Рейтинг')
sheet_tend = client.open('Рейтинг груп').worksheet('Тенденція')
sheet_autorization = client.open('Рейтинг груп').worksheet('Доступ')

current_day = datetime.datetime.today().date().strftime("%d-%m-%Y")
dates = []
date_range = []
chose_date_range = []

start = True
start_menu = f'1 Статистика\n2 Оцінювання\n3 Перенести бали в "Тенденція"\n4 Закінчити'
groups_menu = f'1 301\n2 302\n3 303\n4 304\n5 305\n6 306'
evaluation_menu = f'1 Зауваження з навчання\n2 Заохочення з навчання\n3 Дисципліна-\n4 Дисципліна+\n5 Порядок-\n' \
                  f'6 Порядок+\n7 Ініціатива'

bot = telebot.TeleBot('1809554263:AAFv6EmyZ-h5UREpf_ghsFBPpdLfSNbW7fo')

start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
start_markup.row('Авторизація')
start_markup.row('Допомога')
start_markup.row('Отримати доступ')

main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
main_menu_markup.row('Статистика')
main_menu_markup.row('Оцінювання')
main_menu_markup.row('Перенести бали в "Тенденція"')
main_menu_markup.row('Вихід')

groups_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
groups_menu_markup.row('301', '302')
groups_menu_markup.row('303', '304')
groups_menu_markup.row('305', '306')
groups_menu_markup.row('<--')

ev_groups_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
ev_groups_menu_markup.row('301+/-', '302+/-')
ev_groups_menu_markup.row('303+/-', '304+/-')
ev_groups_menu_markup.row('305+/-', '306+/-')
ev_groups_menu_markup.row('<--')

category_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
category_markup.row('Зауваження з навчання', 'Заохочення з навчання')
category_markup.row('Дисципліна-', 'Дисципліна+')
category_markup.row('Порядок-', 'Порядок+')
category_markup.row('Ініціатива')
category_markup.row('<-')

accept_markup = types.InlineKeyboardMarkup()
accept_markup.add(types.InlineKeyboardButton(text='+', callback_data='+'),
                  types.InlineKeyboardButton(text='-', callback_data='-'))

commands = ['авторизація', 'допомога', 'отримати доступ',
            'статистика', 'оцінювання', 'перенести бали в "тенденція"', 'вихід',
            '301', '302', '303', '304', '305', '306', '<--',
            '301+/-', '302+/-', '303+/-', '304+/-', '305+/-', '306+/-',
            'зауваження з навчання', 'заохочення з навчання', 'дисципліна-', 'дисципліна+', 'порядок-', 'порядок+', 'ініціатива', '<-']
current_group = []
pr = []


@bot.message_handler(commands=['start'])
def start(message):
    hello_message = f'<b>Редагуй таблиці рейтингу 30 навчального курсу</b>'

    bot.send_message(message.chat.id, hello_message, parse_mode='html', reply_markup=start_markup)


@bot.message_handler(content_types=['text'])
def main(message):
    user_input = message.text.strip().lower()
    list_access_id = sheet_autorization.col_values(1)
    user_id = message.chat.id

    # ДОПОМОГА
    if user_input == 'допомога':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton(
                'Написати', url='telegram.me/vit_devv'
            )
        )
        bot.send_message(
            message.chat.id, 'Якщо є питання чи пропозиції, нажміть кнопку нище', parse_mode='html',
            reply_markup=keyboard
        )

    # ОТРИМАННЯ ДОСТУПУ

    elif user_input == 'отримати доступ':
        user_first_name = message.chat.first_name
        user_last_name = message.chat.last_name
        bot.send_message(1649577403, f'<b>Запит на отримання доступу до таблиць</b>\n\n<b>ID:</b> {user_id}\n'
                                     f'<b>First-name:</b> {user_first_name}'
                                     f'\n<b>Last-name:</b> {user_last_name}')
    # АВТОРИЗАЦІЯ
    if user_input == 'авторизація' and str(user_id) not in list_access_id:
        bot.send_message(message.chat.id, f'<b>Доступ закритий, надішліть заявку для його отримання</b>',
                         parse_mode='html')
    if user_input == 'авторизація' and str(user_id) in list_access_id:
        bot.send_message(message.chat.id, f'<b>Успішна авторизація</b>\n\nВи в головному меню', parse_mode='html',
                         reply_markup=main_menu_markup)
    # СТАТИСТИКА
    if user_input == 'статистика' and str(user_id) in list_access_id:
        bot.send_message(message.chat.id, f'<b>Статистика груп</b>', parse_mode='html', reply_markup=groups_menu_markup)

    if user_input == '301' and str(user_id) in list_access_id:
        mess = statistic_of_group('301', int(user_input[-1]), sheet)
        bot.send_message(message.chat.id, mess, parse_mode='html')
    if user_input == '302' and str(user_id) in list_access_id:
        mess = statistic_of_group('302', int(user_input[-1]), sheet)
        bot.send_message(message.chat.id, mess, parse_mode='html')
    if user_input == '303' and str(user_id) in list_access_id:
        mess = statistic_of_group('303', int(user_input[-1]), sheet)
        bot.send_message(message.chat.id, mess, parse_mode='html')
    if user_input == '304' and str(user_id) in list_access_id:
        mess = statistic_of_group('304', int(user_input[-1]), sheet)
        bot.send_message(message.chat.id, mess, parse_mode='html')
    if user_input == '305' and str(user_id) in list_access_id:
        mess = statistic_of_group('305', int(user_input[-1]), sheet)
        bot.send_message(message.chat.id, mess, parse_mode='html')
    elif user_input == '306' and str(user_id) in list_access_id:
        mess = statistic_of_group('306', int(user_input[-1]), sheet)
        bot.send_message(message.chat.id, mess, parse_mode='html')
    # СТАТИСТИКА

    if user_input == 'оцінювання' and str(user_id) in list_access_id:
        bot.send_message(message.chat.id, f'Виберіть групу', reply_markup=ev_groups_menu_markup)
    if user_input == '301+/-' and str(user_id) in list_access_id:
        current_group.append(user_input[2])
        bot.send_message(message.chat.id, f'Введіть причину зміни балу, а потім виберіть категорію оцінювання', parse_mode='html',
                         reply_markup=category_markup)
    if user_input == '302+/-' and str(user_id) in list_access_id:
        current_group.append(user_input[2])
        bot.send_message(message.chat.id, f'Введіть причину зміни балу, а потім виберіть категорію оцінювання', parse_mode='html',
                         reply_markup=category_markup)
    if user_input == '303+/-' and str(user_id) in list_access_id:
        current_group.append(user_input[2])
        bot.send_message(message.chat.id, f'Введіть причину зміни балу, а потім виберіть категорію оцінювання', parse_mode='html',
                         reply_markup=category_markup)
    if user_input == '304+/-' and str(user_id) in list_access_id:
        current_group.append(user_input[2])
        bot.send_message(message.chat.id, f'Введіть причину зміни балу, а потім виберіть категорію оцінювання', parse_mode='html',
                         reply_markup=category_markup)
    if user_input == '305+/-' and str(user_id) in list_access_id:
        current_group.append(user_input[2])
        bot.send_message(message.chat.id, f'Введіть причину зміни балу, а потім виберіть категорію оцінювання', parse_mode='html',
                         reply_markup=category_markup)
    if user_input == '306+/-' and str(user_id) in list_access_id:
        current_group.append(user_input[2])
        bot.send_message(message.chat.id, f'Введіть причину зміни балу, а потім виберіть категорію оцінювання', parse_mode='html',
                         reply_markup=category_markup)

    if user_input not in commands:
        pr.append(user_input)

    if user_input == 'зауваження з навчання' and str(user_id) in list_access_id:

        try:
            bot.send_message(1649577403, f'Зміна балів\n\nГрупа: 30{current_group[0]}\nКритерій: {user_input.capitalize()}'
                                         f'\nОсоба що змінює:\nID: {message.chat.id}\nName: {message.chat.first_name} '
                                         f'{message.chat.last_name}\nПричина: {pr[0].capitalize()}')
            val = sheet.acell(f'B{int(current_group[0]) + 1}').value
            val = int(val) + 1
            sheet.update(f'B{int(current_group[0]) + 1}', str(val))
        except IndexError:
            bot.send_message(message.chat.id, f'Error', parse_mode='html', reply_markup=ev_groups_menu_markup)
        pr.clear()
    if user_input == 'заохочення з навчання' and str(user_id) in list_access_id:
        try:
            bot.send_message(1649577403,
                             f'Зміна балів\n\nГрупа: 30{current_group[0]}\nКритерій: {user_input.capitalize()}'
                             f'\nОсоба що змінює:\nID: {message.chat.id}\nName: {message.chat.first_name} '
                             f'{message.chat.last_name}\nПричина: {pr[0].capitalize()}')
            val = sheet.acell(f'C{int(current_group[0]) + 1}').value
            val = int(val) + 1
            sheet.update(f'C{int(current_group[0]) + 1}', str(val))
        except IndexError:
            bot.send_message(message.chat.id, f'Error', parse_mode='html', reply_markup=ev_groups_menu_markup)
    if user_input == 'дисципліна-' and str(user_id) in list_access_id:
        try:
            bot.send_message(1649577403,
                             f'Зміна балів\n\nГрупа: 30{current_group[0]}\nКритерій: {user_input.capitalize()}'
                             f'\nОсоба що змінює:\nID: {message.chat.id}\nName: {message.chat.first_name} '
                             f'{message.chat.last_name}\nПричина: {pr[0].capitalize()}')
            val = sheet.acell(f'D{int(current_group[0]) + 1}').value
            val = int(val) + 1
            sheet.update(f'D{int(current_group[0]) + 1}', str(val))
        except IndexError:
            bot.send_message(message.chat.id, f'Error', parse_mode='html', reply_markup=ev_groups_menu_markup)
    if user_input == 'дисципліна+' and str(user_id) in list_access_id:
        try:
            bot.send_message(1649577403,
                             f'Зміна балів\n\nГрупа: 30{current_group[0]}\nКритерій: {user_input.capitalize()}'
                             f'\nОсоба що змінює:\nID: {message.chat.id}\nName: {message.chat.first_name} '
                             f'{message.chat.last_name}\nПричина: {pr[0].capitalize()}')
            val = sheet.acell(f'E{int(current_group[0]) + 1}').value
            val = int(val) + 1
            sheet.update(f'E{int(current_group[0]) + 1}', str(val))
        except IndexError:
            bot.send_message(message.chat.id, f'Error', parse_mode='html', reply_markup=ev_groups_menu_markup)
    if user_input == 'порядок-' and str(user_id) in list_access_id:
        try:
            bot.send_message(1649577403,
                             f'Зміна балів\n\nГрупа: 30{current_group[0]}\nКритерій: {user_input.capitalize()}'
                             f'\nОсоба що змінює:\nID: {message.chat.id}\nName: {message.chat.first_name} '
                             f'{message.chat.last_name}\nПричина: {pr[0].capitalize()}')
            val = sheet.acell(f'F{int(current_group[0]) + 1}').value
            val = int(val) + 1
            sheet.update(f'F{int(current_group[0]) + 1}', str(val))
        except IndexError:
            bot.send_message(message.chat.id, f'Error', parse_mode='html', reply_markup=ev_groups_menu_markup)
    if user_input == 'порядок+' and str(user_id) in list_access_id:
        try:
            bot.send_message(1649577403,
                             f'Зміна балів\n\nГрупа: 30{current_group[0]}\nКритерій: {user_input.capitalize()}'
                             f'\nОсоба що змінює:\nID: {message.chat.id}\nName: {message.chat.first_name} '
                             f'{message.chat.last_name}\nПричина: {pr[0].capitalize()}')
            val = sheet.acell(f'G{int(current_group[0]) + 1}').value
            val = int(val) + 1
            sheet.update(f'G{int(current_group[0]) + 1}', str(val))
        except IndexError:
            bot.send_message(message.chat.id, f'Error', parse_mode='html', reply_markup=ev_groups_menu_markup)
    if user_input == 'ініціатива' and str(user_id) in list_access_id:
        try:
            bot.send_message(1649577403,
                             f'Зміна балів\n\nГрупа: 30{current_group[0]}\nКритерій: {user_input.capitalize()}'
                             f'\nОсоба що змінює:\nID: {message.chat.id}\nName: {message.chat.first_name} '
                             f'{message.chat.last_name}\nПричина: {pr[0].capitalize()} ')
            val = sheet.acell(f'H{int(current_group[0]) + 1}').value
            val = int(val) + 1
            sheet.update(f'H{int(current_group[0]) + 1}', str(val))
        except IndexError:
            bot.send_message(message.chat.id, f'Error', parse_mode='html', reply_markup=ev_groups_menu_markup)

    if user_input == 'перенести бали в "тенденція"' and str(user_id) in list_access_id:
        one_date = 0
        second_date = 1

        values_list = sheet_tend.col_values(1)
        values_list.pop(0)
        values_list.pop(0)
        for i in values_list:
            new_date = i.split('-')
            for j in new_date:
                new_date_now = j.replace('.', '-')
                dates.append(new_date_now)

        for i in range(len(dates)):
            try:

                start = datetime.datetime.strptime(dates[one_date], "%d-%m-%Y")
                end = datetime.datetime.strptime(dates[second_date], "%d-%m-%Y")
                date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
                last_date = end.strftime("%d-%m-%Y")

                for date in date_generated:
                    chose_date = date.strftime("%d-%m-%Y")
                    chose_date_range.append(chose_date)

                chose_date_range.append(last_date)

                if str(current_day) in chose_date_range:
                    val = sheet.acell(f'I2').value
                    sheet_tend.update(f'B{i + 3}', str(val))
                    val = sheet.acell(f'I3').value
                    sheet_tend.update(f'C{i + 3}', str(val))
                    val = sheet.acell(f'I4').value
                    sheet_tend.update(f'D{i + 3}', str(val))
                    val = sheet.acell(f'I5').value
                    sheet_tend.update(f'E{i + 3}', str(val))
                    val = sheet.acell(f'I6').value
                    sheet_tend.update(f'F{i + 3}', str(val))
                    val = sheet.acell(f'I7').value
                    sheet_tend.update(f'G{i + 3}', str(val))
                chose_date_range.clear()

                one_date += 2
                second_date += 2
            except IndexError:
                print('IndexError')
            except ValueError:
                print('ValueError')
    if user_input == '<-' and str(user_id) in list_access_id:
        current_group.clear()
        print(current_group)
        bot.send_message(message.chat.id, f'Вибір групи', reply_markup=ev_groups_menu_markup)

    if user_input == '<--' and str(user_id) in list_access_id:
        bot.send_message(message.chat.id, f'Назад', reply_markup=main_menu_markup)

    if user_input == 'вихід' and str(user_id) in list_access_id:
        bot.send_message(message.chat.id, f'Вихід', parse_mode='html', reply_markup=start_markup)


bot.polling(none_stop=True)
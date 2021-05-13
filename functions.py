def stats(group, promotion_plus, promotion_mines, discipline_plus, discipline_mines, order_plus, order_mines,
          initiative, overall_score, place_in_the_ranking, number_of_seats_available):
    return(f'<b>Статистика</b>\n\n<i>Група:</i> {group}\n<i>Зауваження з навчання:</i> {promotion_mines}\n<i>Заохочення з навчання:</i> {promotion_plus}'
          f'\n<i>Дисципліна-:</i> {discipline_mines}\n<i>Дисципліна+:</i> {discipline_plus}\n<i>Порядок-:</i> {order_mines}'
          f'\n<i>Порядок+:</i> {order_plus}\n<i>Ініціатива:</i> {initiative}\n<i>Загальний бал:</i> {overall_score}\n'
          f'<i>Місце в рейтингу:</i> {place_in_the_ranking}\n<i>Кількість місць на звільнення:</i> {number_of_seats_available}\n')


def statistic_of_group(name, com, sheet):
    promotion_plus = sheet.acell(f'C{int(com) + 1}').value
    promotion_mines = sheet.acell(f'B{int(com) + 1}').value
    discipline_plus = sheet.acell(f'E{int(com) + 1}').value
    discipline_mines = sheet.acell(f'D{int(com) + 1}').value
    order_plus = sheet.acell(f'G{int(com) + 1}').value
    order_mines = sheet.acell(f'F{int(com) + 1}').value
    initiative = sheet.acell(f'H{int(com) + 1}').value
    overall_score = sheet.acell(f'I{int(com) + 1}').value
    place_in_the_ranking = sheet.acell(f'J{int(com) + 1}').value
    number_of_seats_available = sheet.acell(f'K{int(com) + 1}').value

    mess = stats(name, promotion_plus, promotion_mines, discipline_plus, discipline_mines, order_plus, order_mines,
          initiative, overall_score, place_in_the_ranking, number_of_seats_available)
    return mess


def evaluation_group(user_input, evaluation_menu, sheet):
    print(evaluation_menu)
    com_evaluation = input('Виберіть критерій: ')

    if com_evaluation == '1':
        val = sheet.acell(f'B{int(user_input) + 1}').value
        val = int(val) + 1
        sheet.update(f'B{int(user_input) + 1}', str(val))
    if com_evaluation == '2':
        val = sheet.acell(f'C{int(user_input) + 1}').value
        val = int(val) + 1
        sheet.update(f'C{int(user_input) + 1}', str(val))
    if com_evaluation == '3':
        val = sheet.acell(f'D{int(user_input) + 1}').value
        val = int(val) + 1
        sheet.update(f'D{int(user_input) + 1}', str(val))
    if com_evaluation == '4':
        val = sheet.acell(f'E{int(user_input) + 1}').value
        val = int(val) + 1
        sheet.update(f'E{int(user_input) + 1}', str(val))
    if com_evaluation == '5':
        val = sheet.acell(f'F{int(user_input) + 1}').value
        val = int(val) + 1
        sheet.update(f'F{int(user_input) + 1}', str(val))
    if com_evaluation == '6':
        val = sheet.acell(f'G{int(user_input) + 1}').value
        val = int(val) + 1
        sheet.update(f'G{int(user_input) + 1}', str(val))
    if com_evaluation == '7':
        val = sheet.acell(f'H{int(user_input) + 1}').value
        val = int(val) + 1
        sheet.update(f'H{int(user_input) + 1}', str(val))


def accept_mess(message, bot):
    mess = f'ID: {message.chat.id}\nFirst-name: {message.chat.first_name}\nLast-name: {message.chat.last_name}' \
           f'\nГрупа: \nКритерій: \nПричина: '

    return mess
import re
import csv
from pprint import pprint
from datetime import datetime

def logger(old_function):
    def new_function(*args, **kwargs):
        dt = datetime.today()
        result = old_function(*args, **kwargs)

        with open('main.log', 'a') as f:
            f.write(f'{dt}\n')
            f.write(f'{old_function.__name__}\n')
            f.write(f'{args}, {kwargs}\n')
            f.write(f'{result}\n')
            f.write('\n')

        return result

    return new_function

@logger
def contacts_change():
    contacts_new = []
    for people in contacts_list:
        fio = []
        el_list = []
        chel_new = []
        for el in people[:3]:
            el_list.extend(el.split(' '))
        fio.extend(el_list[:3])
        chel_new.extend(fio)
        chel_new.extend(people[3:])
        contacts_new.append(chel_new)

    # Поиск дублей:
    contacts_dicts = {}
    for people in contacts_new:
        cont_dict = {'lastname': people[0],
                     'firstname': people[1],
                     'surname': people[2],
                     'organization': people[3],
                    'position': people[4],
                    'phone': people[5],
                    'email': people[6]}
        if f'{people[0]} {people[1]}' not in contacts_dicts.keys():
            # Создать ключ с фамилией и именем
            contacts_dicts[f'{people[0]} {people[1]}'] = cont_dict
        else:
            for k, val in list(contacts_dicts[f'{people[0]} {people[1]}'].items()):
                if val == '':
                    # Обновить пустующую информацию
                    contacts_dicts[f'{people[0]} {people[1]}'].update({k: cont_dict[k]})

    # конвертация обратно в список:
    contacts_edit = []
    for s in list(contacts_dicts.values()):
        contacts_edit.append(list(s.values()))
    return contacts_edit

@logger
def phone_edit(contacts_edit):
    # Исправление номеров телефонов на +7(999)999-99-99 доб.9999
    pattern = r'(\+7|8)?\s*\(*(\d{3})\)*[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})[ \(]*[доб\.]*\s*(\d{4})*\)*'
    replace_full = r'+7(\2)\3-\4-\5 доб.\6'
    replace = r'+7(\2)\3-\4-\5'
    for chel in contacts_edit:
        if 'доб' in chel[5]:
            chel[5] = re.sub(pattern, replace_full, chel[5])
        else:
            chel[5] = re.sub(pattern, replace, chel[5])

if __name__ == '__main__':
    # читаем адресную книгу в формате CSV в список contacts_list
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    pprint(contacts_list)

    contacts_edit = contacts_change()
    phone_edit(contacts_edit)

    # TODO 2: сохраните получившиеся данные в другой файл
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_edit)
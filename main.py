import csv
import re


def read_csv(csv_file):
    with open(csv_file, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return contacts_list


def sorted_fullname_change_phone():
    pattern_tel = r'(\+7|8)[\s(]*(\d{3})[\s\)-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s(]*(доб.)*\s*(\d+)*'
    tel_sub = r'+7(\2)\3-\4-\5 \6\7'
    contact_list = read_csv('phonebook_raw.csv')
    k = 1
    for person in contact_list[1:]:
        person_fullname = ' '.join(person[:3]).split(' ')
        if '' in person_fullname:
            person_fullname.remove('')
        contact_list_sorted = [person_fullname[0], person_fullname[1], person_fullname[2],
                               person[3], person[4], re.sub(pattern_tel, tel_sub, person[5]), person[6]]
        contact_list[k] = contact_list_sorted
        k += 1

    return contact_list


def delete_double():
    contact_list = sorted_fullname_change_phone()
    contact_dict = {}
    for item in contact_list[1:]:
        contact_dict.update({f'{item[0]} {item[1]}': item[2:]})
    contact_list_new = [contact_list[0]]
    for item in contact_dict:
        contact_list_new.append(item.split(' ') + contact_dict[item])
    k = 1
    for item in contact_list_new[1:]:
        for item_2 in contact_list[1:]:
            if item[0] == item_2[0] and item[1] == item_2[1]:
                for i in range(2, 7):
                    if item[i] == '':
                        contact_list_new[k][i] = item_2[i]
        k += 1
    return contact_list_new


def write_phonebook():
    contact_list = delete_double()
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        return datawriter.writerows(contact_list)


print(write_phonebook())

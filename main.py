import re

from db import db
import pymongo
from datetime import datetime


# декоратор  - обработчик ошибок
def input_error(func):
    def hundler(data):
        try:
            result = func(data)
        except Exception as e:
            return e
        return result
    return hundler


@input_error
def hello(data):
    print("How can I help you?")

#@input_error
def del_ph(data): #++
    # функция, которая удаляет документ с name-phone
    data = data.replace('del ph ', '')
    #  действительно ли там есть два "слова" ?
    if len(data.split()) == 2:
        name, phone = data.split()
        phone = re.sub(r'[^\d]', '', phone)
        result = db.addressbook.find_one({'name': name, 'phone': phone})
        print(result)
        result = db.addressbook.delete_one({'name': name, 'phone': phone})
        

@input_error
def del_name(data): #++
    # удаление записи  по  имени
    data = data.replace('del ', '')
    if len(data.split()) == 1:
        name = data
        result = db.addressbook.find({'name': name})
        for el in result:
            print(el)
        result = db.addressbook.delete_many({'name': name})
    else:
        raise Exception("Give me only name")


@input_error
def add_ph(data): #++
    # функция, которая добавляет имя-телефон
    data = data.replace('add ph ', '')
    #  действительно ли там есть два "слова" ?
    if len(data.split()) == 2:
        name, phone = data.split()
        phone = re.sub(r'[^\d]', '', phone)
        result = db.addressbook.insert_one(
            {
                "name" : name,
                "phone" : phone
            }
        )
        print(db.addressbook.find_one({'_id':result.inserted_id}))
    else:
        raise Exception("Give me name and phone please")

#@input_error
def add_bd(data): #++
    # функция, которая добавляет имя-день рождения
    data = data.replace('add bd ', '')
    #  действительно ли там есть два "слова" ?
    if len(data.split()) == 2:
        name, birthday = data.split()
        birthday = datetime(*map(int,re.split(r'[-,./]+',birthday)))

        result = db.addressbook.insert_one(
            {
                "name" : name,
                "birthday" : birthday
            }
        )
        print(db.addressbook.find_one({'_id':result.inserted_id}))
    else:
        raise Exception("Give me name and birthday please")

@input_error
def change_ph(data): #++
    #   чтобы изменить телефон. должна получить три слова
    #   name, phone, new_phone
    data = data.replace('change ph ', '')
    if len(data.split()) == 3:
        name, phone, new_phone = data.split()
        phone = re.sub(r'[^\d]', '', phone)
        new_phone = re.sub(r'[^\d]', '', new_phone)
        # изменит телефон, если не найдет создаст новую запись name-new_phone
        result = db.addressbook.update_one({"name" : name, "phone" : phone}, 
                            {"$set": {"name": name, "phone" : new_phone}}, 
                            upsert = True)
    else:
        raise Exception("Give me name and phone please")

@input_error
def change_bd(data): #++
    #   изменить день рождения. должна получить два слова
    #   name,  new_birthday
    data = data.replace('change bd ', '')
    if len(data.split()) == 2:
        name,  new_birthday = data.split()
        birthday = datetime(*map(int,re.split(r'[-,./]+',new_birthday)))
        
        result = db.addressbook.update_one({"name" : name, "birthday" : {"$exists": True}}, 
                            {"$set": {"name": name, "birthday" : birthday}}, 
                            upsert = True)
        print(db.addressbook.find_one({'_id':result.upserted_id}))
    else:
        raise Exception("Give me name and birthday, please")


@input_error
def phone(data): #++
    # простая функция поиска записи  по  имени
    data = data.replace('phone ', '')
    if len(data.split()) == 1:
        name = data
        result = db.addressbook.find({"name": name})   
    for el in result : 
        print(el)
    else:
        raise Exception("Give me only name")
    

@input_error
def show_all(data): #++
    data = data.replace('show all', '')
    result = db.addressbook.find()   
    for el in result : 
        print(el)
        
@input_error
def good_bye(data):
    # функция окончания работы и сохранения данных
    
    return "Good bye!"


ACTIONS = {
    'hello': hello,
    'add ph': add_ph,
    'add bd': add_bd,
    'change ph': change_ph,
    'change bd': change_bd,
    'del ph' : del_ph,
    'del' : del_name,
    'phone': phone,
    'show all': show_all,
    'good bye': good_bye,
    'close': good_bye,
    'exit': good_bye,
    '.': good_bye,
}


@input_error
def choice_action(data):
    for command in ACTIONS:
        if data.startswith(command):
            return ACTIONS[command]
    raise Exception("Give me a correct command please")


if __name__ == '__main__':

    while True:
        text = ''' You can:
        hello, good bye, close, exit, . - understandably
        add ph <name> <phone>
        add bd <name> <birthday>
        change ph <name> <phone> <new_phone>
        change bd <name> <new_birthday>
        del <name>
        del ph <name> <phone>
        show all  <N>    - show all abonent, N - number abonents in page
        phone <name>  - show all phone this abonent
        '''
        print(text)
        data = input()

        func = choice_action(data)
        if isinstance(func, Exception):
            print(func)
            continue
        result = func(data)
        #for el in result:
        #    print('--------', el.name, el.address)

        if result:
            print(result)
        if result == 'Good bye!':
            break

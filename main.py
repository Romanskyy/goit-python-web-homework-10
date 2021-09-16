import re

from db import db
import pymongo
from datetime import datetime
import redis 
redis_db = redis.Redis(host = 'localhost', port = 6379, db = 0)


# декоратор  - обработчик ошибок
def input_error(func):
    def hundler(data):
        try:
            result = func(data)
        except Exception as e:
            return e
        return result
    return hundler

def lru_cache(name_action, max_size = 10):
    list_cache = []
    def wrapped(func):
        #cache = LruCache(func, name_action, max_size, db)
        def inner(*args):
            print(name_action, *args) 
            # ключ это (действие, параметры)
            # например ('find_one', 'vova', '123456')
            # or ('find', 'vova')
            key = name_action, *args
            key = f'{key}'

            # если вызываемая функция - не find
            # значит она изменит данные и онм станут неактуальными
            if not name_action.startswith('find'):
                # если имя из этого ключа есть в кеше -  удаляем ту запись
                name = args[0]
                # поиск имени в ключах, сохраняя найденное во временном списке
                # нам их надо будет удалить и из list_cache и из словаря.
                list_key_for_del = []
                for ind, el in enumerate(list_cache):
                    if name in el:
                        list_key_for_del.append(el)

                # удаляем и из list_cache и из словаря.    
                for el in list_key_for_del:
                    list_cache.remove(el)
                    redis_db.delete(el)
                
                result = func(*args)
                return result
            print('key, list_cache', key, list_cache)
            print('type key', type(key))
            # если в кеше нет такого значения
            if key not in list_cache:
                # таки вызываем функцию.
                value = func(*args)
                # формирую строку
                if name_action == 'find':
                    result = ''
                    for el in value : 
                        result += str(el)
                else:
                    result = str(value)
                # записываем значение в словарь
                redis_db.set(key, result)
            # если нет
            else:
                #перемещаем ключ в начало очереди
                # сначала удаляем из очереди
                #  надо проверить есть ли такие и данные в словаре 
                ind = list_cache.find(key)
                el = list_cache.pop(ind)
                # еще надо выполнить функцию
                # ставим в начало
                list_cache.insert(0, el)
            # если очередь слишком длинная усекаем ее
            if len(list_cache) >= max_size:
                list_cache.pop()
            # забираем значение из словаря
            print('72 ', key, result)
            print('--------')
            result = redis_db.get(key)
            return result
        
        return inner
    return wrapped

@lru_cache('find')
def my_find(*args):
    return db.addressbook.find(*args)

@lru_cache('find_one')
def my_find_one(*args):
    return db.addressbook.find_one(*args)

@lru_cache('delete_one')
def my_delete_one(*args):
    return db.addressbook.delete_one(*args)
        

@lru_cache('delete_many')
def my_delete_many(*args):
    return db.addressbook.delete_many(*args)

@lru_cache('insert_one')
def my_insert_one(*args):
    return db.addressbook.insert_one(*args)

@lru_cache('update_one')
def my_update_one(*args):
    return db.addressbook.update_one(*args)

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
        result = my_find_one({'name': name, 'phone': phone})
        print(result)
        result = my_delete_one({'name': name, 'phone': phone})
        

@input_error
def del_name(data): #++
    # удаление записи  по  имени
    data = data.replace('del ', '')
    if len(data.split()) == 1:
        name = data
        result = my_find({'name': name})
        for el in result:
            print(el)
        result = my_delete_many({'name': name})
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
        result = my_insert_one({"name" : name, "phone" : phone})
        print(my_find_one({'_id':result.inserted_id}))
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

        result = my_insert_one({"name" : name, "birthday" : birthday})
        print(my_find_one({'_id':result.inserted_id}))
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
        result = my_update_one({"name" : name, "phone" : phone}, 
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
        
        result = my_update_one({"name" : name, "birthday" : {"$exists": True}}, 
                            {"$set": {"name": name, "birthday" : birthday}}, 
                            upsert = True)
        print(my_find_one({'_id':result.upserted_id}))
    else:
        raise Exception("Give me name and birthday, please")


#@input_error
def phone(data): #++
    # простая функция поиска записи  по  имени
    data = data.replace('phone ', '')
    if len(data.split()) == 1:
        name = data
        result = my_find({"name": name})    
        print(result)
    else:
        raise Exception("Give me only name")
    

@input_error
def show_all(data): #++
    data = data.replace('show all', '')
    result = my_find()   
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

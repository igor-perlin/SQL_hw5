import psycopg2

# Создаем базу данных
def create_tables():
    with psycopg2.connect(database='clients', user='postgres', password='200182') as conn: # Подключаемся
        with conn.cursor() as cur: # Создаем курсор
            cur.execute(f"CREATE TABLE IF NOT EXISTS clients ( "
                        f"client_id SERIAL PRIMARY KEY, "
                        f"name VARCHAR(15) NOT NULL, "
                        f"surname VARCHAR(15) NOT NULL, "
                        f"email VARCHAR(25) UNIQUE);"
                        f"CREATE TABLE IF NOT EXISTS phone_numbers ( "
                        f"phone_number_id SERIAL PRIMARY KEY, "
                        f"client_id INTEGER REFERENCES clients(client_id), "
                        f"phone_number VARCHAR(15) NOT NULL);")
            conn.commit()
            print('Таблицы в базе созданы.')
    conn.close() # Закрываем подключение
    print()


def add_new_client(): # Добавление клиента
    print('*** добавить нового клиента ***')
    name = input('Введите имя: ')
    surname = input('Введите фамилию: ')
    email = input('Введите e-mail: ')
    phone_number = input('Введите телефон: ')
    with psycopg2.connect(database='clients', user='postgres', password='200182') as conn:
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO clients (name, surname, email) "
                        f"VALUES ('{name}','{surname}','{email}'); "
                        f"SELECT * FROM clients;")
            client_id = cur.fetchall()[-1][0]
            if phone_number != '':
                cur.execute(f"INSERT INTO phone_numbers (client_id, phone_number) "
                            f"VALUES ({client_id}, '{phone_number}');")
                conn.commit()
                print(f'Новый клиент добавлен!')
    conn.close()
    print()

def add_phone_number(): # Добавляем номер телефона
    print('*** добавить телефон для существующего клиента ***')
    client_id = input('Введите id клиента: ')
    new_phone_number = input('Введите дополнительный телефон: ')
    with psycopg2.connect(database='clients', user='postgres', password='200182') as conn:
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO phone_numbers (client_id, phone_number)"
                        f"VALUES ({client_id},'{new_phone_number}');")
            conn.commit()
            print(f'Дополнительный телефон добавлен')
    conn.close()
    print()

def update_client_info(): # Меняем данные клиента
    print('*** изменить данные о клиенте ***')
    client_id = input('Введите id клиента: ')
    new_name = input('Введите новое [Имя]: ')
    new_surname = input('Введите новую [Фамилию]: ')
    new_email = input('Введите новую [Почту]: ')
    updates_str = ''
    if new_name != '':
        updates_str += f"name='{new_name}'"
    if new_surname != '':
        updates_str += f", surname='{new_surname}'"
    if new_email != '':
        updates_str += f", email='{new_email}'"
    with psycopg2.connect(database='clients', user='postgres', password='200182') as conn:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE clients SET {updates_str} WHERE client_id={client_id};")
            conn.commit()
            print('Данные изменены')
    conn.close()
    print()

def del_phone_number(): # Удаляем телефон клиента
    print('*** удалить телефон для существующего клиента ***')
    client_id = input('Введите id клиента: ')
    with psycopg2.connect(database='clients', user='postgres', password='200182') as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM clients WHERE client_id={client_id};")
            client_info = cur.fetchone()
            print(f'Клиент {client_info[1]} {client_info[2]}')
            print('Номера телефонов:')
            cur.execute(f"SELECT * FROM phone_numbers WHERE client_id={client_id};")
            client_phones = cur.fetchall()
            print('id'.center(5) + '-' + 'Номер телефона'.center(16))
            for client_phone in client_phones:
                print(str(client_phone[0]).center(5) + '-' + client_phone[2].center(16))
            phone_number_id = input('Введите id удаляемого номера: ')
            cur.execute(f"DELETE FROM phone_numbers WHERE phone_number_id={phone_number_id};")
            conn.commit()
            print('Номер телефона удален')
    conn.close()
    print()

def del_client(): # Удаляем клиента из базы
    print('*** удалить существующего клиента ***')
    client_id = input('Введите id клиента: ')
    with psycopg2.connect(database='clients', user='postgres', password='200182') as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM phone_numbers WHERE client_id={client_id};"
                        f"DELETE FROM clients WHERE client_id={client_id};")
            conn.commit()
            print('Клиент удален из базы')
    conn.close()
    print()

def find_client(): # Находим клиента в базе
    print('*** найти клиента по его данным (имени, фамилии, email-у или телефону) ***')
    key = input('Введите данные для поиска: ')
    with psycopg2.connect(database='clients', user='postgres', password='200182') as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT DISTINCT clients.client_id, name, surname, email, phone_number "
                        f"FROM clients "
                        f"JOIN phone_numbers "
                        f"ON clients.client_id = phone_numbers.client_id "
                        f"WHERE name LIKE '%{key}%' OR surname LIKE '%{key}%' OR email LIKE '%{key}%' "
                        f"OR phone_number LIKE '%{key}%';")
            clients_info = cur.fetchall()
            print(clients_info)
            print('id'.center(5) + 'Имя'.center(15) + 'Фамилия'.center(15) +
                  'e-mail'.center(25) + 'Номер телефона'.center(16))
            print('-' * 82)
            for client in clients_info:
                print(str(client[0]).center(5) + client[1].center(15) +
                      client[2].center(15) + client[3].center(25) + client[4].center(16))
    conn.close()
    print()

def main():
    functions = {1: create_tables,
                 2: add_new_client,
                 3: add_phone_number,
                 4: update_client_info,
                 5: del_phone_number,
                 6: del_client,
                 7: find_client
                 }
    print('1 - Функция, создающая структуру БД (таблицы)\n'
          '2 - Функция, позволяющая добавить нового клиента\n'
          '3 - Функция, позволяющая добавить телефон для существующего клиента\n'
          '4 - Функция, позволяющая изменить данные о клиенте\n'
          '5 - Функция, позволяющая удалить телефон для существующего клиента\n'
          '6 - Функция, позволяющая удалить существующего клиента\n'
          '7 - Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)\n')
    function = int(input('Выберите номер функции: '))
    functions[function]()


if __name__ == '__main__':
    while True:
        main()
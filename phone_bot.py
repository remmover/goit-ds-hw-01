import re
from collections import UserDict
from datetime import datetime
from functools import wraps
from itertools import islice
import pickle
import pathlib

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Record:
    def __init__(self, name, phone=None, b_date=None):
        self.name = name
        self.phones = []
        self.b_date = b_date

    def add_phone(self, phone):
        self.phones.append(f'num = {phone}')

    def change_phone(self, name, phone):
        self.phones[name] = phone

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def days_to_birthday(self, b_date):
        b_date = str(b_date)
        current_date = datetime.now().date()
        normal_date = datetime.strptime(b_date, '%d.%m.%Y').replace(
            year=current_date.year).date()
        days = (normal_date - current_date).days
        if days < 0:
            normal_date = datetime.strptime(b_date, '%d.%m.%Y').replace(
                year=current_date.year + 1).date()
            days = (normal_date - current_date).days
        self.phones.append(f'days to BD = {days} ;')

    def __repr__(self) -> str:
        return f"{', '.join([str(i) for i in self.phones])}"


class Birthday(Field):
    def __init__(self, value=None):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, bd_date):
        try:
            datetime.strptime(bd_date, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Birthdate must be in 'dd.mm.yyyy' format")
        self.__value = bd_date


class Phone(Field):

    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        if not re.match(r"^(?:\+380|0)(?:39|67|68|96|97|98|50|66|95|99|63|73|93)\d{7}$", phone):
            raise ValueError(
                "Phone must start with +380 or 0 and has 9 nums after")
        self.__value = phone


class Name(Field):
    pass


class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value
        self.data[name] = record

    def iterator(self, records_count=3):
        start_iterate = 0
        while True:
            if start_iterate >= len(self.data):
                break
            yield dict(islice(self.data.items(),
                              start_iterate,
                              start_iterate + records_count))
            start_iterate += records_count

    def save_to_bin(self, path="AddressBook.bin"):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_bin(path="AddressBook.bin"):
        if pathlib.Path(path).exists():
            with open(path, "rb") as f:
                return pickle.load(f)
        else:
            return AddressBook()

contacts = AddressBook.load_from_bin()


def input_error(func):
    @wraps(func)
    def wrapper(*args):
        try:
            return func(*args)
        except (KeyError, ValueError, IndexError) as exc:
            result = f"An error occurred: {str(exc)}"
            return result
    return wrapper


def help(*args):
    return """"hello", відповідає у консоль "How can I help you?"
"add ...". За цією командою бот зберігає у пам'яті новий контакт.
"change ..." За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту.
"phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту.
"show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.
"good bye", "close", "exit" по будь-якій з цих команд бот завершує свою роботу після того, як виведе у консоль "Good bye!"."""


def hello(*args):
    return 'Hello, how can I help you?'


@input_error
def add_func(*args):
    obj = args[0].split()
    name = Name(obj[0])
    phone = Phone(obj[1])
    record = Record(name)
    record.add_phone(phone)
    if len(obj) == 3:
        bd_date = Birthday(obj[2])
        record.days_to_birthday(bd_date)
        contacts.add_record(record)
        return f'U add contact with all parameters : {name} and his number is : {phone} and his BD : {bd_date}'
    else:
        contacts.add_record(record)
        return f'U add contact with name: {name} and his number is : {phone}'


@input_error
def change_contacts_dict(*args):
    obj = args[0].split()
    name = Name(obj[0])
    phone = Phone(obj[1])
    record = contacts[name.value]
    record.change_phone(0, phone)
    return f'You have changed the number to this one: {phone} in the contact with the name: {name}'


def phone_func(*args):
    if len(args) < 1:
        return "Please provide a search query"

    value = args[0].lower()

    result = ''
    for name, record in contacts.data.items():
        phones = [str(phone) for phone in record.phones]
        phone_str = ', '.join(phones)

        if value in name.lower() or any(value in phone.lower() for phone in phones):
            contact = f'\n{name.capitalize()}: {phone_str}'
            result += contact

    if not result:
        return f'\nNo contact found with the query: {value}\n'
    return result


def show_all_func(*args):
    if len(contacts.data) == 0:
        return "list of contacts is empty..."
    records_count = args[0]
    if records_count:
        for i in contacts.iterator(int(records_count)):
            print(i)
    else:
        return contacts


def no_command(*args):
    return "Unknown command, try again."

def exit(*args):
    contacts.save_to_bin()
    print("Good bye!")


OPERATION = {
    'hello': hello,
    'add': add_func,
    'change': change_contacts_dict,
    'phone': phone_func,
    'show all': show_all_func,
    'help': help,
}


END_WORDS = ['good bye', 'close', 'exit']


def handle_command(user_input):
    for word, command in OPERATION.items():
        if user_input.startswith(word):
            return command, user_input.replace(word, '').strip()
    return no_command, None


def main():

    print(help())
    while True:
        user_input = input("Write what u wont from bot >>> ").lower()
        if user_input in END_WORDS:
            exit()
            break
        command, data = handle_command(user_input)
        print(command(data))


if __name__ == '__main__':
    main()
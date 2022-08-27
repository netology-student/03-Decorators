
# Домашнее задание к лекции 3.«Decorators»
#
#     Написать декоратор - логгер. Он записывает в файл дату и время вызова функции, имя функции, аргументы, с которыми вызвалась и возвращаемое значение.
#     Написать декоратор из п.1, но с параметром – путь к логам.
#     Применить написанный логгер к приложению из любого предыдущего д/з.

from log_tools import logged

nested_list = [
        ['1', '2', '3'],
        '4',
        ['5', '6', '7', ['8', '9', '10'], '11'],
        [['12', '13'], '14'],
    ]

class FlatIterator():

    def __init__(self, nested_list):
        self.nested_list = nested_list

    def __iter__(self):
        self.iter_stack = []
        self.crt_iter = iter(self.nested_list)
        return self

    @logged("logs/my_next.log")
    def my_next(self):
        try:
            next_value = next(self.crt_iter)
        except StopIteration:
            if len(self.iter_stack) != 0:
                #  Возвращаемся на уровень выше
                self.crt_iter = self.iter_stack.pop()
                next_value = self.my_next()
            else:
                #  Конец обхода верхнего уровня
                raise StopIteration
        else:
            if isinstance(next_value, list):
                # Сохраняем текущий уровень
                self.iter_stack.append(self.crt_iter)
                # Ныряем глубже
                self.crt_iter = iter(next_value)
                next_value = self.my_next()

        return next_value

    def __next__(self):
        return self.my_next()


@logged("logs/flat_generator.log")
def flat_generator(o):
    if isinstance(o, list):
        for value in o:
            for subvalue in flat_generator(value):
                yield subvalue
    else:
        yield o

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print("flat_list:");
    flat_list = [item for item in FlatIterator(nested_list)]
    print(flat_list);

    print("__________________________________")

    print("flat_generator:")
    for item in flat_generator(nested_list):
        print(item)

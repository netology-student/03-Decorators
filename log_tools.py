
import logging
from datetime import datetime
import os

def logged(filename):
    def _logged(target_function):

        logger = logging.getLogger(filename)
        logger.setLevel(logging.INFO)

        directory = 'logs'
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_handler = logging.FileHandler(filename)
        logger.addHandler(file_handler)

        def logged_function(*args, **kwargs):

            # Он записывает в файл дату и время вызова функции, имя функции, аргументы, с которыми вызвалась и возвращаемое значение

            result = target_function(*args, **kwargs)

            log_message = f'time = {datetime.now()}, name = {target_function.__name__} , params = {args}{kwargs}, result = {result}'
            logger.info(log_message)

            return result

        return logged_function

    return _logged

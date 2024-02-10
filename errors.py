from tts import TextToSpeech
import logging

class SayException(Exception):
    def say(self):
        if self.say_message != '':
            TextToSpeech.say(self.say_message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

class RegexArgumentError(SayException):
    def __init__(self, 
                 command_class='', 
                 code=11,  
                 argument='', 
                 message="Совпадений регулярного выражения не найдено в вводе. Пожалуйста, проверяйте правильность регулярного выражения на стронних ресурсах, прежде чем его использовать. Также возможно, что в фразе нет нужного аргумента", 
                 say_message='Аргумент не найден по регулярному выражению'):
        self.code = code
        self.message = message
        self.say_message = say_message
        self.command_class = command_class
        self.argument = argument

    def log_critical_error(self):
        logging.critical(f"{self.__class__.__name__} in '{self.command_class}':Error_code={self.code}:{self.argument}:{self.message}.")

    def proccess_critical_error(self):
        self.say()
        self.log_critical_error()
    

class RegexPatternError(SayException):
    def __init__(self, 
                 command_class='', 
                 code=12,  
                 argument='', 
                 message="Кажется, вы неверно указали регулярное выражение. Пожалуйста, проверяйте правильность регулярного выражения на стронних ресурсах", 
                 say_message='Неверное регулярное выражение'):
        self.code = code
        self.message = message
        self.say_message = say_message
        self.command_class = command_class
        self.argument = argument

    def log_critical_error(self):
        logging.critical(f"{self.__class__.__name__} in '{self.command_class}':Error_code={self.code}:{self.argument}:{self.message}.")

    def proccess_critical_error(self):
        self.say()
        self.log_critical_error()

class ArgumentError(SayException):
    def __init__(self, 
                 command_class='', 
                 code=10,  
                 argument='', 
                 message="Не удалось распознать аргумент. Проверьте правильность написание регулярного выражения, или ввод на наличие нужного выражения", 
                 say_message='Не удалось прочитать аргумент'):
        self.code = code
        self.message = message
        self.say_message = say_message
        self.command_class = command_class
        self.argument = argument

    def log_critical_error(self):
        logging.critical(f"{self.__class__.__name__} in '{self.command_class}':Error_code={self.code}:{self.argument}:{self.message}.")

    def proccess_critical_error(self):
        self.say()
        self.log_critical_error()

    
class ExecCliCommandError(SayException):
    def __init__(self, 
                 command_class='', 
                 code=30, 
                 command='',
                 output='',
                 message='Не удалось выполнить команду. Проверьте правильность написания команды. Если все правильно, то скорее всего команду невозможно выполнить при текущих условиях', 
                 say_message='Не удалось выполнить команду'):
        self.code = code
        self.message = message
        self.say_message = say_message
        self.command_class = command_class
        self.command = command
        self.output = output

    def log_critical_error(self):
        logging.critical(f"{self.__class__.__name__} in '{self.command_class}':Error_code={self.code}:STDOUT={self.output}:{self.command}:{self.message}.")

    def proccess_critical_error(self):
        self.say()
        self.log_critical_error()



class CommandAccessError(SayException):
    def __init__(self, 
                 command_class='', 
                 code=40,
                 access_to='',
                 message='Ошибка доступа к информации о команде. Пожалуйста, проверьте правильность написания команды и ее параметров.', 
                 say_message='Ошибка доступа к информации о команде.'):
        self.code = code
        self.message = message
        self.say_message = say_message
        self.command_class = command_class
        self.access_to = access_to

    def log_critical_error(self):
        logging.critical(f"{self.__class__.__name__} in '{self.command_class}' access to {self.access_to}:Error_code={self.code}:{self.message}.")

    def proccess_critical_error(self):
        self.say()
        self.log_critical_error()

    

class CommandSyntaxInYamlError(SayException):
    def __init__(self, 
                 command_class='', 
                 code=50,
                 key='',
                 message='Не хватает нужного параметра в YAML фалйе с командами', 
                 say_message='Неверное описание команды. Недостает параметров'):
        self.code = code
        self.message = message
        self.say_message = say_message
        self.command_class = command_class
        self.key = key

    def log_critical_error(self):
        logging.critical(f"{self.__class__.__name__} in '{self.command_class}' not exists {self.key}:Error_code={self.code}:{self.message}.")

    def proccess_critical_error(self):
        self.say()
        self.log_critical_error()



class WikipediaNotFoundError(SayException):
    def __init__(self, 
                 command_class='', 
                 code=100,
                 search_for='',
                 message='В Wikipedia нет такой страницы', 
                 say_message='По вашему запросу ничего не найдено'):
        self.code = code
        self.message = message
        self.say_message = say_message
        self.command_class = command_class
        self.search_for = search_for

    def log_warning(self):
        logging.warning(f"{self.__class__.__name__} in '{self.command_class}' search for {self.search_for}:Error_code={self.code}:{self.message}.")

    def proccess_warning(self):
        self.say()
        self.log_warning()

    

class WikipediaApiError(SayException):
    def __init__(self, 
                 command_class='', 
                 code=110,
                 search_for='',
                 message='Ошибка подключения к API Wikipedia', 
                 say_message='Ошибка подключения к википедии'):
        self.code = code
        self.message = message
        self.say_message = say_message
        self.command_class = command_class
        self.search_for = search_for

    def log_warning(self):
        logging.warning(f"{self.__class__.__name__} in '{self.command_class}' search for {self.search_for}:Error_code={self.code}:{self.message}.")

    def proccess_warning(self):
        self.say()
        self.log_warning()


class UnknownError(SayException):
    def __init__(self, 
                 command_class='', 
                 code=120,
                 message='Неизвестная ошибка', 
                 say_message='Неизвестная ошибка, информация в лог файле'):
        self.code = code
        self.message = message
        self.say_message = say_message
        self.command_class = command_class

    def log_critical_error(self):
        logging.critical(f"{self.__class__.__name__} in '{self.command_class}':Error_code={self.code}:{self.message}.")

    def proccess_critical_error(self):
        self.say()
        self.log_critical_error()


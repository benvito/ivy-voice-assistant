import tts
import logging

class RegexArgumentError(Exception):
    def __init__(self, 
                 command_class='', 
                 code=11,  
                 argument='', 
                 message="Совпадений регулярного выражения не найдено в вводе. Пожалуйста, проверяйте правильность регулярного выражения на стронних ресурсах, прежде чем его использовать. Также возможно, что в фразе нет нужного аргумента", 
                 say_message='Не удалось прочитать аргумент'):
        self.code = code
        self.message = message
        self.say_message = say_message
        self.command_class = command_class
        self.argument = argument

    def say(self):
        if self.say_message != '':
            tts.say(self.say_message)

    def log_critical_error(self):
        logging.critical(f"{self.__class__.__name__} in {self.command_class}:Error_code={self.code}:{self.argument}:{self.message}.")

    def proccess_critical_error(self):
        self.say()
        self.log_critical_error()

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

class ArgumentError(Exception):
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

    def say(self):
        if self.say_message != '':
            tts.say(self.say_message)

    def log_critical_error(self):
        logging.critical(f"{self.__class__.__name__} in {self.command_class}:Error_code={self.code}:{self.argument}:{self.message}.")

    def proccess_critical_error(self):
        self.say()
        self.log_critical_error()

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
    
class ExecCliCommandError(Exception):
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

    def say(self):
        if self.say_message != '':
            tts.say(self.say_message)

    def log_critical_error(self):
        logging.critical(f"{self.__class__.__name__} in {self.command_class}:Error_code={self.code}:STDOUT={self.output}:{self.command}:{self.message}.")

    def proccess_critical_error(self):
        self.say()
        self.log_critical_error()

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

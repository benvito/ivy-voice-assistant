import time
import yaml
import os
import random as rnd
import subprocess
import re
import logging
import webbrowser
import wikipediaapi
from pprint import pprint
import threading
import ctypes
from abc import abstractmethod

from config.constants import *
from errors.errors import *
from utils.yaml_utils import YamlData
from utils.utils import Time, WordNum, StringProcessing
from config import COMMANDS_PATH
from commands.img_macro import IMacro
from commands.arguments_process import ArgumentsProcessor

class Command:
    """
    COMMAND CLASS

    HELPS LINT NECESSARY COMMAND 
    """
    @abstractmethod
    def process(command : dict, command_class : str, voice_input : str) -> str:
        raise NotImplementedError("Please implement 'process' method")
    
    @staticmethod
    def lint_unnecessary(command : dict) -> dict:
        try:
            a = command[CMD_ARGS]
        except:
            command[CMD_ARGS] = dict()

        try:
            a = command[ARGS_SEP]
        except:
            command[ARGS_SEP] = CONCAT

        try:
            a = command[SPEECH_ARGS]
        except:
            command[SPEECH_ARGS] = False
        
        try:
            a = command[SPEECH_OUTPUT]
        except:
            command[SPEECH_OUTPUT] = False

        for arg, params in command[CMD_ARGS].items():
            if type(params) != dict:
                command[CMD_ARGS][arg] = dict()
            try:
                a = params[REGEX_ON]
            except:
                command[CMD_ARGS][arg][REGEX_ON] = False
            try:
                a = params[PREFIX]
            except:
                command[CMD_ARGS][arg][PREFIX] = ''
            try:
                a = params[POSTFIX]
            except:
                command[CMD_ARGS][arg][POSTFIX] = ''

        return command

    def lint_type(self, command : dict, command_class : str) -> dict:
        return command

    def lint(self, command : dict, command_class : str) -> dict:
        command[COMMAND_FOLDER] = YamlData.path_to_command(command_class)

        try:
            a = command[SPEECH_TYPE]
            a = command[SPEECH_LIST]
            a = command[COMMAND_TYPE]
            a = command[PHRASES]
        except Exception as e:
            raise CommandSyntaxInYamlError(command_class=command_class,
                                        key=e)
        
        command = self.lint_unnecessary(command)
        command = self.lint_type(command, command_class)
        return command
    
    def lint_hybrid(self, command : dict, command_class : str) -> dict:
        command = self.lint_unnecessary(command)
        try:
            a = command[SPEECH_TYPE]
        except KeyError:
            command[SPEECH_TYPE] = 'dynamic'

        try:
            a = command[SPEECH_LIST]
        except KeyError:
            command[SPEECH_LIST] = None

        try:
            a = command[PHRASES]
        except KeyError:
            command[PHRASES] = None
        print(command)

        command = self.lint_type(command, command_class)
        return command


class CommandProcessor:
    """
    COMMAND PROCESSOR
    USE IT TO:
        - PROCESS COMMAND
        - CREATE SPEECH OUTPUT
        - LINT COMMANDS FROM YAML
    """ 
    @staticmethod
    def create_speech_output(speech_type : str, speech_list : list, command_class : str, command_output : str = None, speech_output : bool = False) -> str:
        phrase = ''
        if speech_type == DYNAMIC:

            if speech_list != None:
                phrase += rnd.choice(speech_list)

            if speech_output == True:
                phrase += ' '

                if 'time' in command_class:
                    command_output = Time.time_format_for_string(command_output)

                phrase += str(command_output)
                
        return phrase
    
    @staticmethod
    def unknown_command() -> str:
        try:
            command = YamlData.read_file(os.path.join(COMMANDS_PATH, 'unknown_command.yaml'))
        except FileNotFoundError as e:
            raise FileNotExists(path=os.path.join(COMMANDS_PATH, 'unknown_command.yaml'))
        return CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                                    speech_list=command[SPEECH_LIST],
                                                    command_class='')
    
    @staticmethod
    def wake_up() -> str:
        try:
            command = YamlData.read_file(os.path.join(COMMANDS_PATH, 'wake_up.yaml'))
        except FileNotFoundError as e:
            raise FileNotExists(path=os.path.join(COMMANDS_PATH, 'wake_up.yaml'))
        return CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                                    speech_list=command[SPEECH_LIST],
                                                    command_class='')
    

    class Cli(Command):
        """
        Cli COMMAND PROCESSOR

        FOR EXECUTING CLI COMMANDS
        """
        @staticmethod
        def exec_cmd_command(cmd_command : str) -> (str):
            cmd_output = ''
            try:
                cmd_output = subprocess.check_output(cmd_command, shell=True, universal_newlines=True, encoding='cp866')
            except subprocess.CalledProcessError as e:
                raise ExecCliCommandError(command=cmd_command, code=e.returncode, output=e)
            return cmd_output

        @staticmethod
        def process(command : dict, command_class : str, voice_input : str) -> str:
            output = ''
            try:
                if CMD_ARGS in command.keys():
                    cmd_arguments = ArgumentsProcessor.recognize_arguments(command, command_class, voice_input)
                else:
                    cmd_arguments = []
                command_output = CommandProcessor.Cli.exec_cmd_command(ArgumentsProcessor.concat_cmd_command_and_arguments(command[CMD_COMMAND], cmd_arguments))
                output = CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE], 
                                            speech_list=command[SPEECH_LIST], 
                                            speech_output=command[SPEECH_OUTPUT], 
                                            command_output=command_output, 
                                            command_class=command_class)
            except ExecCliCommandError as e:
                e.command_class = command_class
                e.proccess_critical_error()
                output = None
            except ArgumentError as e:
                e.proccess_critical_error()
                output = None

            return output

        def lint_type(self, command : dict, command_class : str) -> dict:
            try:
                a = command[CMD_COMMAND]
            except Exception as e:
                raise CommandSyntaxInYamlError(command_class=command_class,
                                            key=e)
            return command


    class Dialog(Command):
        """
        Dialog COMMAND PROCESSOR
        
        FOR CREATING A DIALOG
        """
        @staticmethod
        def process(command : dict, command_class : str, voice_input : str) -> str:
            output = CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                  speech_list=command[SPEECH_LIST],
                                  command_class=command_class)
    
            return output
    
    class OpenLink(Command):
        """
        OpenLink COMMAND PROCESSOR
        
        OPEN A LINK IN BROWSER
        """
        @staticmethod
        def open_link(link : str) -> str:
            webbrowser.open(link)

        @staticmethod
        def process(command : dict, command_class : str, voice_input : str) -> str:
            output = ''
            CommandProcessor.OpenLink.open_link(command[LINK])
            output = CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                        speech_list=command[SPEECH_LIST],
                                        command_class=command_class)
            return output   
        
        def lint_type(self, command : dict, command_class : str) -> dict:
            try:
                a = command[LINK]
            except Exception as e:
                raise CommandSyntaxInYamlError(command_class=command_class,
                                            key=e)
            return command


    class Wikipedia(Command):
        """
        Wikipedia COMMAND PROCESSOR
        
        PARSE A PAGE FROM A WIKIPEDIA
        """
        @staticmethod
        def wikipedia_search(search_for : list) -> str:
            result = ''
            try:
                wiki_wiki = wikipediaapi.Wikipedia('VA (Ivy)', 'ru')
            except Exception as e:
                raise WikipediaApiError(command_class='wikipedia',
                                        search_for=search_for)

            for i in range(len(search_for)):
                try:
                    page_py = wiki_wiki.page(search_for[i])

                    if page_py.exists():
                        if 'может означать:' in page_py.summary:
                            result = page_py.summary
                        else:
                            page = StringProcessing.remove_brackets(page_py.summary)
                            dash = page.find('—')
                            dot = page.find('.', dash + 1)
                            result = page[0:dot+1]
                except Exception as e:
                    logging.warning(e)
            
            if not result:
                raise WikipediaNotFoundError(search_for=search_for, command_class='wikipedia')
            return result

        @staticmethod
        def process(command : dict, command_class : str, voice_input : str) -> str:
            output = ''
            try:
                search_for = ArgumentsProcessor.recognize_arguments(command, command_class, voice_input)
                wiki_output = CommandProcessor.Wikipedia.wikipedia_search(search_for)
                output = CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                            speech_list=command[SPEECH_LIST],
                                            command_class=command_class,
                                            command_output=wiki_output,
                                            speech_output=command[SPEECH_OUTPUT])
            except ArgumentError as e:
                e.proccess_critical_error()
                output = None
            except WikipediaNotFoundError as e:
                e.proccess_warning()
                output = None
            except WikipediaApiError as e:
                e.proccess_warning()
                output = None

            return output  
        
        def lint_type(self, command : dict, command_class : str) -> dict:
            try:
                a = command[CMD_ARGS]
            except Exception as e:
                raise CommandSyntaxInYamlError(command_class=command_class,
                                            key=e)
            return command

    
    class Random(Command):
        """
        Random COMMAND PROCESSOR
        
        GENERATE RANDOM NUMBERS FROM A TO B
        """
        @staticmethod
        def random_numbers(argument : list=[1, 100000]) -> int:
            argument = list(map(int, argument))
            try:
                if len(argument) == 0:
                    answer = rnd.randint(1, 100000)
                elif len(argument) == 1:
                    answer = rnd.randint(argument[0], 100000)
                elif len(argument) == 2:
                    answer = rnd.randint(argument[0], argument[1])
                elif len(argument) > 2:
                    answer = rnd.choice(argument)
            except ValueError:
                answer = rnd.randint(argument[0], argument[0] + argument[1])

            return answer

        @staticmethod
        def process(command : dict, command_class : str, voice_input : str) -> str:
            output = ''
            try:
                arguments = ArgumentsProcessor.recognize_arguments(command, command_class, voice_input)
                answer = CommandProcessor.Random.random_numbers(arguments)
                output = CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                            speech_list=command[SPEECH_LIST],
                                            command_class=command_class,
                                            command_output=answer,
                                            speech_output=command[SPEECH_OUTPUT])
            except ArgumentError as e:
                e.proccess_critical_error()
                output = None

            return output

    
    class Ahk(Command):
        """
        Ahk COMMAND PROCESSOR
        
        EXECUTE AHK SCRIPT
        """
        @staticmethod
        def process(command : dict, command_class : str, voice_input : str) -> str:
            output = ''
            try:
                arguments = ArgumentsProcessor.recognize_arguments(command, command_class, voice_input)
                print("ARGUMENTS: ", arguments)
                ahk_path = os.path.join(command[COMMAND_FOLDER], os.path.normpath(command[AHK_PATH]))
                cmd_output = subprocess.call([ahk_path, "".join(arguments)])
                output = CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                            speech_list=command[SPEECH_LIST],
                                            command_class=command_class)
            except ArgumentError as e:
                e.proccess_critical_error()
                output = None
            return output
        
        def lint_type(self, command : dict, command_class : str) -> dict:
            try:
                a = command[AHK_PATH]
            except Exception as e:
                raise CommandSyntaxInYamlError(command_class=command_class,
                                            key=e)
            return command


    class ImgMacro(Command):
        """
        ImgMacro COMMAND PROCESSOR
        
        EXECUTE ImgMacro SCRIPT
        click to image or simple macro
        """
        @staticmethod
        def process(command : dict, command_class : str, voice_input : str) -> str:
            output = ''

            marco = command[IMG_MACRO]
            imacro = IMacro(path_to_command=YamlData.path_to_command(command_class),
                            check_all_screens=command[CHECK_ALL_SCREENS])
            
            imacro.execute_macro(marco)

            output = CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                        speech_list=command[SPEECH_LIST],
                                        command_class=command_class)

            return output

        def lint_unnecessary(self, command : dict) -> dict:
            command = super().lint_unnecessary(command)
            try:
                a = command[CHECK_ALL_SCREENS]
            except:
                command[CHECK_ALL_SCREENS] = True
            return command
        
        def lint_type(self, command : dict, command_class : str) -> dict:
            try:
                a = command[IMG_MACRO]
            except Exception as e:
                raise CommandSyntaxInYamlError(command_class=command_class,
                                            key=e)
            return command


    class Trigger(Command):
        """
        Trigger COMMAND PROCESSOR
        
        USE TO STOP IMG CHECKING FOR ImgMacro
        """
        @staticmethod
        def process(command : dict, command_class : str, voice_input : str) -> str:
            output = ''
            trigger = command[TRIGGER]
            threads = threading.enumerate()

            for thread in threads:
                if thread.name == trigger:
                    thread_id = ctypes.c_long(thread.ident)
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
                    # IMacro.trigger_stop = trigger

            output = CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                        speech_list=command[SPEECH_LIST],
                                        command_class=command_class)

            return output
        
        def lint_type(self, command : dict, command_class : str) -> dict:
            try:
                a = command[TRIGGER]
            except Exception as e:
                raise CommandSyntaxInYamlError(command_class=command_class,
                                            key=e)
            return command
    

    class OpenProgram(Command):
        """
        OpenProgram COMMAND PROCESSOR
        
        OPEN A PROGRAMM
        """
        @staticmethod
        def process(command : dict, command_class : str, voice_input : str) -> str:
            output = ''

            program_path = YamlData.get_program_path(command[PROGRAM])

            os.system(program_path)

            output = CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                        speech_list=command[SPEECH_LIST],
                                        command_class=command_class)
            return output

        def lint_type(self, command : dict, command_class : str) -> dict:
            try:
                a = command[PROGRAM]
            except Exception as e:
                raise CommandSyntaxInYamlError(command_class=command_class,
                                            key=e)
            return command
        
    
    class Hybrid(Command):
        """
        Hybrid COMMAND PROCESSOR
        
        CUSTOM COMMAND (PRESETS)
        """
        @staticmethod
        def process(command : dict, command_class : str, voice_input : str) -> str:
            output = ''

            command_hybrid = command[COMMAND]
            commands_output = ''

            try:
                for cmd in command_hybrid:
                    cmd = list(cmd.values())[0]

                    command_processor = CommandExecutor.exec_command[cmd[COMMAND_TYPE]]()

                    command = command_processor.lint_hybrid(cmd, command_class)

                    commands_output += command_processor.process(command, command_class, voice_input)  
            except CommandSyntaxInYamlError as e:
                raise CommandSyntaxInYamlError(command_class=command_class,
                                            key=e.key)
            except Exception as e:
                raise UnknownError(command_class=command_class,
                                message=e)
            


            output = CommandProcessor.create_speech_output(speech_type=command[SPEECH_TYPE],
                                        speech_list=command[SPEECH_LIST],
                                        speech_output=command[SPEECH_OUTPUT],
                                        command_class=command_class,
                                        command_output=commands_output)
            
            return output
        
        def lint_type(self, command: dict, command_class: str) -> dict:
            try:
                a = command[COMMAND]
            except Exception as e:
                raise CommandSyntaxInYamlError(command_class=command_class,
                                            key=e)
            return command
        

class CommandExecutor:
    """
    COMMAND EXECUTOR

    EXEC NECESSARY COMMAND TYPE PARSER BASED ON COMMAND CLASS
    """
    exec_command = {
        CMD : CommandProcessor.Cli,
        DIALOG : CommandProcessor.Dialog,
        OPEN_LINK : CommandProcessor.OpenLink,
        WIKIPEDIA : CommandProcessor.Wikipedia,
        RANDOM : CommandProcessor.Random,
        AHK : CommandProcessor.Ahk,
        IMG_MACRO : CommandProcessor.ImgMacro,
        TRIGGER : CommandProcessor.Trigger,
        OPEN_PROGRAM : CommandProcessor.OpenProgram,
        HYBRID : CommandProcessor.Hybrid
    }

    @staticmethod
    def exec_nessesary_command(command_class : str, voice_input : str) -> str:
        output = ''
        try:
            if command_class is None:
                output = CommandProcessor.unknown_command()
            elif command_class == WAKE_UP:
                output = CommandProcessor.wake_up()
            else:         
                voice_input = WordNum.word_to_num_in_string(voice_input)

                command = YamlData.load_command_data(command_class)[command_class]
                command_processor = CommandExecutor.exec_command[command[COMMAND_TYPE]]()

                command = command_processor.lint(command, command_class)

                output = command_processor.process(command, command_class, voice_input)

                output = WordNum.num_to_word_in_string(output)
        except KeyError as e:
            try:
                raise CommandAccessError(command_class=command_class,
                                        access_to=e)
            except CommandAccessError as e:
                e.proccess_critical_error()
            output = None
        except CommandSyntaxInYamlError as e:
            e.proccess_critical_error()
            output = None
        except UnknownError as e:
            e.proccess_critical_error()
            output = None
        except FileNotExists as e:
            e.proccess_critical_error()
            output = None
        return output

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

from config import *
import tts
from errors import *
import func as f
import img_macro as imarco

logging.basicConfig(level=logging.INFO, filename='logs/log.log', filemode='w')

# commands = dict(yaml.safe_load(open('data/commands/commands.yaml', 'r', encoding='utf-8')))

def all_list_to_str(lst : list) -> list:
    r"""
    CONVERT ALL LIST ELEMENTS TO STR
    EXAMPLE:
    >>> lst = [1, 2, 3]
    >>> all_list_to_str(lst)
    ['1', '2', '3']
    """
    return list(map(str, lst))

def unpack_matches(re_arguments : list) -> str:
    r"""
    UNPACK MATCHES FROM RE ARGUMENTS
    EXAMPLE:
    >>> re_arguments = ['монетка', 'монетку', 'монетки']
    result = 'монетка монетку монетки'

    >>> re_arguments = [('2', 'часа'), ('5', 'минут')]
    result = '2 часа 5 минут'
    """
    result = ''
    if is_multi_group_match(re_arguments):
        for match in re_arguments:
            for m in match:
                result += m + ' '
    else:
        for match in re_arguments:
            result += match
    return result

def concat_arguments(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> str:
    r"""
    CONCAT ARGUMENTS FROM RE ARGUMENTS TO CMD ARGUMENTS
    EXAMPLE:
    >>> cmd_arguments = ['1', '2']
    >>> re_arguments = [('3', '4'), ('5', '6')]
    cmd_arguments = ['1', '2', '3', '4', '5', '6']

    >>> cmd_arguments = ['1', '2']
    >>> re_arguments = ['3', '4']
    cmd_arguments = ['1', '2', '3', '4']
    """
    cmd_arguments.append(prefix + unpack_matches(re_arguments) + postfix)
    return cmd_arguments

def re_arg_to_list(re_arguments : list) -> list:
    r"""
    CONVERT RE ARGUMENTS TO LIST
    EXAMPLE:
    >>> re_arguments = [('3', '4'), ('5', '6')]
    result = ['3', '4', '5', '6']

    >>> re_arguments = ['3', '4']
    result = ['3', '4']
    """
    result = []
    if is_multi_group_match(re_arguments):
        for match in re_arguments:
            for m in match:
                result.append(m)
    else:
        for match in re_arguments:
            result.append(match)
    return result

def add_each_re_arg(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
    r"""
    ADD EACH RE ARGUMENT TO CMD ARGUMENTS
    EXAMPLE:
    >>> cmd_arguments = ['1', '2']
    >>> re_arguments = [('3', '4'), ('5', '6')]
    cmd_arguments = ['1', '2', '3', '4', '5', '6']

    >>> cmd_arguments = ['1', '2']
    >>> re_arguments = ['3', '4']
    cmd_arguments = ['1', '2', '3', '4']
    """
    if is_multi_group_match(re_arguments):
        re_arguments = re_arg_to_list(re_arguments)
    for i in range(len(re_arguments)):
        cmd_arguments.append(prefix + re_arguments[i] + postfix)
    
    return cmd_arguments

def format_each_match_concat(re_arguments : list) -> list:
    r"""
    FORMAT EACH MATCH FROM RE ARGUMENTS AND CONCAT THEY
    EXAMPLE:
    >>> re_arguments = [('3', '4'), ('5', '6')]
    result = ['34', '56']

    >>> re_arguments = ['3', '4']
    result = ['3', '4']
    """
    new_re_arg = []
    if is_multi_group_match(re_arguments):
        for i in range(len(re_arguments)):
            arg = ''
            for j in range(len(re_arguments[i])):
                arg += re_arguments[i][j]
            new_re_arg.append(arg)
    else:
        new_re_arg = re_arguments
    
    return new_re_arg

def add_each_match(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
    r"""
    ADD EACH MATCH FROM RE ARGUMENTS TO CMD ARGUMENTS
    EXAMPLE:
    >>> cmd_arguments = ['1', '2']
    >>> re_arguments = [('3', '4'), ('5', '6')]
    cmd_arguments = ['1', '2', '34', '56']

    >>> cmd_arguments = ['1', '2']
    >>> re_arguments = ['3', '4']
    cmd_arguments = ['1', '2', '3', '4']
    """
    new_re_arg = format_each_match_concat(re_arguments)
    
    for i in range(len(new_re_arg)):
        cmd_arguments.append(prefix + new_re_arg[i] + postfix)

    return cmd_arguments

def pick_first_match_arg(cmd_arguments : list, re_arguments : list, prefix : str, postfix : str) -> list:
    r"""
    PICK FIRST MATCH FROM RE ARGUMENTS
    EXAMPLE:
    >>> cmd_arguments = ['1', '2']
    >>> re_arguments = [('3', '4'), ('5', '6')]
    cmd_arguments = ['1', '2', '34']

    >>> cmd_arguments = ['1', '2']
    >>> re_arguments = ['3', '4']

    cmd_arguments = ['1', '2', '3']
    """
    re_arguments = format_each_match_concat(re_arguments)
    cmd_arguments.append(prefix + re_arguments[0] + postfix)
    return cmd_arguments

def recognize_arguments(command: dict, command_class: str, voice_input: str) -> (list, list):
    switch_arg_sep = {
                    ADD_EACH : add_each_re_arg,
                    CONCAT : concat_arguments,
                    PICK_FIRST_MATCH : pick_first_match_arg
                }
    cmd_arguments = []
    speech_args = []
    for arg, params in command[CMD_ARGS].items():
        if params[REGEX_ON] == True:
            try:
                re_arguments = take_arg_from_string(voice_input, arg)
            except RegexArgumentError as e:
                e.command_class = command_class
                e.proccess_critical_error()
                if command_class != 'random/number':
                    raise ArgumentError(command_class=command_class, argument=arg) from e  
                else:
                    re_arguments = []
            except RegexPatternError as e:
                e.command_class = command_class
                e.proccess_critical_error()
                raise ArgumentError(command_class=command_class, argument=arg) from e
                  
            arg = re_arguments
            if command[SPEECH_ARGS] == True:
                speech_args.append(unpack_matches(arg))
            
            if command_class == 'shutdown/timer':
                cmd_arguments.append(params[PREFIX] + str(f.convert_to_seconds(arg)) + params[POSTFIX])
            elif command_class == 'wikipedia':
                cmd_arguments.append(params[PREFIX] + arg[0][-1] + params[POSTFIX])
            else:
                cmd_arguments = switch_arg_sep[command[ARGS_SEP]](cmd_arguments, arg, params[PREFIX], params[POSTFIX])

            # if command[ARGS_SEP] == ADD_EACH:
            #     cmd_arguments = add_each_re_arg(cmd_arguments, re_arguments)
            # elif command[ARGS_SEP] == CONCAT:
            #     cmd_arguments.append(unpack_matches(re_arguments))
            # elif command[ARGS_SEP] == PICK_FIRST_MATCH:
            
        else:
            arg = params[PREFIX] + str(arg) + params[POSTFIX]
            cmd_arguments.append(arg)

    return cmd_arguments, speech_args

def concat_cmd_command_and_arguments(cmd_command : str, cmd_arguments : list) -> str:
    if cmd_arguments:
        return cmd_command + ' ' + ' '.join(cmd_arguments)
    return cmd_command

def exec_cmd_command(cmd_command : str) -> (str):
    cmd_output = ''
    try:
        cmd_output = subprocess.check_output(cmd_command, shell=True, universal_newlines=True, encoding='cp866')
    except subprocess.CalledProcessError as e:
        raise ExecCliCommandError(command=cmd_command, code=e.returncode, output=e)
    return cmd_output

def create_speech_output(speech_type : str, speech_list : list, command_class : str, command_output : str = None, speech_output : bool = False) -> str:
    phrase = ''
    if speech_type == DYNAMIC:

        if speech_list != None:
            phrase += rnd.choice(speech_list)

        if speech_output == True:
            phrase += ' '

            if 'time' in command_class:
                command_output = f.time_format_for_string(command_output)

            phrase += str(command_output)
            
    return phrase

def is_multi_group_match(match : list) -> bool:
    if len(match) > 0:
        return type(match[0]) == tuple
    return False

def take_arg_from_string(voice_input : str, arg : str):
    nums_voice_input = f.word_to_num_in_string(voice_input)
    regex = arg

    try:
        pattern = re.compile(regex)
    except TypeError:
        raise RegexPatternError(argument=arg)

    match = pattern.findall(nums_voice_input)

    if not match:
        raise RegexArgumentError(argument=arg)
    return match

def cmd_command_proccessing(command : dict, command_class : str, voice_input : str) -> str:
    output = ''
    try:
        if CMD_ARGS in command.keys():
            cmd_arguments, speech_args = recognize_arguments(command, command_class, voice_input)
        else:
            cmd_arguments = []
        command_output = exec_cmd_command(concat_cmd_command_and_arguments(command[CMD_COMMAND], cmd_arguments))
        output = create_speech_output(speech_type=command[SPEECH_TYPE], 
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

def dialog_command_proccessing(command : dict, command_class : str, voice_input : str) -> str:
    output = create_speech_output(speech_type=command[SPEECH_TYPE],
                                  speech_list=command[SPEECH_LIST],
                                  command_class=command_class)
    
    return output

def open_link(link : str) -> str:
    webbrowser.open(link)

def open_link_command_proccessing(command : dict, command_class : str, voice_input : str) -> str:
    output = ''
    open_link(command[LINK])
    output = create_speech_output(speech_type=command[SPEECH_TYPE],
                                  speech_list=command[SPEECH_LIST],
                                  command_class=command_class)
    return output


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
                    page = f.remove_brackets(page_py.summary)
                    dash = page.find('—')
                    dot = page.find('.', dash + 1)
                    result = page[0:dot+1]
        except Exception as e:
            logging.warning(e)
    
    if not result:
        raise WikipediaNotFoundError(search_for=search_for, command_class='wikipedia')
    return result


def wikipedia_command_proccessing(command : dict, command_class : str, voice_input : str) -> str:
    output = ''
    try:
        search_for, speech_args = recognize_arguments(command, command_class, voice_input)
        wiki_output = wikipedia_search(search_for)
        output = create_speech_output(speech_type=command[SPEECH_TYPE],
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

def fix_command_params(command : dict, command_class : str) -> dict:
    command[COMMAND_FOLDER] = f.path_to_command(command_class)
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

    try:
        a = command[SPEECH_TYPE]
        a = command[SPEECH_LIST]
        a = command[COMMAND_TYPE]
        a = command[PHRASES]
        if command[COMMAND_TYPE] == CMD:
            a = command[CMD_COMMAND]
        elif command[COMMAND_TYPE] == OPEN_LINK:
            a = command[LINK]
        elif command[COMMAND_TYPE] == AHK:
            a = command[AHK_PATH]
        elif command[COMMAND_TYPE] == WIKIPEDIA:
            a = command[CMD_ARGS]
        elif command[COMMAND_TYPE] == IMG_MACRO:
            a = command[IMG_MACRO]
    except Exception as e:
        raise CommandSyntaxInYamlError(command_class=command_class,
                                       key=e)

    return command

def random_numbers(argument : list=[1, 100000]) -> (int, int):
    argument = list(map(int, argument))
    if len(argument) == 0:
        answer = rnd.randint(1, 100000)
    elif len(argument) == 1:
        answer = rnd.randint(argument[0], 100000)
    elif len(argument) == 2:
        answer = rnd.randint(argument[0], argument[1])
    elif len(argument) > 2:
        answer = rnd.choice(argument)

    return answer

def random_command_proccessing(command : dict, command_class : str, voice_input : str) -> str:
    output = ''
    try:
        arguments, speech_args = recognize_arguments(command, command_class, voice_input)
        answer = random_numbers(arguments)
        output = create_speech_output(speech_type=command[SPEECH_TYPE],
                                      speech_list=command[SPEECH_LIST],
                                      command_class=command_class,
                                      command_output=answer,
                                      speech_output=command[SPEECH_OUTPUT])
    except ArgumentError as e:
        e.proccess_critical_error()
        output = None

    return output


def ahk_command_proccessing(command : dict, command_class : str, voice_input : str) -> str:
    output = ''
    try:
        arguments, speech_args = recognize_arguments(command, command_class, voice_input)
        print("ARGUMENTS: ", arguments)
        ahk_path = os.path.join(command[COMMAND_FOLDER], os.path.normpath(command[AHK_PATH]))
        cmd_output = subprocess.call([ahk_path, "".join(arguments)])
        output = create_speech_output(speech_type=command[SPEECH_TYPE],
                                    speech_list=command[SPEECH_LIST],
                                    command_class=command_class)
    except ArgumentError as e:
        e.proccess_critical_error()
        output = None
    return output

def img_macro_command_proccessing(command : dict, command_class : str, voice_input : str) -> str:
    output = ''

    marco = command[IMG_MACRO]

    imarco.execute_macro(marco, f.path_to_command(command_class))

    output = create_speech_output(speech_type=command[SPEECH_TYPE],
                                  speech_list=command[SPEECH_LIST],
                                  command_class=command_class)

    return output

def exec_nessesary_command(command_class : str, voice_input : str) -> str:
    output = ''
    try:
        # command = f.load_command_data(command_class)
        command = f.load_command_data(command_class)[command_class]
        command = fix_command_params(command, command_class)

        if command[COMMAND_TYPE] == CMD:
            output = cmd_command_proccessing(command, command_class, voice_input)
        elif command[COMMAND_TYPE] == DIALOG:
            output = dialog_command_proccessing(command, command_class, voice_input)
        elif command[COMMAND_TYPE] == OPEN_LINK:
            output = open_link_command_proccessing(command, command_class, voice_input)
        elif command[COMMAND_TYPE] == WIKIPEDIA:
            output = wikipedia_command_proccessing(command, command_class, voice_input)
        elif command[COMMAND_TYPE] == RANDOM:
            output = random_command_proccessing(command, command_class, voice_input)
        elif command[COMMAND_TYPE] == AHK:
            output = ahk_command_proccessing(command, command_class, voice_input)
        elif command[COMMAND_TYPE] == IMG_MACRO:
            output = img_macro_command_proccessing(command, command_class, voice_input)
        output = f.num_to_word_in_string(output)
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
    return output
    # exec(commands[command_class]['function'] + f"({commands[command_class]['function_args']})")


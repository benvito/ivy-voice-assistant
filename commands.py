import time
import yaml
import os
import random as rnd
import subprocess
import re
import logging

from config import *
import tts
from errors import Error
import func as f

logging.basicConfig(level=logging.INFO, filename='logs/log.log', filemode='w')

commands = dict(yaml.safe_load(open('data/commands/commands.yaml', 'r', encoding='utf-8')))

def recognize_arguments(command: dict, command_class: str, voice_input: str) -> (list, list, Error):
    cmd_arguments = []
    speech_args = []
    error = Error()
    for arg_dict in command[CMD_ARGS]:
        for arg, re_on in arg_dict.items():
            if re_on == True:
                re_arguments = take_arg_from_string(voice_input, arg)

                if re_arguments:
                    if command[SPEECH_ARGS] == True:
                        speech_args.append(str(re_arguments) if type(re_arguments) != list else re_arguments)

                    if command_class == 'shutdown_timer':
                        re_arguments = f.convert_to_seconds(re_arguments)

                    cmd_arguments.append(str(re_arguments) if type(re_arguments) != list else re_arguments)
                else:
                    error.code = 4
                    error.message = f'Не могу распознать аргумент под номером {command[CMD_ARGS].index(arg_dict) + 1}'

            else:
                cmd_arguments.append(arg)
    
    return cmd_arguments, speech_args, error

def format_cmd_command(cmd_command : str, cmd_arguments : list) -> str:
    return cmd_command + ' ' + ' '.join(cmd_arguments)

def exec_cmd_command(cmd_command : str) -> (str, Error):
    error = Error()
    cmd_output = 'Не удалось выполнить команду'
    try:
        cmd_output = subprocess.check_output(cmd_command, shell=True, universal_newlines=True, encoding='cp866')
    except subprocess.CalledProcessError as e:
        error.code = e.returncode
        error.message = e
    return cmd_output, error

def create_speech_output(speech_type : str, speech_list : list, speech_output : bool, command_output : str, command_class : str, error_exec_cmd: Error) -> str:
    phrase = ''

    if speech_type == DYNAMIC:
        phrase = ''
        if speech_list != None and error_exec_cmd.code == 0:
            phrase += rnd.choice(speech_list) + ' '
        if speech_output == True:
            if 'time' in command_class:
                command_output = f.time_format_for_string(command_output)
            phrase += str(command_output)
    return phrase

def take_arg_from_string(voice_input : str, arg : str):
    nums_voice_input = f.word_to_num_in_string(voice_input)
    regex = arg

    pattern = re.compile(regex)

    match = pattern.findall(nums_voice_input)

    return match

def exec_nessesary_command(command_class : str, voice_input : str) -> str:
    output = ''
    command = commands[command_class]
    if command[COMMAND_TYPE] == CMD:
        if CMD_ARGS in command.keys():
            cmd_arguments, speech_args, error_recognize = recognize_arguments(command, command_class, voice_input)
        
        if error_recognize.code == 0:
            command_output, error_exec_cmd = exec_cmd_command(format_cmd_command(command[CMD_COMMAND], cmd_arguments))
            
            output = create_speech_output(command[SPEECH_TYPE], command[SPEECH_LIST], command[SPEECH_OUTPUT], command_output, command_class, error_exec_cmd)
        else:
            logging.critical(error_recognize.message)
            output = error_recognize.message
    
    if error_exec_cmd.code != 0:
        logging.critical(error_exec_cmd.message)
    print(cmd_arguments, speech_args)
    output = f.num_to_word_in_string(output)
    return output
    # exec(commands[command_class]['function'] + f"({commands[command_class]['function_args']})")


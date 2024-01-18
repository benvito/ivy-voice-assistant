import time
import yaml
import os
import random as rnd
import subprocess
import re
import logging

from config import *
import tts
from errors import *
import func as f

logging.basicConfig(level=logging.INFO, filename='logs/log.log', filemode='w')

commands = dict(yaml.safe_load(open('data/commands/commands.yaml', 'r', encoding='utf-8')))

def recognize_arguments(command: dict, command_class: str, voice_input: str) -> (list, list):
    cmd_arguments = []
    speech_args = []
    for arg_dict in command[CMD_ARGS]:
        for arg, re_on in arg_dict.items():
            if re_on == True:
                try:
                    re_arguments = take_arg_from_string(voice_input, arg)
                except RegexArgumentError as e:
                    e.command_class = command_class
                    e.log_critical_error()
                    raise ArgumentError(command_class=command_class, argument=arg) from e       
                
                if command[SPEECH_ARGS] == True:
                    speech_args.append(str(re_arguments) if type(re_arguments) != list else re_arguments)

                if command_class == 'shutdown_timer':
                    re_arguments = f.convert_to_seconds(re_arguments)

                cmd_arguments.append(str(re_arguments) if type(re_arguments) != list else re_arguments)
            else:
                cmd_arguments.append(arg)
    
    return cmd_arguments, speech_args

def format_cmd_command(cmd_command : str, cmd_arguments : list) -> str:
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


def take_arg_from_string(voice_input : str, arg : str):
    nums_voice_input = f.word_to_num_in_string(voice_input)
    regex = arg

    pattern = re.compile(regex)

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
        command_output = exec_cmd_command(format_cmd_command(command[CMD_COMMAND], cmd_arguments))
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

def exec_nessesary_command(command_class : str, voice_input : str) -> str:
    output = ''
    try:
        command = commands[command_class]
        if command[COMMAND_TYPE] == CMD:
            output = cmd_command_proccessing(command, command_class, voice_input)
        elif command[COMMAND_TYPE] == DIALOG:
            output = dialog_command_proccessing(command, command_class, voice_input)
        output = f.num_to_word_in_string(output)
    except KeyError as e:
        try:
            raise CommandAccessError(command_class=command_class,
                                     access_to=e)
        except CommandAccessError as e:
            e.proccess_critical_error()
        output = None
    return output
    # exec(commands[command_class]['function'] + f"({commands[command_class]['function_args']})")


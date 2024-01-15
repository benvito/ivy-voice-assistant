import time
import func as f
import yaml
from config import *
import os
import random as rnd
import subprocess
import re

commands = dict(yaml.safe_load(open('data/commands/commands.yaml', 'r', encoding='utf-8')))

def format_cmd_command(cmd_command : str, cmd_arguments : list) -> str:
    return cmd_command + ' ' + ' '.join(cmd_arguments)

def exec_cmd_command(cmd_command : str):
    return subprocess.check_output(cmd_command, shell=True, universal_newlines=True, encoding='cp866')

def create_speech_output(speech_type : str, speech_list : list, speech_output : bool, command_output : str, command_class : str) -> str:
    phrase = ''

    if speech_type == DYNAMIC:
        phrase = ''
        if speech_list != None:
            phrase += rnd.choice(speech_list)
        if speech_output == True:
            if 'time' in command_class:
                command_output = f.time_fomat_for_string(command_output)
            phrase += ' ' + str(command_output)
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
    print(command)
    if command[COMMAND_TYPE] == CMD:
        cmd_arguments = []
        speech_args = []

        if CMD_ARGS in command.keys():
            for arg_dict in command[CMD_ARGS]:
                for arg, re_on in arg_dict.items():
                    if re_on == True:

                        re_arguments = take_arg_from_string(voice_input, arg)

                        if command[SPEECH_ARGS] == True:
                            speech_args.append(str(re_arguments))

                        if command_class == 'shutdown_timer':
                            re_arguments = f.convert_to_seconds(re_arguments)

                        if re_arguments:
                            cmd_arguments.append(str(re_arguments))
                        else:
                            output = f'Не могу распознать аргумент под номером {command[CMD_ARGS].index(arg_dict) + 1}'
                            return output
                    else:
                        cmd_arguments.append(arg)

        command_output = exec_cmd_command(format_cmd_command(command[CMD_COMMAND], cmd_arguments))
        output = create_speech_output(command[SPEECH_TYPE], command[SPEECH_LIST], command[SPEECH_OUTPUT], command_output, command_class)
    
    print(cmd_arguments, speech_args)
    output = f.num_to_word_in_string(output)
    return output
    # exec(commands[command_class]['function'] + f"({commands[command_class]['function_args']})")

            




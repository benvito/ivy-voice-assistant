import time
import func as f
import yaml
from config import *
import os
import random as rnd
import subprocess

commands = dict(yaml.safe_load(open('data/commands/commands.yaml', 'r', encoding='utf-8')))

def exec_cmd_command(cmd_command : str):
    return subprocess.check_output(cmd_command, shell=True, universal_newlines=True, encoding='cp866')

def say_command_output(speech_type : str, speech_list : list, speech_output : bool, command_output : str):
    phrase = ''

    if speech_type == DYNAMIC:
        phrase = ''
        if speech_list != None:
            phrase += rnd.choice(speech_list)
        if speech_output == True:
            phrase += ' ' + str(command_output)
    
    return phrase

def exec_nessesary_command(command_class : str):
    output = ''
    command = commands[command_class]

    if command[COMMAND_TYPE] == CMD:
        command_output = exec_cmd_command(command[CMD_COMMAND])
        output = say_command_output(command[SPEECH_TYPE], command[SPEECH_LIST], command[SPEECH_OUTPUT], command_output)
    
    return output
    # exec(commands[command_class]['function'] + f"({commands[command_class]['function_args']})")

            




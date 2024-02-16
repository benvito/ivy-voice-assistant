import yaml
import os

from config.config import PATH
from utils.decorators import exec_timer
from utils import BASE_DIR


class YamlData:
    @staticmethod
    def get_program_path(program_name : str) -> str:
        yaml_path = os.path.join(BASE_DIR, 'data', 'commands', 'programs.yaml')
        programs_data = dict(yaml.safe_load(open(yaml_path, 'r', encoding='utf-8')))
        program_path = os.path.normpath(programs_data[program_name][PATH])
        if 'username' in program_path:
            program_path = program_path.replace('username', os.environ['USERNAME'])
        return '"' + program_path + '"'

    @staticmethod
    @exec_timer
    def path_to_command(command_class : str) -> str:
        command_folder = command_class.split('/')[0]
        return os.path.join(BASE_DIR, 'data', 'commands', command_folder)

    @staticmethod
    @exec_timer
    def load_command_data(command_class : str) -> dict:
        command_folder = command_class.split('/')[0]
        yaml_path = os.path.join(BASE_DIR, 'data', 'commands', command_folder, 'commands.yaml')
        command_data = dict(yaml.safe_load(open(yaml_path, 'r', encoding='utf-8')))
        return command_data

    @staticmethod
    @exec_timer
    def load_all_commands_dict() -> dict:
        commands = dict()
        for dirName, subdirList, fileList in os.walk(os.path.join(BASE_DIR, 'data', 'commands')):
            if "commands.yaml" in fileList:
                commands.update(dict(yaml.safe_load(open(os.path.join(dirName, 'commands.yaml'), 'r', encoding='utf-8'))))
        return commands

    @staticmethod
    @exec_timer
    def load_all_commands_classes() -> list:
        commands = YamlData.load_all_commands_dict()
        return commands.keys()
    
    @staticmethod
    @exec_timer
    def load_all_commands_folders() -> list:
        commands_folders = dict()
        for dirName, subdirList, fileList in os.walk(os.path.join(BASE_DIR, 'data', 'commands')):
            if "commands.yaml" in fileList:
                commands_folders[dirName.split(os.sep)[-1]] = dirName
        return commands_folders

    @staticmethod
    @exec_timer
    def load_all_command_subfolders(path : str) -> list:
        subfolders = None
        for dirName, subdirList, fileList in os.walk(path):
            if "commands.yaml" in fileList:
                return subdirList
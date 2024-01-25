import cv2
import pprint
from config import IMG_MACRO,IMG,POSITION,DEFINE,WAIT,AIM,CLICK

def read_command(command : dict) -> (str, any):
    return list(command.keys())[0], list(command.values())[0]

def parse_macro(macro : list):
    pass
    
def execute_macro(macro : list):
    current_img_data = {
        IMG : '',
        POSITION : (0, 0),
    }
    macro_commands = {
        AIM : macro_aim,
        CLICK : macro_click
    }
    for command in macro:
        command, value = read_command(command)
        if command == DEFINE:
            current_img_data = img_define(current_img_data, value)
        elif command == WAIT:
            macro_wait(value)
        else:
            macro_commands[command](current_img_data, value)

def macro_aim(current_img_data : dict, value : str):
    print(f"aimed at {current_img_data[POSITION]} at {value}")

def macro_click(current_img_data : dict, value : int):
    print(f"clicked {value} at {current_img_data[POSITION]}")

def macro_wait(value : int):
    print(f"waited for a {value}")

def img_define(current_img_data : dict, image : str or list) -> dict:
    print(image)
    return current_img_data
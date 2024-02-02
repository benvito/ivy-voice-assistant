import cv2
import pprint
import pyautogui
import numpy as np
import os
import mss
import threading

from config import IMG_MACRO,IMG,POSITION,DEFINE,WAIT,AIM,CLICK,SIZE,CENTER,X,Y,STRAIGHT,WATCH,TRIGGER
import func as f

THRESHOLD = 0.8

def read_command(command : dict) -> (str, any):
    return list(command.keys())[0], list(command.values())[0]

def parse_macro(macro : list):
    pass
    
def execute_macro(macro : list, path_to_command : str, check_all_screens : bool = False):
    current_img_data = {
        IMG : None,
        POSITION : (None, None),
        SIZE : (None, None),
        TRIGGER : None
    }
    macro_commands = {
        AIM : macro_aim,
        CLICK : macro_click
    }
    for macro_dict in macro:
        type_macro = list(macro_dict.keys())[0]
        if type_macro == STRAIGHT:
            execute_straight_macro(macro_dict[type_macro], 
                                   path_to_command, 
                                   check_all_screens, 
                                   macro_commands,
                                   current_img_data)
        elif type_macro == WATCH:
            exec_watch_macros_thread = threading.Thread(name=path_to_command,
                                                        target=execute_watch_macro,
                                                        args=(macro_dict[type_macro],
                                                              path_to_command,
                                                              check_all_screens,
                                                              macro_commands,
                                                              current_img_data,))
            exec_watch_macros_thread.start()
            # execute_watch_macro(macro_dict[type_macro], 
            #                    path_to_command, 
            #                    check_all_screens, 
            #                    macro_commands,
            #                    current_img_data)

def execute_straight_macro(macro : dict, 
                           path_to_command : str, 
                           check_all_screens : bool = False, 
                           macro_commands : dict = {}, 
                           current_img_data : dict = {}):
    for command, value in macro.items():
        if command == DEFINE:
            current_img_data = img_define(current_img_data, value, path_to_command, check_all_screens)
        elif command == WAIT:
            macro_wait(value)
        else:
            macro_commands[command](current_img_data, value)

def execute_watch_macro(macro : dict, 
                       path_to_command : str, 
                       check_all_screens : bool = False, 
                       macro_commands : dict = {},
                       current_img_data : dict = {}):
    global trigger_stop
    trigger_stop = None
    for command, value in macro.items():
        if command == TRIGGER:
            current_img_data[TRIGGER] = value
            threading.current_thread().name = value
        elif command == DEFINE:
            print(current_img_data[IMG], current_img_data[TRIGGER])
            while current_img_data[IMG] is None and trigger_stop != threading.current_thread().name:
                current_img_data = img_define(current_img_data, value, path_to_command, check_all_screens)
                pyautogui.sleep(0.05)
        elif command == WAIT:
            macro_wait(value)
        else:
            macro_commands[command](current_img_data, value)

def macro_aim(current_img_data : dict, value : str):
    if current_img_data[IMG] is not None:
        AIM_TO = {
            CENTER : (current_img_data[POSITION][X] + current_img_data[SIZE][X] / 2, 
                    current_img_data[POSITION][Y] + current_img_data[SIZE][Y] / 2)
        }
        pyautogui.moveTo(AIM_TO[value])
        print(f"aimed at {current_img_data[POSITION]} at {value}")

def macro_click(current_img_data : dict, value : int):
    mouse_button = {
        1 : 'left',
        2 : 'right',
        3 : 'middle'
    }
    pyautogui.click(button=mouse_button[value])
    print(f"clicked {value} at {current_img_data[POSITION]}")

def macro_wait(value : float):
    pyautogui.sleep(float(value))
    print(f"waited for a {value}")

def get_img_size(image : str) -> (int, int):
    w, h = cv2.imread(image).shape[::-1][:2]
    return w, h

def get_img_pos(image : str, check_all_screens : bool) -> (int, int, int, int):
    if check_all_screens:
        with mss.mss() as sct:
            monitors = sct.monitors
            all_monitors_screen = sct.grab(monitors[0])
            screen_img = np.array(all_monitors_screen)
    else:
        screen_img = np.array(pyautogui.screenshot())
        
    screenshot = cv2.cvtColor(screen_img, cv2.COLOR_RGB2GRAY)
    template = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1][:2]
    result_match = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_match)
    if max_val > THRESHOLD:
        x, y = max_loc
        x -= abs(monitors[0]['left'])
        y -= abs(monitors[0]['top'])
        return x, y, w, h
    return None, None, None, None

def img_define(current_img_data : dict, image : str or list, path_to_command : str, check_all_screens : bool) -> dict:
    cur_img = None
    w, h = None, None
    if type(image) != list:
        image = [image]
    for img in image:
        img_x, img_y, w, h = get_img_pos(os.path.join(os.path.normpath(path_to_command), os.path.normpath(img)), check_all_screens)
        if img_x != None or img_y != None:
            cur_img = img
            break
    
    current_img_data[IMG] = cur_img
    current_img_data[POSITION] = (img_x, img_y)
    current_img_data[SIZE] = (w, h)

    print(current_img_data)
    return current_img_data
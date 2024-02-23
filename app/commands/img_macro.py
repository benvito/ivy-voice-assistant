import cv2
import pprint
import pyautogui
import numpy as np
import os
import mss
import threading

from config.constants import IMG_MACRO,PRESS,IMG,POSITION,DEFINE,WAIT,AIM,CLICK,SIZE,CENTER,X,Y,POS,MOVE,STRAIGHT,WATCH,TRIGGER,LEFT_TOP,RIGHT_TOP,LEFT_BOTTOM,RIGHT_BOTTOM,LEFT_CENTER,RIGHT_CENTER

THRESHOLD = 0.8


class IMacro:
    def __init__(self, path_to_command : str, check_all_screens : bool) -> None:
        pyautogui.FAILSAFE = False

        self.macro_commands = {
            TRIGGER : self.macro_trigger,
            PRESS : self.macro_press,
            DEFINE : self.macro_define,
            WAIT : self.macro_wait,
            MOVE : self.macro_move_to,
            POS : self.macro_position,
            AIM : self.macro_aim,
            CLICK : self.macro_click
        }

        self.current_img_data = self.init_img_data()

        self.mouse_button = {
            1 : 'left',
            2 : 'right',
            3 : 'middle'
        }

        self.path_to_command = path_to_command
        self.check_all_screens = check_all_screens
    
    def init_img_data(self):
        current_img_data = {
                IMG : None,
                POSITION : (None, None),
                SIZE : (None, None),
                TRIGGER : None
            }
        return current_img_data

    @staticmethod
    def read_command(command : dict) -> tuple:
        return list(command.keys())[0], list(command.values())[0]
      
    def execute_macro(self, macro : list):
        for macro_dict in macro:
            self.current_img_data = self.init_img_data()
            type_macro = list(macro_dict.keys())[0]
            if type_macro == STRAIGHT:
                self.execute_straight_macro(macro_dict[type_macro])
            elif type_macro == WATCH:
                exec_watch_macros_thread = threading.Thread(name=self.path_to_command,
                                                            target=self.execute_watch_macro,
                                                            args=(macro_dict[type_macro],))
                exec_watch_macros_thread.start()

    def execute_straight_macro(self,
                               macro : list):
        for line in macro:
            command, value = self.read_command(line)
            print(command, value)
            self.macro_commands[command](value)

    def execute_watch_macro(self,
                            macro : list):
        global trigger_stop
        trigger_stop = None
        for line in macro:
            command, value = self.read_command(line)
            if command == DEFINE:
                print(self.current_img_data[IMG], self.current_img_data[TRIGGER])
                while self.current_img_data[IMG] is None and trigger_stop != threading.current_thread().name:
                    self.current_img_data = self.img_define(value)
                    pyautogui.sleep(0.05)
            else:
                self.macro_commands[command](value)

    def macro_press(self, value : str):
        pyautogui.press(value)

    def macro_trigger(self, value : str):
        self.current_img_data[TRIGGER] = value
        threading.current_thread().name = value

    def macro_define(self, value : str):
        self.current_img_data = self.img_define(value)

    def macro_move_to(self, value : str):
        coords = list(map(int, value.split(" ")))
        pyautogui.moveRel(coords)

    def macro_position(self, value : str):
        coords = list(map(int, value.split(" ")))
        pyautogui.moveTo(coords)

    def macro_aim(self, value : str):
        if self.current_img_data[IMG] is not None:
            AIM_TO = {
                CENTER : (self.current_img_data[POSITION][X] + self.current_img_data[SIZE][X] / 2, 
                        self.current_img_data[POSITION][Y] + self.current_img_data[SIZE][Y] / 2),
                LEFT_TOP : (self.current_img_data[POSITION][X] + 1, 
                            self.current_img_data[POSITION][Y] + 1),
                LEFT_BOTTOM : (self.current_img_data[POSITION][X] + 1, 
                            self.current_img_data[POSITION][Y] + self.current_img_data[SIZE][Y] - 1),
                LEFT_CENTER : (self.current_img_data[POSITION][X] + 1, 
                            self.current_img_data[POSITION][Y] + self.current_img_data[SIZE][Y] / 2),
                RIGHT_TOP : (self.current_img_data[POSITION][X] + self.current_img_data[SIZE][X] - 1, 
                            self.current_img_data[POSITION][Y] + 1),
                RIGHT_BOTTOM : (self.current_img_data[POSITION][X] + self.current_img_data[SIZE][X] - 1,
                                self.current_img_data[POSITION][Y] + self.current_img_data[SIZE][Y] - 1),
                RIGHT_CENTER : (self.current_img_data[POSITION][X] + self.current_img_data[SIZE][X] - 1,
                                self.current_img_data[POSITION][Y] + self.current_img_data[SIZE][Y] / 2)
            }
            pyautogui.moveTo(AIM_TO[value])

    def macro_click(self, value : int):
        pyautogui.click(button=self.mouse_button[value])

    def macro_wait(self, value : float):
        pyautogui.sleep(float(value))

    def get_img_size(image : str) -> tuple:
        w, h = cv2.imread(image).shape[::-1][:2]
        return w, h

    def get_img_pos(self, image : str) -> tuple:
        if self.check_all_screens:
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

    def img_define(self, image : list) -> dict:
        cur_img = None
        w, h = None, None
        if type(image) != list:
            image = [image]
        for img in image:
            img_x, img_y, w, h = self.get_img_pos(os.path.join(os.path.normpath(self.path_to_command), os.path.normpath(img)))
            if img_x != None or img_y != None:
                cur_img = img
                break
        
        self.current_img_data[IMG] = cur_img
        self.current_img_data[POSITION] = (img_x, img_y)
        self.current_img_data[SIZE] = (w, h)

        # print(current_img_data)
        return self.current_img_data
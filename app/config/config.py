import yaml
from utils.decorators import exec_timer
import os
from config import BASE_DIR

# FOR DEVELOPMENT
# PATH_TO_CONFIG = os.path.join(BASE_DIR, "app", "config", "config.yaml")

# FOR BUILD
PATH_TO_CONFIG = os.path.join("data", "config.yaml")


class Config:
    @staticmethod
    @exec_timer
    def read_config() -> dict:
        with open(PATH_TO_CONFIG, 'r', encoding="utf-8") as file:
            yaml_conf =  yaml.safe_load(file)

        return yaml_conf
        
    @staticmethod
    @exec_timer
    def write_config(config : dict):
        if type(config) != dict:
            config = dict(config)
        with open(PATH_TO_CONFIG, 'w', encoding="utf-8") as file:
            yaml.dump(config, file)
import yaml
from utils.decorators import exec_timer
import os
from attrdict import AttrDict
from config import BASE_DIR

class Config:
    @staticmethod
    @exec_timer
    def read_config() -> AttrDict:
        with open(os.path.join(BASE_DIR, "app", "config", "config.yaml"), 'r', encoding="utf-8") as file:
            yaml_conf =  yaml.safe_load(file)

        return AttrDict(yaml_conf)
        
    @staticmethod
    @exec_timer
    def write_config(config : AttrDict):
        if type(config) == AttrDict:
            config = dict(config)
        with open(os.path.join(BASE_DIR, "app", "config", "config.yaml"), 'w', encoding="utf-8") as file:
            yaml.dump(config, file)
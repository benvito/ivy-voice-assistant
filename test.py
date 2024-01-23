# import subprocess

# subprocess.run(["data\\commands\\ahk\\Compiler\\Ahk2exe.exe", 
#                 "/in", 
#                 "data\\commands\\ahk\\mute_volume.ahk",
#                 "/out",
#                 "data\\commands\\ahk\\mute_volume.exe"], shell=True)

# subprocess.run(["data\\commands\\ahk\\mute_volume.exe", '0'], shell=True)


import os
import yaml
commands = dict()
print(os.path.join(".", "data", "commands"))
for dirName, subdirList, fileList in os.walk("./data/commands/"):
    if "commands.yaml" in fileList:
        commands.update(dict(yaml.safe_load(open(os.path.join(dirName, 'commands.yaml'), 'r', encoding='utf-8'))))


print(commands)
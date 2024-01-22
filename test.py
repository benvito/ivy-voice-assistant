import subprocess

subprocess.run(["data\\commands\\ahk\\Compiler\\Ahk2exe.exe", 
                "/in", 
                "data\\commands\\ahk\\mute_volume.ahk",
                "/out",
                "data\\commands\\ahk\\mute_volume.exe"], shell=True)

# subprocess.run(["data\\commands\\ahk\\mute_volume.exe", '0'], shell=True)
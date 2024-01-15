import yaml

commands = dict(yaml.safe_load(open('data/commands/commands.yaml', 'r', encoding='utf-8')))

print(list(commands.keys()).index('time'))
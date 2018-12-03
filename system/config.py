import json

with open('config.json') as config_file:
    config = json.loads(config_file.read())

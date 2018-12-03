import json

with open('config.json') as config_file:
    config = json.loads(config_file.read())


def set_config(key, value):
    global config

    config[key] = value
    with open('config.json', 'w') as config_file:
        config_file.write(json.dumps(config))
    return value


def get_config(key):
    return config[key]

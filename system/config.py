import json

with open('config.json') as config_file:
    config = json.loads(config_file.read())


def set_config(key, value):
    global config

    config[key] = value
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
        # config_file.write(json.dumps(config))
    return value


def get_config(key):
    try:
        return config[key]
    except IndexError:  # If for some reason it doesn't exist
        return None

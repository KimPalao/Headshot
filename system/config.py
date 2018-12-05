import json

try:
    with open('config.json') as config_file:
        config = json.loads(config_file.read())
except json.decoder.JSONDecodeError:
    # Restore the original version of the config
    config = {
        "enemy": 0,
        "control": 0,
        "damage": 100,
        "health": 100,
    }
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=2)


def set_config(key, value):
    global config

    config[key] = value
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=2)
        # config_file.write(json.dumps(config))
    return value


def get_config(key):
    try:
        return config[key]
    except IndexError:  # If for some reason it doesn't exist
        return None

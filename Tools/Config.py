import os
import logging
import shutil

def read_config_file():
    """
    Read the config file and return the config as a dictionary
    """
    config_file_path = os.path.expanduser('~/.config/Smartinput/config')
    config = {}
    try:
        with open(config_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=')
                    config[key.strip()] = value.strip().strip('"')
                    logging.info(f"Read config: {key}={value}")
    except FileNotFoundError:
        logging.error(f"Config file not found: {config_file_path}, copy the default config to {config_file_path}")
        lang = os.environ.get('LANG', 'en_US')
        os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
        shutil.copy("config", config_file_path)
        with open(config_file_path, 'a') as file:
            file.write(f"lang={lang}\n")
        logging.info(f"Default config file copied to: {config_file_path}")
        config = read_config_file()
    except Exception as e:
        logging.error(f"Failed to read config file: {config_file_path}, {e}")
        exit(1)
    return config

def change_one_config(key, value):
    """
    Change one config and write it to the config file, if the key is not found, add it to the end of the file
    """
    config_file_path = os.path.expanduser('~/.config/Smartinput/config')
    try:
        with open(config_file_path, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        logging.error(f"Failed to read config file: {config_file_path}, {e}")
        return False
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break
    if not found:
        lines.append(f"{key}={value}\n")
    try:
        with open(config_file_path, 'w') as file:
            file.writelines(lines)
    except Exception as e:
        logging.error(f"Failed to write config file: {config_file_path}, {e}")
        return False
    return True
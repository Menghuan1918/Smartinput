import os
import logging
import shutil

def read_config_file():
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

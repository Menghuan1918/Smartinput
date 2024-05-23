import os
import logging
import shutil

from Tools.DEFAULT import DEFAULT_General_Congig, DEFAULT_LLM_Congig, DEFAULT_Prompts


def get_default_config(filename):
    """
    Get the default config
    """
    if "General" in filename:
        return DEFAULT_General_Congig
    return ""


def read_config_file(filename):
    """
    Read the config file and return the config as a dictionary
    """
    config_file_path = os.path.expanduser(f"~/.config/Smartinput/{filename}")
    config = {}
    try:
        with open(config_file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=")
                    config[key.strip()] = value.strip().strip('"')
                    logging.info(f"Read config: {key}={value}")
    except FileNotFoundError:
        logging.error(
            f"Config file not found: {config_file_path}, copy the default config to {config_file_path}"
        )
        lang = os.environ.get("LANG", "en_US")
        if os.name == "nt":
            lang = os.environ.get("LC_ALL", "en_US")
        os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
        text = get_default_config(filename)
        text = text.replace("lang=en_US", f"lang={lang}")
        with open(config_file_path, "a") as file:
            file.write(f"lang={lang}\n")
        logging.info(f"Default config file copied to: {config_file_path}")
        config = read_config_file()
    except Exception as e:
        logging.error(f"Failed to read config file: {config_file_path}, {e}")
        exit(1)
    return config


def change_one_config(filename, key, value, explain="None"):
    """
    Change one config and write it to the config file, if the key is not found, add it to the end of the file
    """
    config_file_path = os.path.expanduser(f"~/.config/Smartinput/{filename}")
    try:
        with open(config_file_path, "r") as file:
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
        with open(config_file_path, "w") as file:
            file.writelines(lines)
    except Exception as e:
        logging.error(f"Failed to write config file: {config_file_path}, {e}")
        return False
    return True


def get_prompts():
    """
    Get the prompts from the prompts file in folder ~/.config/Smartinput/Prompts
    """
    prompts_folder = os.path.expanduser("~/.config/Smartinput/Prompts")
    prompts = {}
    try:
        for filename in os.listdir(prompts_folder):
            file_path = os.path.join(prompts_folder, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    content = file.read()
                    prompts[filename] = content
                    logging.info(f"Read prompts: {filename}")
    except FileNotFoundError:
        logging.error(
            f"Prompts folder not found: {prompts_folder}, create the folder and copy the default prompts"
        )
        os.makedirs(prompts_folder, exist_ok=True)
        for prompt_name, prompt_content in DEFAULT_Prompts.items():
            with open(os.path.join(prompts_folder, prompt_name), "w") as file:
                file.write(prompt_content)
        logging.info(f"Default prompts copied to: {prompts_folder}")
        prompts = get_prompts()

    except Exception as e:
        logging.error(f"Failed to read prompts folder: {prompts_folder}, {e}")
        exit(1)
    return prompts

"""
Парсер settings.yaml
Конфигурирует приложение
"""

import os
import re
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_FILE = Path.joinpath(PROJECT_ROOT, 'settings.yml')


def get_config(path=None, data=None, tag='!ENV'):
    pattern = re.compile('.*?\${(\w+)}.*?')
    loader = yaml.SafeLoader

    loader.add_implicit_resolver(tag, pattern, None)

    def constructor_env_variables(loader, node):
        value = loader.construct_scalar(node)
        match = pattern.findall(value)
        if match:
            full_value = value
            for g in match:
                full_value = full_value.replace(
                    f'${{{g}}}', os.environ.get(g, g)
                )
            return full_value
        return value

    loader.add_constructor(tag, constructor_env_variables)

    if path:
        with open(path) as conf_data:
            return yaml.load(conf_data, Loader=loader)
    elif data:
        return yaml.load(data, Loader=loader)
    else:
        raise ValueError('Either a path or data should be defined as input')


app_config = get_config(SETTINGS_FILE)

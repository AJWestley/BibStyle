import json
import re
import sys
import shutil
from typing import Literal
from pathlib import Path
from importlib.resources import files

COMPULSORY_FIELD = re.compile(r'^\w+(\|\w+)*$')

CONFIG_DIR = Path.home() / ".config" / "bibstyle"
USER_CONFIG = CONFIG_DIR / "config.json"
DEFAULT_CONFIG = files("bibstyle.data").joinpath("default_config.json")


def ensure_user_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not USER_CONFIG.exists():
        shutil.copy(DEFAULT_CONFIG, USER_CONFIG)


class Config:
    def __init__(self, path=USER_CONFIG):
        ensure_user_config()

        self.path = Path(path)

        with self.path.open("r") as conf_file:
            self.settings = json.load(conf_file)
    
    def get_valid_months(self):
        return self.settings['valid_months'][self.settings['month']]
    
    def set_month_preference(self, value: Literal['name', 'number']):
        if value not in ['name', 'number']:
            print(f'Invalid month preference: {value}')
            sys.exit(1)
        self.settings['month'] = value
        self.update()
    
    def get_compulsory_fields(self):
        return self.settings['compulsory_fields']
    
    def add_compulsory_field(self, entry_type: str, field: str):
        if entry_type not in self.settings['compulsory_fields']:
            print(f'Entry type {entry_type} does not exist')
            sys.exit(1)
        if not COMPULSORY_FIELD.fullmatch(field):
            print(f'Invalid field structure {field}')
            sys.exit(1)
        self.settings['compulsory_fields'][entry_type].append(field)
        self.update()
    
    def remove_compulsory_field(self, entry_type: str, field: str):
        if entry_type not in self.settings['compulsory_fields']:
            print(f'Entry type {entry_type} does not exist')
            sys.exit(1)
        if field not in self.settings['compulsory_fields'][entry_type]:
            print(f'Entry type {entry_type} does not contain field {field}')
            sys.exit(1)
        self.settings['compulsory_fields'][entry_type].remove(field)
        self.update()
    
    def add_entry_type(self, entry_type: str):
        if entry_type in self.settings['compulsory_fields']:
            print(f'Entry type {entry_type} already exists')
            sys.exit(1)
        self.settings['compulsory_fields'][entry_type] = []
        self.update()
    
    def clear_entry_type(self, entry_type: str):
        if entry_type not in self.settings['compulsory_fields']:
            print(f'Entry type {entry_type} does not exist')
            sys.exit(1)
        self.settings['compulsory_fields'][entry_type] = []
        self.update()
    
    def remove_entry_type(self, entry_type: str):
        if entry_type not in self.settings['compulsory_fields']:
            print(f'Entry type {entry_type} does not exist')
            sys.exit(1)
        self.settings['compulsory_fields'].pop(entry_type)
        self.update()
    
    def reset_to_default(self):
        """Reset the user config file back to the packaged default configuration."""
        shutil.copy(DEFAULT_CONFIG, self.path)
        with self.path.open("r") as conf_file:
            self.settings = json.load(conf_file)
    
    def print_settings(self):
        print(f"Month preference: {self.settings['month']}\n")
        for entry, fields in self.settings['compulsory_fields'].items():
            print(f"{entry}:")
            if len(fields) == 0:
                print("\tNo compulsory fields")
            for field in fields:
                print(f"\t- {field}")
    
    def update(self):
        with open(self.path, 'w') as conf_file:
            json.dump(self.settings, conf_file, indent=4)

preferences = Config()
valid_months = preferences.get_valid_months()
compulsory_fields = preferences.get_compulsory_fields()
import configparser
from pathlib import Path
import os

class FilterManager:
    def __init__(self, config_file='ignore_config.ini'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.ensure_config_file_exists()
        self.config.read(config_file)
        self.load_default_patterns()
        self.user_defined_patterns = set()
        self.user_defined_extensions = set()

    def ensure_config_file_exists(self):
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                f.write("[DEFAULT]\n")
                f.write("ignore_folders = .git,.vscode,__pycache__,node_modules\n")
                f.write("ignore_extensions = .pyc,.pyo,.pyd,.log,.tmp,.temp,.bak,.swp,.DS_Store\n")

    def load_default_patterns(self):
        self.default_folders = set(self.config.get('DEFAULT', 'ignore_folders', fallback='.git,.vscode,__pycache__,node_modules').split(','))
        self.default_extensions = set(self.config.get('DEFAULT', 'ignore_extensions', fallback='.pyc,.pyo,.pyd,.log,.tmp,.temp,.bak,.swp,.DS_Store').split(','))

    def add_user_pattern(self, pattern):
        self.user_defined_patterns.add(pattern)

    def add_user_extension(self, extension):
        if not extension.startswith('.'):
            extension = '.' + extension
        self.user_defined_extensions.add(extension)

    def should_ignore(self, path):
        path = Path(path)
        
        # Always ignore files named styles.ts
        if path.name == 'styles.ts':
            return True
        
        # Check if the path or any parent folder should be ignored
        for parent in [path] + list(path.parents):
            if parent.name in self.default_folders or parent.name in self.user_defined_patterns or str(parent) in self.user_defined_patterns:
                return True
        
        # Check file extension
        if path.suffix in self.default_extensions or path.suffix in self.user_defined_extensions:
            return True
        
        # Check user-defined patterns
        if str(path) in self.user_defined_patterns:
            return True
        
        return False

    def get_ignored_items(self):
        return {
            "default_folders": self.default_folders,
            "default_extensions": self.default_extensions,
            "user_defined_patterns": self.user_defined_patterns,
            "user_defined_extensions": self.user_defined_extensions
        }
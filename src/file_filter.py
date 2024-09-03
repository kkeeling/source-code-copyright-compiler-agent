import os
import logging

class FileFilter:
    def __init__(self, ignored_extensions=None, ignored_directories=None):
        """
        Initialize the FileFilter with lists of extensions and directories to ignore.

        Args:
            ignored_extensions (list): List of file extensions to ignore (without the dot).
            ignored_directories (list): List of directory names to ignore.
        """
        default_ignored_extensions = ['html', 'md', 'txt', 'pdf', 'pyc']
        default_ignored_directories = ['node_modules', 'venv', 'env', '.git']

        self.ignored_extensions = set(default_ignored_extensions + (ignored_extensions or []))
        self.ignored_directories = set(default_ignored_directories + (ignored_directories or []))
        self.always_ignored_files = {'.DS_Store', '.gitignore'}

        logging.info(f"Initializing FileFilter with ignored extensions: {self.ignored_extensions}")
        logging.info(f"Initializing FileFilter with ignored directories: {self.ignored_directories}")
        logging.info(f"Always ignored files: {self.always_ignored_files}")

    def should_process_file(self, file_path):
        """
        Determine if a file should be processed based on its extension and name.

        Args:
            file_path (str): The path of the file to check.

        Returns:
            bool: True if the file should be processed, False otherwise.
        """
        file_name = os.path.basename(file_path)

        if file_name in self.always_ignored_files:
            logging.info(f"Skipping always ignored file: {file_path}")
            return False

        for ext in self.ignored_extensions:
            if file_name.endswith(f'.{ext}'):
                logging.info(f"Skipping file due to ignored extension: {file_path}")
                return False

        return True

    def should_process_directory(self, dir_path):
        """
        Determine if a directory should be processed.

        Args:
            dir_path (str): The path of the directory to check.

        Returns:
            bool: True if the directory should be processed, False otherwise.
        """
        dir_name = os.path.basename(dir_path)
        should_process = dir_name not in self.ignored_directories
        if not should_process:
            logging.info(f"Skipping directory: {dir_path}")
        return should_process

    def set_ignored_extensions(self, ignored_extensions):
        """
        Set a new list of ignored extensions.

        Args:
            ignored_extensions (list): List of file extensions to ignore (without the dot).
        """
        self.ignored_extensions = set(ignored_extensions)
        logging.info(f"Updated ignored extensions: {self.ignored_extensions}")

    def set_ignored_directories(self, ignored_directories):
        """
        Set a new list of ignored directories.

        Args:
            ignored_directories (list): List of directory names to ignore.
        """
        self.ignored_directories = set(ignored_directories)
        logging.info(f"Updated ignored directories: {self.ignored_directories}")

    def add_always_ignored_file(self, file_name):
        """
        Add a file name to the list of always ignored files.

        Args:
            file_name (str): Name of the file to always ignore.
        """
        self.always_ignored_files.add(file_name)
        logging.info(f"Added {file_name} to always ignored files: {self.always_ignored_files}")
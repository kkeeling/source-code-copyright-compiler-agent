import os
from collections import deque
import logging
from filter_manager import FilterManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProjectAnalyzer:
    def __init__(self, root_path, filter_manager=None):
        """
        Initialize the ProjectAnalyzer with the root path of the project and an optional FilterManager.

        Args:
            root_path (str): The root path of the project to analyze.
            filter_manager (FilterManager): An instance of FilterManager to use for filtering files and directories.
        """
        self.root_path = root_path
        self.project_structure = {}
        self.files_list = []
        self.filter_manager = filter_manager or FilterManager()

    def analyze(self):
        """
        Analyze the project structure using breadth-first search, applying file and directory filtering.
        """
        queue = deque([(self.root_path, self.project_structure)])

        while queue:
            current_path, current_dict = queue.popleft()
            
            for item in os.listdir(current_path):
                item_path = os.path.join(current_path, item)
                
                if os.path.isdir(item_path):
                    if not self.filter_manager.should_ignore(item_path):
                        logging.info(f"Discovered directory: {item_path}")
                        current_dict[item] = {}
                        queue.append((item_path, current_dict[item]))
                    else:
                        logging.info(f"Filtered out directory: {item_path}")
                        current_dict[item] = "FILTERED_DIR"
                elif not self.filter_manager.should_ignore(item_path):
                    logging.info(f"Discovered file: {item_path}")
                    current_dict[item] = None
                    self.files_list.append(item_path)
                else:
                    logging.info(f"Filtered out file: {item_path}")
                    current_dict[item] = "FILTERED_FILE"

        logging.info("Project analysis completed.")

    def get_project_structure(self):
        """
        Get the project structure as a dictionary.

        Returns:
            dict: The project structure.
        """
        return self.project_structure

    def get_files_list(self):
        """
        Get the list of files in breadth-first order.

        Returns:
            list: List of file paths in breadth-first order.
        """
        return self.files_list

    def print_structure(self):
        """
        Print the project structure.
        """
        print("Project structure:")
        self._print_structure(self.project_structure)

    def _print_structure(self, structure, level=0):
        """
        Recursively print the project structure.

        Args:
            structure (dict): The structure to print.
            level (int): The current indentation level.
        """
        for key, value in structure.items():
            if value == "FILTERED_FILE":
                print("  " * level + f"- {key} (FILTERED FILE)")
            elif value == "FILTERED_DIR":
                print("  " * level + f"- {key}/ (FILTERED DIRECTORY)")
            else:
                print("  " * level + f"- {key}")
                if isinstance(value, dict):
                    self._print_structure(value, level + 1)

if __name__ == "__main__":
    # Example usage
    filter_manager = FilterManager()
    filter_manager.add_user_pattern('*.html')
    filter_manager.add_user_pattern('*.md')
    filter_manager.add_user_pattern('node_modules')
    analyzer = ProjectAnalyzer("/path/to/your/project", filter_manager)
    analyzer.analyze()
    analyzer.print_structure()
    print("\nFiles list:")
    print(analyzer.get_files_list())

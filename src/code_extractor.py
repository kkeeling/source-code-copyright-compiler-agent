import logging
import re

class CodeExtractor:
    def __init__(self, max_lines=200):
        self.max_lines = max_lines
        logging.info(f"Initializing CodeExtractor with max_lines: {self.max_lines}")

    def extract_code(self, file_path):
        """
        Extract code from a file, excluding import statements, export statements, console.log statements, comments, and stylesheet code.

        Args:
            file_path (str): The path to the file to extract code from.

        Returns:
            str: The extracted code snippet.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                filtered_content = self.filter_content(content)
                lines = filtered_content.split('\n')
                extracted_lines = lines[:self.max_lines]
                snippet = '\n'.join(extracted_lines)
                logging.info(f"Extracted {len(extracted_lines)} lines from {file_path}")
                return snippet
        except Exception as e:
            logging.error(f"Error extracting code from {file_path}: {str(e)}")
            return f"Error: Unable to extract code from {file_path}"

    def filter_content(self, content):
        """
        Filter out import statements, export statements, console.log statements, comments, and stylesheet code.

        Args:
            content (str): The content of the file.

        Returns:
            str: Filtered content.
        """
        # Remove multi-line comments
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        
        # Remove single-line comments
        content = re.sub(r'//.*', '', content)
        
        # Remove import statements
        content = re.sub(r'^\s*(import|from)\s+.*$', '', content, flags=re.MULTILINE)
        
        # Remove export statements
        content = re.sub(r'^\s*export\s+.*$', '', content, flags=re.MULTILINE)
        
        # Remove console.log statements
        content = re.sub(r'^\s*console\.log\(.*\);?$', '', content, flags=re.MULTILINE)
        
        # Remove stylesheet code
        content = re.sub(r'const\s+styles\s*=\s*StyleSheet\.create\s*\({[\s\S]*?\}\);?', '', content)
        
        # Remove empty lines
        content = re.sub(r'^\s*$\n', '', content, flags=re.MULTILINE)
        
        return content.strip()

    def set_max_lines(self, max_lines):
        """
        Set the maximum number of lines to extract.

        Args:
            max_lines (int): The maximum number of lines to extract.
        """
        self.max_lines = max_lines
        logging.info(f"Updated max_lines to: {self.max_lines}")
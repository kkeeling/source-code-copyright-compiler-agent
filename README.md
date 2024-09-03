# Source Code Copyright Compiler

The Source Code Copyright Compiler is a command-line tool that generates an MS Word document containing the source code of a project for copyright submission purposes. It analyzes the project structure using a breadth-first search algorithm, extracts code snippets, and creates a well-formatted document.

## Features

- Analyzes project structure using breadth-first search
- Filters out specified files and directories
- Extracts code snippets from source files
- Generates an MS Word document with formatted code snippets
- Provides real-time progress updates

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/source-code-copyright-compiler.git
   cd source-code-copyright-compiler
   ```

2. Ensure conda is initialized:
   If you haven't already initialized conda in your shell, run the following command:
   ```
   conda init
   ```
   After running this command, close and reopen your terminal or run `source ~/.bashrc` (or the appropriate file for your shell) to apply the changes.

3. Create and activate the conda environment:
   ```
   conda create -n source-code-copyright-compiler python=3.11 -y
   conda activate source-code-copyright-compiler
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the tool from the command line, providing the path to your project's root folder:

```
python src/main.py /path/to/your/project [options]
```

### Command-line options:

- `--ignore-folder FOLDER [FOLDER ...]`: Additional folders to ignore (can be used multiple times)
- `--ignore-extension EXT [EXT ...]`: Additional file extensions to ignore (can be used multiple times)
- `--ignore-file FILE [FILE ...]`: Specific files to ignore (can be used multiple times)
- `--output FILENAME`: Output document filename (default: copyright_submission.docx)

Example:
```
python src/main.py /path/to/your/project --ignore-folder node_modules .git --ignore-extension .log .tmp --ignore-file config.ini .env --output my_project_copyright.docx
```

You can also use multiple `--ignore-folder`, `--ignore-extension`, and `--ignore-file` arguments:

```
python src/main.py /path/to/your/project --ignore-folder node_modules --ignore-folder .git --ignore-extension .log --ignore-extension .tmp --ignore-file config.ini --ignore-file .env --output my_project_copyright.docx
```

**Note:** Be careful with typos in the command-line options. For example, `--ignore-extenstion` (missing 'i') is a common typo. The tool will try to suggest corrections for misspelled arguments.

The tool will analyze the project structure, extract code snippets, and generate an MS Word document in the specified location or the current directory.

## Output

The generated MS Word document will contain:

1. A project structure overview
2. Code snippets from each file (first and last 10 "pages" of code)

## Development

This project is currently under development. The initial setup includes the project structure, project analyzer, file filtering, code extraction, and document generation.

To contribute or extend the functionality, please refer to the user stories and tasks outlined in the project documentation.

## License

[MIT License](LICENSE)
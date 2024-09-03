import argparse
import os
import logging
import sys
from difflib import get_close_matches
from project_analyzer import ProjectAnalyzer
from filter_manager import FilterManager
from code_extractor import CodeExtractor
from document_generator import DocumentGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def suggest_correction(arg):
    """Suggest a correction for a misspelled argument."""
    valid_args = ['--ignore-folder', '--ignore-extension', '--ignore-file', '--output']
    closest = get_close_matches(arg, valid_args, n=1, cutoff=0.6)
    return closest[0] if closest else None

def sort_files_by_folder(file_paths):
    """Sort file paths alphabetically within folders."""
    sorted_paths = sorted(file_paths, key=lambda x: (os.path.dirname(x), os.path.basename(x)))
    return sorted_paths

def main():
    parser = argparse.ArgumentParser(description="Source Code Copyright Compiler")
    parser.add_argument("project_path", help="Path to the root folder of the project")
    parser.add_argument("--ignore-folder", nargs='+', action='append', help="Additional folders to ignore")
    parser.add_argument("--ignore-extension", nargs='+', action='append', help="Additional file extensions to ignore")
    parser.add_argument("--ignore-file", nargs='+', action='append', help="Specific files to ignore")
    parser.add_argument("--output", default="copyright_submission.docx", help="Output document filename")

    # Custom argument parsing to catch and suggest corrections for typos
    args = []
    skip_next = False
    for i, arg in enumerate(sys.argv[1:]):
        if skip_next:
            skip_next = False
            continue
        if arg.startswith('--'):
            if arg not in parser._option_string_actions:
                suggestion = suggest_correction(arg)
                if suggestion:
                    print(f"Warning: '{arg}' is not a valid argument. Did you mean '{suggestion}'?")
                    arg = suggestion
            args.append(arg)
            if i + 1 < len(sys.argv[1:]) and not sys.argv[i+2].startswith('--'):
                args.append(sys.argv[i+2])
                skip_next = True
        else:
            args.append(arg)

    args = parser.parse_args(args)

    project_root = os.path.abspath(args.project_path)
    if not os.path.isdir(project_root):
        logging.error(f"Error: '{project_root}' is not a valid directory.")
        return

    # Initialize FilterManager with user-defined patterns
    filter_manager = FilterManager()
    if args.ignore_folder:
        for folders in args.ignore_folder:
            for folder in folders:
                filter_manager.add_user_pattern(folder)
                # Also add the full path to ensure it's ignored
                filter_manager.add_user_pattern(os.path.join(project_root, folder))
    if args.ignore_extension:
        for extensions in args.ignore_extension:
            for ext in extensions:
                filter_manager.add_user_extension(ext)
    if args.ignore_file:
        for files in args.ignore_file:
            for file in files:
                filter_manager.add_user_pattern(file)
                # Also add the full path to ensure it's ignored
                filter_manager.add_user_pattern(os.path.join(project_root, file))

    ignored_items = filter_manager.get_ignored_items()
    logging.info(f"Using filter with ignored folders: {ignored_items['default_folders']}")
    logging.info(f"Using filter with ignored extensions: {ignored_items['default_extensions']}")
    logging.info(f"Using filter with user-defined patterns: {ignored_items['user_defined_patterns']}")
    logging.info(f"Using filter with user-defined extensions: {ignored_items['user_defined_extensions']}")

    logging.info(f"Analyzing project at: {project_root}")
    analyzer = ProjectAnalyzer(project_root, filter_manager)
    analyzer.analyze()

    logging.info("Extracting code snippets")
    extractor = CodeExtractor()
    code_snippets = {}
    for file_path in analyzer.get_files_list():
        code_snippets[file_path] = extractor.extract_code(file_path)

    logging.info("Generating copyright submission document")
    project_name = os.path.basename(project_root)
    doc_gen = DocumentGenerator(project_name, project_root)

    logging.info("Adding code snippets to the document in alphabetical order within folders")
    sorted_file_paths = sort_files_by_folder(code_snippets.keys())
    for file_path in sorted_file_paths:
        doc_gen.add_code_snippet(file_path, code_snippets[file_path])

    output_path = os.path.join(os.path.dirname(project_root), args.output)
    doc_gen.save_document(output_path)

    logging.info(f"Copyright submission document generated: {output_path}")

if __name__ == "__main__":
    main()
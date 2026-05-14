import sys
from pathlib import Path
import bibtexparser

def load_lines(path):
    '''Loads the lines from a bibtex file'''
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def load_bib(path):
    '''Loads the entry dictionary from a bibtex file'''
    try:
        with open(path, "r", encoding="utf-8") as f:
            parser = bibtexparser.bparser.BibTexParser()
            parser.ignore_nonstandard_types = False
            return bibtexparser.load(f, parser).entries
    except Exception as e:
        print(f"[FATAL] BibTeX parse error:\n{e}")
        sys.exit(1)

def print_issues(issue_list):
    '''Outputs the issue list'''
    for i in issue_list:
        print(" -", i)
    sys.exit(0)

def check_file_exists(path):
    '''Checks the given file exists'''
    if not Path(path).is_file():
        print(f'No file found at {path}')
        sys.exit(1)
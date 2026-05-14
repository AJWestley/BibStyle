import sys
from bibstyle.rules import entry
from bibstyle.rules import line
from bibstyle.io import load_lines, load_bib, print_issues, check_file_exists
from bibstyle.checker import run_checks
from bibstyle.config import preferences

def settings(args):
    if len(args) == 3:
        if args[1] =='show' and args[2] == 'config':
            preferences.print_settings()
            return True
        if args[1] == 'month' and args[2] in ['name', 'number']:
            preferences.set_month_preference(args[2])
            return True
    
    if len(args) == 4:
        if args[1] == 'entry':
            if args[2] == 'add':
                preferences.add_entry_type(args[3])
            elif args[2] == 'remove':
                preferences.remove_entry_type(args[3])
            elif args[2] == 'clear':
                preferences.clear_entry_type(args[3])
            else:
                return False
            return True
    
    if len(args) == 5:
        if args[1] == 'field':
            if args[2] == 'add':
                preferences.add_compulsory_field(args[3], args[4])
            elif args[2] == 'remove':
                preferences.remove_compulsory_field(args[3], args[4])
            else:
                return False
            return True
    
    return False

def run(path):
    check_file_exists(path)

    lines = load_lines(path)
    issues = run_checks(lines, 'line')

    if len(issues) > 0:
        print_issues(issues)

    entries = load_bib(path)
    issues = run_checks(entries, 'entry')

    if issues:
        print_issues(issues)
    else:
        print("No issues found.")

def main():
    if len(sys.argv) == 2:
        run(sys.argv[1])
        sys.exit(0)
    
    if settings(sys.argv):
        sys.exit(0)
    
    print("Usage: ")
    print("\tbibstyle file.bib")
    print("\tbibstyle month 'name|number'")
    print("\tbibstyle entry add|remove|clear entry_name")
    print("\tbibstyle field add|remove entry_name 'option1|option2|...'")
    print("\tbibstyle show config")
    sys.exit(1)
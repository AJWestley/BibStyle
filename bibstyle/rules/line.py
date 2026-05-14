import re
from bibstyle.checker import line_check
from bibstyle.config import valid_months

EQUAL_BAD = re.compile(r"[^ ]=[^ ]|[^ ] =[^ ]|=[^ ]")
FIELD_LINE = re.compile(r'^\s*(\w+)\s*=\s*(.+?),?\s*$')
MONTH = re.compile(r"\s*month\s=\s\{(.*)\}\s*,")


@line_check
def check_blank_lines(lines):
    '''Checks that each entry is separated by a blank line'''
    issues = []
    for i, line in enumerate(lines):
        if line.strip().startswith("@"):
            if i > 0 and lines[i - 1].strip() != "":
                issues.append(error_msg(i, "entry not preceded by blank line"))
    return issues

@line_check
def check_equal_spacing(lines):
    '''Checks that each field = has a single space on either side'''
    issues = []
    for i, line in enumerate(lines):
        if "=" in line and not line.strip().startswith("%"):
            if EQUAL_BAD.search(line):
                issues.append(error_msg(i, f"bad '=' spacing -> {line.strip()}"))
    return issues

@line_check
def check_braced_fields(lines):
    '''Checks that all fields are correctly braced'''
    issues = []
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith('%') or stripped.startswith('@'):
            continue
        match = FIELD_LINE.match(stripped)
        if not match:
            continue
        field, value = match.groups()
        value = value.strip()
        if value.endswith(","):
            value = value[:-1].strip()
        if not value:
            continue
        is_braced = value.startswith("{") and value.endswith("}")
        is_quoted = value.startswith('"') and value.endswith('"')
        if is_quoted:
            issues.append(error_msg(i-1, f"{field} uses quotes instead of braces -> {value}"))
        elif not is_braced:
            issues.append(error_msg(i-1, f"{field} not wrapped in braces -> {value}"))
    return issues

@line_check
def check_months(lines):
    '''Checks that the months are correctly formatted'''
    issues = []
    for i, line in enumerate(lines):
        if MONTH.search(line):
            month = MONTH.findall(line)[0]
            if month not in valid_months:
                issues.append(error_msg(i, f"invalid month -> {month}"))
    return issues

def error_msg(line, msg):
    return f"Line {line+1}: {msg}"
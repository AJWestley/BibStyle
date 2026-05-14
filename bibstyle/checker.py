from typing import Literal, Callable

CHECKS = {
    'line': [],
    'entry': []
}

def line_check(func: Callable):
    '''Decorator for line checks'''
    CHECKS['line'].append(func)
    return func

def entry_check(func: Callable):
    '''Decorator for entry checks'''
    CHECKS['entry'].append(func)
    return func

def run_checks(data: dict | list, check_type: Literal['line', 'entry']):
    '''Runs the checks corresponding to a particular decorator'''
    issues = []
    if check_type not in CHECKS:
        raise ValueError(f'Invalid check_type: {check_type}')
    checks = CHECKS[check_type]
    for check in checks:
        issues.extend(check(data))
    return issues
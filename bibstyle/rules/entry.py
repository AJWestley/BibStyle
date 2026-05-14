import re
from collections import defaultdict
from bibstyle.checker import entry_check
from bibstyle.config import compulsory_fields

ORDINAL = re.compile(r"^\d*(?:(?<!1)1st|(?<!1)2nd|(?<!1)3rd|(?<!1[123])\dth|1[123]th)$")
ENTRY_KEY_BAD_CHARS = re.compile(r"[^a-zA-Z0-9:_\-]")
JOURNAL_CMD = re.compile(r"\\[a-zA-Z]+")
PAGE = re.compile(r"^[A-Za-z]?\d+[A-Za-z]?$|^[A-Za-z]+\d+$|^\d+$")
DOI = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.I)


@entry_check
def check_entry_keys(entries):
    '''Checks the entry key is correctly formatted'''
    issues = []
    for e in entries:
        key = e.get("ID", "")
        if ENTRY_KEY_BAD_CHARS.search(key):
            issues.append(error_msg(e, f"invalid characters in key -> {key}"))
        if "." in key:
            issues.append(error_msg(e, f"dots not allowed in key -> {key}"))
    return issues

@entry_check
def check_entry_types(entries):
    issues = []
    for e in entries:
        e_type = e.get("ENTRYTYPE", "").lower()
        if e_type == 'all' or e_type not in compulsory_fields:
            issues.append(error_msg(e, f"invalid entry type -> {e_type}"))
    return issues

@entry_check
def check_fields_present(entries):
    '''Checks the minimum necessary fields are present in each entry'''
    issues = []
    for e in entries:
        e_type = e.get("ENTRYTYPE", "").lower()
        for field in compulsory_fields['all'] + compulsory_fields.get(e_type, []):
            if not field_present(e, field):
                issues.append(error_msg(e, f"missing field -> {field.replace("|", " or ")}"))
    return issues

@entry_check
def check_journal_field(entries):
    '''Checks that the journal entry doesn't use a Latex command'''
    issues = []
    for e in entries:
        if e.get("ENTRYTYPE", "").lower() == "article":
            journal = e.get("journal", "")
            if JOURNAL_CMD.search(journal):
                issues.append(error_msg(e,  f"journal uses LaTeX command -> {journal}"))
    return issues

@entry_check
def check_author(entries):
    '''Checks author formatting'''
    issues = []
    for e in entries:
        author = e.get("author", "")
        if not author:
            continue
        if "  " in author:
            issues.append(error_msg(e, "author has double spaces"))
    return issues

@entry_check
def check_editions(entries):
    '''Checks that the edition is an ordinal'''
    issues = []
    for e in entries:
        edition = e.get('edition', '')
        if edition and not is_ordinal(edition):
            issues.append(error_msg(e, f"invalid edition -> {edition}"))
    return issues

@entry_check
def check_year(entries):
    '''Checks the year format'''
    issues = []
    for e in entries:
        year = e.get("year", "")
        if not year:
            continue
        if not re.fullmatch(r"\d{4}", str(year)):
            issues.append(error_msg(e, f"invalid year -> {year}"))
    return issues

@entry_check
def check_pages(entries):
    '''Checks the pages format'''
    issues = []
    for e in entries:
        pages = e.get("pages", "")
        if not pages:
            continue
        pages = pages.strip()
        if "--" in pages:
            start, end = map(str.strip, pages.split("--", 1))
            if not PAGE.match(start) or not PAGE.match(end):
                issues.append(f"{e.get('ID')}: invalid pages range -> {pages}")
            continue
        if not PAGE.match(pages):
            issues.append(f"{e.get('ID')}: invalid pages -> {pages}")
    return issues

@entry_check
def check_doi(entries):
    '''Checks the DOI structure'''
    issues = []
    for e in entries:
        doi = e.get("doi", "")
        if doi and not DOI.match(doi):
            issues.append(error_msg(e, f"invalid DOI -> {doi}"))
    return issues

@entry_check
def check_urls(entries):
    '''Checks the URL structure'''
    issues = []
    for e in entries:
        url = e.get("url", "")
        if url and not url.startswith(("http://", "https://")):
            issues.append(error_msg(e, f"bad URL -> {url}"))
    return issues

@entry_check
def check_duplicate_keys(entries):
    '''Checks for duplicate keys'''
    issues = []
    seen = defaultdict(list)
    for e in entries:
        key = e.get("ID")
        if key:
            seen[key].append(e)
    for k, v in seen.items():
        if len(v) > 1:
            issues.append(f"duplicate key -> {k}")
    return issues

def field_present(entry, field_description):
    '''Used for parsing the compulsory fields'''
    for subfield in field_description.split("|"):
        if entry.get(subfield, ""):
            break
    else:
        return False
    return True

def is_ordinal(string):
    return ORDINAL.search(string)

def error_msg(entry, msg):
    return f"{entry.get('ID')}: {msg}"
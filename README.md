# BibStyle

My personal Bibtex style checker.

## Installation

**NB: BibStyle has only been tested on Ubuntu**

After cloning this repo, the following can be run from the base directory:

```bash
$ pip install .
```

## Usage

### Style-Checking a File

You can style-check a bibtex file using the following command:
```bash
$ bibstyle your_bibfile.bib
```

### Viewing and Editing Preferences

There are some minor customisation options available:
- Whether months should be names (January, February, March, etc.) or numbers (1, 2, 3, etc.).
- Which fields should be present in each entry type, at minimum.


To view or reset the current settings, you can run
```bash
$ bibstyle config show
# or
$ bibstyle config reset
```


The month preference can be changed with
```bash
$ bibstyle month name
# or
$ bibstyle month number
```


Below are a few commands to add entry types and fields:
```bash
$ bibstyle entry add|remove|clear entry_name # adds|removes|clears an entry type
$ bibstyle bibstyle field add|remove entry_name 'option1|option2|...' # adds a compulsory field ("|" is used to specify one of the options must be present)
```
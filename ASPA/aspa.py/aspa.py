#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The main file for ASPA - static abstract syntax tree analyser."""
__version__ = "0.2.2" # 21.06.2021
__author__ = "RL"


try:
    import tkinter as tk  # Python 3, tested with this
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import font
except ModuleNotFoundError as e:
    print(e)
    import sys
    print("Unable to import tkinter module. If you are using Linux system"
          " try to install tkinter with command:\n"
          "sudo apt-get install python3-tk\n"
          "\nUnless you are using Fedora try this:\n"
          "sudo dnf install python3-tkinter\n"
          "\nIf these didn't fix the problem or you are using Windows or macOS,"
          " please contact course's teaching staff.")
    sys.exit(0)

import ast
import json
import datetime # for timestamp
import os       # os.walk is used for convenient directory exclusion possibility
import pathlib  # Used for all the other path operations
import re
from typing import Iterable
from typing import List


########################################################################
# config.py
#
########################################################################
"""Configuration file containing predefined constants."""

DEFAULT_SETTINGS = {
    "root": str(pathlib.Path(__file__).parents[0].resolve()),
    "language": "FIN",
    "default_paths": [],
    "title_font_size": 12,
    "normal_font_size": 10
}

# -----------------------------------------------------------------------------#
# Constants which are not meant to be changed

# NOTE \w inlcudes alfanumeric characters and underscore
# This is used to exclude elements like class.function or imported.function or
# function.function from analysis dictionaries.
_GLOBAL_ELEM = r"^[\w]+$"

# -----------------------------------------------------------------------------#
# Analysis constants
MAIN_FUNC_NAME = "paaohjelma"

# Allowed naming schema for variables, in Regex
VALID_NAME_SCHEMA = r"^[a-zA-Z_][a-zA-Z0-9_]*$"

# Add names of special functions which are allowed/denied inside class.
# Use * to match any function names. Allowed overrides denied.
ALLOWED_FUNCTIONS = {"__init__"}
DENIED_FUNCTIONS = {"*"}

# Add function names which are allowed to miss return command.
MISSING_RETURN_ALLOWED = {"__init__"}

# Examples of commands which could be searched in check PT1.
SEARCHED_COMMANDS = {"round", "print", "range", "int", "len", "float", "str"}

# Allowed constants values for return values (but not NameConstants True, False, None).
ALLOWED_CONSTANTS = {}

# Add keys of ignored structure messages (work with single or multiple regex patterns)
IGNORE_STRUCT = {}

# Add keys of ignored error messages
# IGNORE = {"PT1", "MR5"}
IGNORE = {"PT1", "MR5", "AR6-2"}
# IGNORE = {"PT1", "PK1", "MR5", "AR6-1", "AR6-2"}
GENERAL = 0
ERROR = 1
WARNING = 2
NOTE = 3
GOOD = 4
DEBUG = 5

# Element orders are tuples with following format:
# (allowed ast types, required names, denied names, element id)
ELEMENT_ORDER = (# Header comment should be first
                 (ast.Expr, ("Docstring", ), tuple(), "E0"),
                 ((ast.Import, ast.ImportFrom), tuple(), tuple(), "E1"),
                 (ast.Assign, tuple(), tuple(), "E3"),
                 (ast.ClassDef, tuple(), tuple(), "E2"),
                 ((ast.AsyncFunctionDef, ast.FunctionDef), tuple(), (MAIN_FUNC_NAME,), "E4"),
                 (ast.FunctionDef, (MAIN_FUNC_NAME,), tuple(), "E5"),
                 (ast.Expr, (MAIN_FUNC_NAME,), tuple(), "E6")
                )

ALLOWED_ELEMENTS = {ast.Import, ast.ImportFrom, ast.Assign, ast.ClassDef,
                    ast.AsyncFunctionDef, ast.FunctionDef, ast.Expr}

# ELEMENT_TEXT = {
#     "ENG": {
#         "E0": "Docstring",
#         "E1": "Imports",
#         "E2": "Class definitions",
#         "E3": "Constants",
#         "E4": "Function definitions",
#         "E5": f"Definition of {MAIN_FUNC_NAME}",
#         "E6": f"{MAIN_FUNC_NAME}() call"
#     },
#     "FIN": {
#         "E0": "Dokumentaatiorivi (docstring)",
#         "E1": "Sisällytykset",
#         "E2": "Luokkien määrittelyt",
#         "E3": "Kiintoarvot",
#         "E4": "Aliohjelmien määrittelyt",
#         "E5": f"{MAIN_FUNC_NAME}-määrittely",
#         "E6": f"{MAIN_FUNC_NAME}-kutsu"
#     }
# }

# --- AST class type sets ---
FUNC = (ast.FunctionDef, ast.AsyncFunctionDef)
CLS_FUNC = (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
LOOP = (ast.For, ast.While)
YIELD = (ast.Yield, ast.YieldFrom)


# --- Formatting configurations tuples ---
FILENAME_OPTIONS = ("name", "filename")  # Strings which mean (show) filename in settings.
FILEPATH_OPTIONS = ("path", "filepath")  # Strings which mean (show) filepath in settings.
OPTIONS_FOR_ALL = ("both", "all", "everything", "*")  # Strings which mean everthing/all/both.

# -----------------------------------------------------------------------------#
# Analysis category names
CHECKBOX_OPTIONS = [
    "basic",
    "function",
    "file_handling",
    "data_structure",
    "library",
    "exception_handling"
]

TEXT = {
    "FIN": {
        "basic": "Perustoiminnot",
        "function": "Aliohjelmat",
        "file_handling": "Tiedostonkäsittely",
        "data_structure": "Tietorakenteet",
        "library": "Kirjaston käyttö",
        "exception_handling": "Poikkeustenkäsittely",
        "file_error": "Tiedostovirhe", # File error e.g. SyntaxError
        "ASPA_error": "Analysointi virhe"  # Analysing error in ASPA
    },
    "ENG": {
        "basic": "Basic commands",
        "function": "Functions",
        "file_handling": "File handling",
        "data_structure": "Data structures",
        "library": "Library usage",
        "exception_handling": "Exception handling",
        "file_error": "File Error", # File error e.g. SyntaxError
        "ASPA_error": "Analysis error" # Analysing error in ASPA
    }
}

# -----------------------------------------------------------------------------#
# GUI constants
GUI = {
    "FIN": {
        "exit": "Sulje",
        "filemenu": "Toiminnot",
        "results": "Näytä tulokset",
        "BKTA": "Tee BKT-analyysi",
        "help": "Käyttöohje",
        "helpmenu": "Ohjeet",
        "select_analysis_title": "Valitse tarkistukset",
        "preset_title": "Esivalinnat",
        "clear": "Tyhjennä",
        "exam_level": "Tentti taso",
        "course_project_short": "HT",
        "filepaths": "Tiedostopolut",
        "select_file": "Valitse tiedosto",
        "select_folder": "Valitse kansio",
        "all_files": "Kaikki tiedostot",
        "execute_analysis": "Suorita analyysi",
        "analysis_result": "Analyysin tulokset",
        "back": "Takaisin",
        "settings": "Asetukset",
        "not_ready_note": "Työn alla"
    },
    "ENG": {
        "exit": "Exit",
        "filemenu": "File",
        "results": "Show results",
        "BKTA": "Execute BKT analysis",
        "help": "User guide",
        "helpmenu": "Help",
        "select_analysis_title": "Select analyses",
        "preset_title": "Presets",
        "clear": "Clear",
        "exam_level": " Exam level",
        "course_project_short": "CP",
        "filepaths": " Filepaths",
        "select_file": "Select file",
        "select_folder": "Select folder",
        "all_files": "All files",
        "execute_analysis": "Execute analysis",
        "analysis_result": "Analysis results",
        "back": "Back",
        "settings": "Settings",
        "not_ready_note": "Under construction"
    }
}


TOOL_NAME = "ASPA - Abstrakti SyntaksiPuu Analysaattori"
TOOL_NAME_SHORT = "ASPA"
BG_COLOR = None #"#bababa" #None # "#383838"
FRAME_COLOR = None #"#ffcfcf"
PAD = 5
LARGE_FONT = "None 12 bold"
NORMAL_FONT = "None 10"
SMALL_FONT = "None 8"
FONT_COLOR = "black"
BD_STYLE = "ridge" #tk.RIDGE # Border style
BD = 2              # Border width

HIGHLIGHT = {
    GOOD: "#00aa00", #""green",
    NOTE: "#0000ff", # "blue",
    WARNING: "#ff7700", #"orange",
    ERROR: "#dd0000" #"red"
}

# THERE ARE ALSO predefined fonts like these
    # TkDefaultFont The default for all GUI items not otherwise specified.
    # TkTextFont    Used for entry widgets, listboxes, etc.
    # TkFixedFont   A standard fixed-width font.
    # TkMenuFont    The font used for menu items.
    # TkHeadingFont A font for column headings in lists and tables.
    # TkCaptionFont A font for window and dialog caption bars.
    # TkSmallCaptionFont    A smaller caption font for subwindows or tool dialogs.
    # TkIconFont    A font for icon captions.
    # TkTooltipFont A font for tooltips.

# Example guide texts
EXAMPLES = {
    "EX0": "Liite 5",
    "EX1": "Tiedon tulostaminen ruudulle",
    "EX2": "Tiedon lukeminen käyttäjältä",
    "EX3": "Valintarakenne",
    "EX4": "Toistorakenteet",
    "EX5": "Aliohjelmat",
    "EX6": "Tiedostoon kirjoittaminen",
    "EX7": "Tiedostosta lukeminen",
    "EX8": "Listan käsittely",
    "EX9": "Monimutkaisempi tietorakenne",
    "EX10": "Poikkeukset",
    "EX11": "Luku 8 asiat kokoava esimerkki",
    "EX12": "Liite 3: Tulkin virheilmoitusten tulkinta"
}

TITLE_TO_EXAMPLES = {
    "basic": ("EX0", "EX1","EX2","EX3","EX4",),
    "function": ("EX0", "EX5",),
    "file_handling": ("EX0", "EX6","EX7",),
    "data_structure": ("EX0", "EX5", "EX8","EX9",),
    "library": ("EX11",),
    "exception_handling": ("EX0", "EX10",),
    "file_error": ("EX12",)
}

# -----------------------------------------------------------------------------#
# Violation messages
MSG = {
    "ENG": {
        "default": ("Error occured!", ERROR),
        "error_error": ("Error while printing an error message. "
                        + "Probably too few *args.", DEBUG), # Debug
        "type_error": ("Abstract Syntax Tree parameter has wrong type, e.g. None.", DEBUG), # Debug
        "syntax_error": ("File has a syntax error.", ERROR),
        "tool_error": (f"{TOOL_NAME_SHORT} error while analysing the file '{{}}'.", ERROR),
        "PT1": ("Command '{}' is used.", NOTE),
        "PT2": ("Name '{}' contains other than A-Z, 0-9 and underscore characters.", WARNING),
        # "PT2-1": ("Name '{}' is Python keyword.", WARNING), # using keyword actually creates syntax error to ast.parse
        "PT4-1": ("Loop never breaks.", ERROR),
        "PT5": ("Unreachable code after command '{}'.", ERROR),
        "AR1": (f"No function defition for '{MAIN_FUNC_NAME}'.", NOTE),
        "AR2-1": ("Definition of the function '{}' is not in the global scope.", ERROR),
        "AR3": ("Global variable '{}'.", ERROR),
        # "AR3-2": ("Variable or object is used in global scope '{}.{}'.", ERROR), # Works only with objects
        "AR4": ("Recursive function call.", NOTE),
        "AR5-1": ("Function '{}' requires at least {} parameters, but {} given.", ERROR),
        "AR5-2": ("Function '{}' requires at most {} parameters, but {} given.", ERROR),
        "AR5-3": ("In call of function '{}', '{}' is invalid keyword argument.", ERROR),
        "AR6": ("Missing return at the end of the function '{}'.", WARNING),
        "AR6-1": ("Usage of '{}' in function '{}'.", NOTE), # Yield and yield from detection
        "AR6-2": ("Return statement at the middle of the function.", NOTE),
        "AR6-3": ("Missing value from the return-statement.", WARNING),
        "AR6-4": ("Return value is a constant.", NOTE),
        "AR6-5": ("Returning multiple values at once.", NOTE),
        "AR6-6": ("Returning something else than a variable or constant.", NOTE),
        "AR7": ("Assigning an attribute to the function '{}'.", ERROR),
        # "AR8": ("<Statement which should not be in global scope.>", WARNING),
        # "MR1": ("Element '{}' should be before '{}'.", WARNING),
        "MR1": ("Statement seem to be in wrong location.", WARNING),
        "MR2-3": ("Function call '{}()' is {} function call in the global scope."
                + f" There should be only one (1) function call '{MAIN_FUNC_NAME}()'.",
                WARNING),
        "MR2-4": ("Function call '{}()' in the global scope does not call the"
                + "main function.", WARNING),
        "MR3": ("Module '{}' is imported again.", ERROR),
        "MR3-1": ("From module '{}' function(s) or module(s) are imported again.", WARNING),
        "MR4": ("Import of the module '{}' is not in the global scope.", ERROR),
        "MR5": ("Missing some or all header comments at {} first lines of the file.", WARNING),
        "PK1": ("Exception handling has no excepts.", ERROR),
        "PK1-1": ("Missing exception type.", WARNING),
        "PK3": ("Missing exception handling from the file opening.", ERROR),
        "PK4": ("Missing exception handling from the file operation '{}'.", ERROR),
        # "PK4b": ("Missing exception handling from the file operation '{}'.", ERROR),
        "TK1": ("File handle '{}' is left open.", ERROR),
        "TK1-1": ("In this course usage of '{}' is not recommended.", NOTE),
        "TK1-2": ("File handle '{}' is closed in except branch.", WARNING),
        "TK1-3": ("Missing parenthesis from file closing '{}.{}'.", ERROR),
        "TK2": ("File operation '{}.{}' is in different function than file open and close.", ERROR),
        "TR2-1": ("Class is used directly without an object '{}'.", ERROR),
        "TR2-2": ("Missing parenthesis from object creation. Should be '{}()'.", ERROR),
        "TR2-3": ("Class '{}' is not defined in the global scope.", ERROR),
        "TR2-4": ("Name of the class '{}' is not in UPPERCASE.", NOTE),
        # "TR3": ("Object created.", NOTE),
        "TR3-1": ("Object's attribute value is added to a list in every loop iteration.", WARNING),
        "TR3-2": ("Object is created outside a loop but usage and addition to"
                + " a list is inside the loop.", WARNING),
        "OK": (": No violations detected.", GOOD),
        "NOTE": (", violations detected please see", GENERAL),
        "LINE": ("Line", GENERAL),
        "WELCOME": ("In prints **-marking stands for warning, and ++ for note, "
                 + "all others are errors.", GENERAL),
        "NOTE_INFO": ("All messages with this colour are notes.", NOTE),
        "WARNING_INFO": ("All messages with this colour are warnings.", WARNING),
        "ERROR_INFO": ("All messages with this colour are errors.", ERROR),
    },
    "FIN": {
        "default": ("Tapahtui virhe!", ERROR),
        "error_error": ("Virhe tulostettaessa virhettä. Luultavasti "
                      + "liian vähän argumentteja (*args).", DEBUG), # Debug
        "type_error": ("Syntaksipuun parametri on väärää tyyppiä, esim. None.", DEBUG), # Debug
        "syntax_error": ("Tiedostossa on syntaksi virhe.", ERROR),
        "tool_error": (f"{TOOL_NAME_SHORT}:n virhe analysoitaessa tiedostoa '{{}}'.", ERROR),
        "PT1": ("Komentoa '{}' on käytetty.", NOTE),
        "PT2": ("Nimessä '{}' on muita kuin A-Z, 0-9 ja alaviiva merkkejä.", WARNING),
        # "PT2-1": ("Nimi '{}' on Pythonin avainsana.", WARNING), # using keyword actually creates syntax error to ast.parse
        "PT4-1": ("Silmukkaa ei koskaan pysäytetä.", ERROR),
        "PT5": ("Koodirivejä komennon '{}' jälkeen.", ERROR),
        "AR1": (f"Ohjelmasta ei löytynyt määrittelyä '{MAIN_FUNC_NAME}':lle.", NOTE),
        "AR2-1": ("Aliohjelman '{}' määrittely ei ole päätasolla.", ERROR),
        "AR3": ("Globaalimuuttuja '{}'.", ERROR),
        # "AR3-2": ("Muuttujan tai olion globaali käyttö '{}.{}'.", ERROR),
        "AR4": ("Rekursiivinen aliohjelmakutsu.", NOTE),
        "AR5-1": ("Aliohjelma '{}' vaatii vähintään {} kpl parametreja, mutta {} lähetetty.", ERROR),
        "AR5-2": ("Aliohjelma '{}' vaatii enintään {} kpl parametreja, mutta {} lähetetty.", ERROR),
        "AR5-3": ("Aliohjelmakutsussa '{}', '{}' on virheellinen parametrin nimi.", ERROR), # Using word parametri here, not argumentti
        "AR6": ("Aliohjelman '{}' lopusta puuttuu return-komento.", WARNING),
        "AR6-1": ("Käytetään generaattoria '{}' aliohjelmassa '{}'.", NOTE), # Yield and yield from detection
        "AR6-2": ("Keskellä aliohjelmaa on return.", NOTE),
        "AR6-3": ("return-komennosta puuttuu paluuarvo.", WARNING),
        "AR6-4": ("Paluuarvo on vakio.", NOTE),
        "AR6-5": ("Palautetaan useita paluuarvoja.", NOTE),
        "AR6-6": ("Palautetaan jotain muuta kuin muuttujia tai avainsana.", NOTE),
        "AR7": ("Aliohjelmalle määritetään attribuuttia '{}'.", ERROR),
        # "AR8": ("<Komento, jonka ei tulisi olla päätasolla.>", WARNING),
        # "MR1": ("Komennon '{}' pitäisi olla ennen '{}'.", WARNING),
        "MR1": ("Komento vaikuttaisi olevan väärässä kohdin tiedostoa.", WARNING),
        "MR2-3": ("Aliohjelmakutsu '{}()' on {}. aliohjelmakutsu. Pitäisi olla vain "
                + f"yksi (1) aliohjelmakutsu '{MAIN_FUNC_NAME}()'.", WARNING),
        "MR2-4": ("Päätason aliohjelmakutsu '{}()' ei viittaa tiedoston pääohjelmaan.", WARNING),
        "MR3": ("Kirjasto '{}' sisällytetään (eng. import) uudelleen.", ERROR),
        "MR3-1": ("Kirjastosta '{}' sisällytetään sisältöä uudelleen.", WARNING),
        "MR4": ("Kirjaston '{}' sisällytys (eng. import) ei ole päätasolla.", ERROR),
        "MR5": ("Tiedostossa ei ole kaikkia alkukommentteja tiedoston {}"
                + " ensimmäisellä rivillä.", WARNING),
        "PK1": ("Poikkeustenkäsittelyssä ei ole lainkaan exceptiä.", ERROR),
        "PK1-1": ("Exceptistä puuttuu virhetyyppi.", WARNING),
        "PK3": ("Tiedoston avaamisesta puuttuu poikkeustenkäsittely.", ERROR),
        "PK4": ("Tiedosto-operaatiosta '{}' puuttuu poikkeustenkäsittely.", ERROR),
        # "PK4b": ("Tiedosto-operaatiosta '{}' puuttuu poikkeustenkäsittely.", ERROR),
        "TK1": ("Tiedostokahva '{}' on sulkematta.", ERROR),
        "TK1-1": ("Tällä kurssilla '{}':n käyttö ei ole suositeltu rakenne.", NOTE),
        "TK1-2": ("Tiedostokahva '{}' suljetaan except-osiossa.", WARNING),
        "TK1-3": ("Tiedoston sulkukomenosta '{}.{}' puuttuvat sulut.", ERROR),
        "TK2": ("Tiedosto-operaatio '{}.{}' eri aliohjelmassa kuin avaus ja sulkeminen.", ERROR),
        "TR2-1": ("Luokan käyttö suoraan ilman oliota '{}'.", ERROR),
        "TR2-2": ("Olion luonnista puuttuvat sulkeet. Pitäisi olla '{}()'.", ERROR),
        "TR2-3": ("Luokkaa '{}' ei ole määritelty päätasolla.", ERROR),
        "TR2-4": ("Luokan '{}' nimi ei ole kirjoitettu SUURAAKKOSIN.", NOTE),
        # "TR3": ("Olion luonti.", NOTE),
        "TR3-1": ("Olion attribuutin arvo lisätään listaan silmukan sisällä.", WARNING),
        "TR3-2": ("Olion luonti silmukan ulkopuolella, mutta arvojen päivitys"
                + " ja listaan lisääminen silmukassa.", WARNING),
        "NOTE": (", tyylirikkeitä havaittu, ole hyvä ja katso", GENERAL),
        "OK": (": Ei tunnistettu tyylirikkomuksia.", GOOD),
        "LINE": ("Rivi", GENERAL),
        "WELCOME": ("Tulosteissa **-merkintä tarkoittaa varoitusta ja ++-merkintä ilmoitusta, "
                 + "muut ovat virheitä.", GENERAL),
        "NOTE_INFO": ("Tällä värillä merkityt viestit ovat huomioita.", NOTE),
        "WARNING_INFO": ("Tällä värillä merkityt viestit ovat varoituksia.", WARNING),
        "ERROR_INFO": ("Tällä värillä merkityt viestit ovat virheitä.", ERROR),
    }
}

# -----------------------------------------------------------------------------#
# CLI error messages
CLI_ERROR = {
    "ENG": {
        "NO_FILES": "Please select files to be analysed.",
        "NO_SELECTIONS": "Please select analysis to be executed.",
        "NO_LANGUAGE": "Please define language in settings. By default FIN is used." # Technically this will never occur if FIN is default
    },
    "FIN": {
        "NO_FILES": "Ole hyvä ja valitse ensin analysoitavat tiedostot.",
        "NO_SELECTIONS": "Ole hyvä ja valitse ensin suoritettavat analyysit.",
        "NO_LANGUAGE": "Ole hyvä ja määrittele käytettävä kieli asetuksista. Oletusasetus on FIN."
    }
}

SETTINGS_CONFLICTS = {
    "ENG": {
        "C0001": "Decimal and cell separators can't be the same character." +
                 " Default values comma (,) and semicolon (;) are used" +
                 " for decimal separator and cell separator, respectively."

    },
    "FIN": {
        "C0001": "Desimaali- ja soluerottimet eivät voi olla sama merkki." +
                 " Käytetään oletusarvoja pilkku (,) desimaalierottimena ja" +
                 " puolipiste (;) soluerottimena."
    }
}

########################################################################
# templates.py
#
########################################################################
"""
File for any template class used in ASPA. Templates are used to store
multivalue information about stored elements, i.e. they are often struc
like objects.
"""

 # TODO Move ViolationTemplate somewhere else because it is not a Template
 # anymore but rather a real class. Same time utils are not needed anymore.

class NodeTemplate():
    """General template class for any ast node."""

    def __init__(self, name, lineno, astree):
        self._name = name
        self._astree = astree # AST of the node
        self._lineno = lineno

    @property
    def name(self):
        return self._name

    @property
    def astree(self):
        return self._astree

    @property
    def lineno(self):
        return self._lineno

class FunctionTemplate(NodeTemplate):
    """Template class for functions found during preanalysis."""

    def __init__(self, name, lineno, astree, pos_args, kw_args, imported=False):
        NodeTemplate.__init__(self, name, lineno, astree)
        self._pos_args = pos_args    # Positional arguments before *args
        self._kw_args = kw_args      # Keyword arguments before **kwargs
        self._imported = imported
        self.recursive_calls = []

    @property
    def pos_args(self):
        return self._pos_args

    @property
    def kw_args(self):
        return self._kw_args

    @property
    def imported(self):
        return self._imported

    def add_recursive_call(self, node):
        self.recursive_calls.append(node)

    def get_recursive_calls(self):
        return self.recursive_calls

class ImportTemplate(NodeTemplate):
    """Template class for imports found during preanalysis."""

    def __init__(self, name, lineno, astree, import_from=False):
        NodeTemplate.__init__(self, name, lineno, astree)
        self._import_from = import_from

    @property
    def import_from(self):
        return self._import_from

class ClassTemplate(NodeTemplate):
    """Template class for classes found during preanalysis."""

    def __init__(self, name, lineno, astree, imported=False):
        NodeTemplate.__init__(self, name, lineno, astree)
        self._imported = imported

    @property
    def imported(self):
        return self._imported

class GlobalTemplate(NodeTemplate):
    """Template class for global variables found during preanalysis."""

    def __init__(self, name, lineno, astree):
        NodeTemplate.__init__(self, name, lineno, astree)


class CallTemplate(NodeTemplate):
    """
    Template class for (function or class) calls found during
    preanalysis.
    """

    def __init__(self, name, lineno, astree):
        NodeTemplate.__init__(self, name, lineno, astree)


class ObjectTemplate(NodeTemplate):
    """Template class for objects used in data structure analysis."""

    def __init__(self, name, lineno, astree):
        NodeTemplate.__init__(self, name, lineno, astree)


class ViolationTemplate():
    """Template class for violations found during any analysis."""

    def __init__(self, vid, args, lineno, status):

        self._vid = vid          # Violation identifier
        # self.vtype = vtype      # Violation type
        self._args = args
        self._lineno = lineno
        self._status = status    # Violation status True/False
        self._msg_tuple = None
        self._lang = None

    @property
    def vid(self):
        return self._vid

    @property
    def args(self):
        return self._args

    @property
    def status(self):
        return self._status

    @property
    def lineno(self):
        return self._lineno

    def get_msg(self, lang):
        """
        Return a violation message as a string. Violation message
        is currently constructed in utils lib.
        """

        if self._msg_tuple is None or lang != self._lang:
            self._lang = lang
            self._msg_tuple = create_msg(
                self._vid,
                *self._args,
                lineno=self._lineno,
                lang=self._lang
            )

        return self._msg_tuple


class FilepathTemplate():
    """Template class for filepaths found during directory crawling."""

    def __init__(self, path, student=None, week=None, exercise=None, course=None):
        self._path = path # Pathlib object
        self._filename = path.name
        self._student = student
        self._exercise = exercise
        self._week = week
        self._course = course

    @property
    def path(self):
        return self._path

    @property
    def filename(self):
        return self._filename

    @property
    def student(self):
        return self._student

    @property
    def exercise(self):
        return self._exercise

    @property
    def week(self):
        return self._week

    @property
    def course(self):
        return self._course


class FilehandleTemplate(NodeTemplate):
    """Template class for filehandles found during file analysis."""

    def __init__(self, name, lineno, astree, closed=0):
        NodeTemplate.__init__(self, name, lineno, astree)
        self._closed = closed

    @property
    def closed(self):
        return self._closed

    @property
    def opened(self):
        return self._lineno

    @property
    def filehandle(self):
        return self._name

    def set_closed(self, closing_line):
        # If _closed is != 0 it is already closed. The first closing is
        # interesting and therefore only that is stored.
        if self._closed == 0:
            self._closed = closing_line

########################################################################
# utils_lib.py
#
########################################################################
"""Module containing utility functions general use."""

# MSG = cnf.MSG
# STRUCTURE = cnf.STRUCTURE
# EXAMPLES = cnf.EXAMPLES
# TITLE_TO_EXAMPLES = cnf.TITLE_TO_EXAMPLES
# TEXT = cnf.TEXT

# IGNORE = cnf.IGNORE
# GENERAL = cnf.GENERAL
# ERROR = cnf.ERROR
# WARNING = cnf.WARNING
# NOTE = cnf.NOTE
# GOOD = cnf.GOOD
# DEBUG = cnf.DEBUG

########################################################################
# Regex
REGEX = {}  # This will store compiled regex patterns
PATTERN = { # This include all configurated patterns as a string
    "valid_naming": VALID_NAME_SCHEMA,
    "_global_element": _GLOBAL_ELEM
}

########################################################################
# General utilities

def ignore_check(code):
    """
    Function to test if check will be ignored. Test is based on
    violation ID.

    Return:
     - True if check will be ignored.
     - False if check won't be ignored.
    """

    if code in IGNORE:
        return True
    return False


def get_all_ignored_checks():
    """
    Getter function for set which included ID's of all ignored checks.
    """

    return IGNORE


def create_msg(code, *args, lineno=-1, lang="FIN"):
    """
    Function to create violation message based on given violation code,
    message parameters (e.g. variable name), linenumber and language.

    Return:
    1. msg - violation message - string
    2. severity - severity level of message - integer number
        (numbers are predefined global constants)
    3. start - character index of violation message's start position
        - integer number
    4. end - character index of violation message's end position
        - integer number
    """

    msg = ""
    start = 0
    end = 0
    severity = MSG[lang]["default"][1]
    # if lineno < 0:
    #     pass
    if lineno >= 0 and lang:
        msg = f"{MSG[lang]['LINE'][0]} {lineno}: "
        start = len(msg)

    try:
        msg += MSG[lang][code][0]
        severity = MSG[lang][code][1]
    except KeyError:
        msg += MSG[lang]["default"][0]
    else:
        try:
            msg = msg.format(*args)
        except IndexError:
            msg = MSG[lang]["error_error"][0]
    finally:
        end = len(msg)

    return msg, severity, start, end


def get_title(title_key, lang):
    """
    Return: title of if ast analyser based on title_key (analyser ID)
    and lang (language). If there is KeyError return None.
    """

    try:
        return TEXT[lang][title_key]
    except KeyError:
        return None


def create_title(code, title_key, lang="FIN"):
    """
    Function to create title string message based on given title code,
    title_key and language.

    Arguments:
    1. code - ID of title - str
    2. title_key - ID of ast analyser - str
    3. lang - language of title, default is FIN - str

    Return:
    1. msg - title - string
    2. severity - severity level of title - integer number
        (numbers are predefined global constants)
    3. start - character index of title's start position - integer
       number
    4. end - character index of title's end position - integer number
    """

    title = get_title(title_key, lang)
    msg = ""
    start = 0
    end = 0
    severity = GENERAL
    if title:
        msg = title
        start = len(msg) + 1

    try:
        if title_key != "analysis_error":
            msg += MSG[lang][code][0]
            severity = MSG[lang][code][1]

            if code == "NOTE":
                exs = TITLE_TO_EXAMPLES[title_key]
                for i in exs:
                    if i == "EX0":
                        msg += f" {EXAMPLES[i]}"
                    else:
                        msg += f" '{EXAMPLES[i]}'"
                msg += ":"
    except KeyError:
        pass

    finally:
        end = len(msg)

    return msg, severity, start, end


def directory_crawler(
    paths,
    excluded_dirs=(),
    excluded_files=(),
    only_leaf_files=True,
    output_format="list"
):
    """
    Function to crawl all (sub)directories and return filepaths based on
    given rules.

    Arguments:
    1. paths is list of crawled filepaths. Paths should be in string
       format.
    2. excluded_dirs is iterable of (sub)directories which are excluded
       from the crawling.
    3. excluded_files is iterable of files which are excluded from the
       crawling result.
    4. only_leaf_files if True/False. If True include only files from
       directories which do not have subdirectories, after excluded_dirs
       are excluded.
    5. output_format defines format in which filepaths are returned.
       Supported formats are currently dictionary and list. List is
       default.

    Return: Filepaths in format speficied in output_format argument.
    """

    def remove_excluded(dirs, excluded):
        for e in excluded:
            try:
                dirs.remove(e)
            except ValueError:
                pass

    def add_file(file_struct, filepath):
        # TODO add settings which allow user to define corresponding numberings
        # and how many there are and in which order.
        student = 0
        exercise = 1
        week = 2 # exam
        # course = 3

        student_str = filepath.parents[student].name
        week_str = filepath.parents[week].name
        exercise_str = filepath.parents[exercise].name

        file_struct.setdefault(student_str, []).append(
            FilepathTemplate(
                path=filepath,
                student=student_str,
                week=week_str,
                exercise=exercise_str
            )
        )


    # List which will include every filepath as pathlib.Path object
    file_list = []

    for path_str in paths:
        path_obj = pathlib.Path(path_str).resolve()

        if path_obj.is_dir():
            # for sub in path_obj.glob("**/*.py"): # NOTE glob itself does not
            # allow selecting only leaf files, therefore os.path.walk is used.
            for current_dir, dirs, all_files in os.walk(path_obj, topdown=True):
                remove_excluded(dirs, excluded_dirs)

                if not all_files or (only_leaf_files and dirs):
                    continue

                for f in all_files:
                    if f.endswith(".py") and not f in excluded_files:
                        file_list.append(pathlib.Path(current_dir).joinpath(f))

        elif (path_obj.is_file()
                and path_obj.suffix == ".py"
                and not path_str in excluded_files):
            file_list.append(path_obj)

    # Transform file_list into requested file structure.
    if output_format == "list":
        file_structure = []

        for path_obj in file_list:
            file_structure.append(FilepathTemplate(path=path_obj))

    elif output_format == "dict":
        file_structure = {}

        for path_obj in file_list:
            add_file(file_structure, path_obj)

    # Else there is invalid output_format then empty list is returned.
    else:
        file_structure = []

    file_list.clear()

    return file_structure


def read_file(filepath, encoding="UTF-8", settings_file=False):
    """
    Function to read given filepath. If encoding is given use it
    otherwise expect UTF-8 encoding.

    Return: Read content as string.
    """

    content = None
    try:
        with open(filepath, "r", encoding=encoding) as f_handle:
            content = f_handle.read() # Add pass / fail metadata extraction
    except OSError:
        if not settings_file:
            print("OSError while reading a file", filepath)
    except Exception:
        pass
    return content


def write_file(filepath, content, mode="w", encoding="UTF-8", repeat=True):
    """
    Function to write given content to given filepath. If filepath has
    subdirectories which do not exists, these subdirectories are created
    and single recursive call is created to try again.

    Return: None
    """

    try:
        try:
            with open(filepath, mode=mode, encoding=encoding) as f_handle:
                f_handle.write(content)

        except FileNotFoundError: # When subdirectory is not found
                path = pathlib.Path(filepath)
                path.parent.absolute().mkdir(parents=True, exist_ok=True)
                if repeat:
                    # This call is first level recursion
                    write_file(
                        filepath,
                        content,
                        mode=mode,
                        encoding=encoding,
                        repeat=False # To prevent infinite repeat loop
                    )

    except OSError:
        print("OSError while writing a file", filepath)
    except Exception:
        print("Other error than OSError with file", filepath)
    return None


def print_title(title):
    print(f"--- {title} ---")


def create_dash(character="-", dash_count=80, get_dash=False):
    """
    Creates a "line" which is given character repeated dash_count times.

    Return: If get_dash is True, return created "line of dashes"
            else prints it and return None.
    """

    if get_dash:
        return character * dash_count
    else:
        print(character * dash_count)


########################################################################
# Getter functions for static values

def get_compiled_regex(key):
    """
    Function to get compiled regex pattern. On the first call pattern
    will be compiled in concecutive calls same compiled pattern will be
    returned.
    """

    # NOTE this will raise a KeyError if key is not found from the
    # PATTERN but that should be possible only in development phase when
    # patterns are added to config file and to the PATTERN dictionary.
    # PATTERN is not configurable by an end user.
    return REGEX.setdefault(key, re.compile(PATTERN[key]))

########################################################################
# Init functions

def add_fixed_settings(settings):
    """
    Function to add fixed settings which are not modifieable by user and
    derived settings e.g. result paths which are concatenated result
    directory path and filename.

    Return: None
    """

    # Checkbox options
    settings["checkbox_options"] = CHECKBOX_OPTIONS

    # Defaults
    settings["dump_tree"] = False
    settings["console_print"] = False
    settings["file_write"] = True
    settings["GUI_print"] = True
    settings["only_leaf_files"] = False
    settings["result_dir"] = settings["root"]
    settings["result_file"] = "tarkistukset.txt"
    settings["excluded_directories"] = ["__pycache__", ".git"]
    settings["excluded_files"] = ["__init__.py"]
    settings["clear_filepaths"] = False
    settings["shown_filepath_format"] = "both" # Options are defined in "Formatting configurations tuples"
    settings["BKT_decimal_separator"] = ","
    settings["BKT_cell_separator"] = ";"

    # Result file paths
    result_dir = pathlib.Path(settings["result_dir"])
    settings["result_path"] = result_dir.joinpath(settings["result_file"])




    return None


def init_settings() -> dict:
    """
    Function to initialise settings dictionary. Settings are based on
    default settings which are then updated by values from asetukset.json
    file. If there is no settings file, new asetukset.json file is
    created.

    Return: settings dictionary.
    """

    settings = DEFAULT_SETTINGS # Currently reference not copy
    settings_path = pathlib.Path(
        settings["root"] + "/" + "asetukset.json"
    )

    content = read_file(settings_path, settings_file=True)
    if content:
        for key, value in json.loads(content).items():
            settings[key] = value
    else:
        content = json.dumps(settings, indent=4)
        write_file(settings_path, content, mode="w")
    add_fixed_settings(settings)

    return settings


def detect_settings_conflicts(settings: dict) -> List[str]:
    """
    Function to check throught predefined set of possible conflict cases
    in settings.

    Arguments:
    1. settings - Settings dictionary, key is setting name and value is
       setting value - dict

    Return: conflicts - list of conflict message IDs (str) - List[str]
    """

    # Initialise
    conflicts = []

    # Check defined conflict cases
    if settings.get("BKT_decimal_separator") == settings.get("BKT_cell_separator"):
        conflicts.append("C0001")

    return conflicts


def solve_settings_conflicts(conflicts: List[str], settings: dict) -> None:
    """
    Function to solve detected settings conflicts.

    Arguments:
    1. conflicts - List of conflict message keys as string - List[str]
    2. settings - Settings dictionary, key is setting name and value is
       setting value - dict

    Return: None
    """

    for key in conflicts:
        if key == "C0001":
            settings["BKT_decimal_separator"] = ","
            settings["BKT_cell_separator"] = ";"

    return None


########################################################################
# analysis_utils.py
#
########################################################################
"""Library containing utility functions for static analysers."""

# AST improvement utilities
def add_parents(tree):
    """Function to add parent_node attribute to each node in AST."""

    for node in ast.walk(tree):
        for child_node in ast.iter_child_nodes(node):
            child_node.parent_node = node


def add_siblings(tree):
    """
    Function to add previous_sibling and next_sibling attributes to each
    node in AST, which are inside iterable body of parent node. For
    nodes which are inside these iterable bodies, if no there is no
    previous or next sibling the respective value will be None.

    NOTE 1:
    Useful iterable bodies are body, orelse, handlers and finalbody,
    however, also type_ignores, decorator_list, argument lists (e.g.
    args and kw_defaults) will get sibling attributes.

    NOTE 2:
    In addition global-keyword creates Global node which has str typed
    elements and this creates attribute error when trying to assign
    values to next_sibling and previous_sibling attrbutes.
    """

    for node in ast.walk(tree):
        for field in ast.iter_fields(node): # Yield a tuple of (fieldname, value)

            # There could be check that name of the field is either
            # body, orelse, handlers or finalbody
            # but not in 'names' used in Global node.
            if(isinstance(field[1], (list, tuple))):
                previous_sibling = last = None
                for child_node in field[1]:
                    try:
                        if(previous_sibling):
                            previous_sibling.next_sibling = child_node

                        child_node.previous_sibling = previous_sibling
                        previous_sibling = last = child_node

                    # This error may occur e.g. when
                    #   'str' object has no attribute 'previous_sibling'
                    # which is case e.g. with global-keyword creating node
                    #   Global(names=['with_global_keyword']),
                    except AttributeError:
                        pass
                if(last):
                    last.next_sibling = None

    # # Print siblings
    # for node in ast.walk(tree):
    #     try:
    #         pl = nl = ""
    #         if(node.previous_sibling):
    #             pl = node.previous_sibling.lineno

    #         if(node.next_sibling):
    #             nl = node.next_sibling.lineno

    #         print(f"{node.lineno:4}: {node}, PREV {pl}: {node.previous_sibling}, NEXT {nl}: {node.next_sibling}")
    #     except AttributeError:
    #         print("---", node)

# AST search utilities
def get_parent(node, allowed, denied=tuple()):
    """
    Function to get parent instance of a node.
    'allowed' argument defines type of the desired parent, it should be
    any of the ast node types and can be tuple. Optional argument '
    denied' defines not allowed parents as ast node types.

    If allowed type is found, returns found node, if denied type is
    found first or neither of them is found returns None.
    """

    temp = node
    parent = None
    while(hasattr(temp, "parent_node") and not isinstance(temp, denied)):
        temp = temp.parent_node
        if isinstance(temp, allowed):
            parent = temp
            break
    return parent


def get_outer_parent(node, allowed, **kwargs):
    """
    Function to get outermost parent instance with allowed type. Uses
    get_parent function until denied is found or no more allowed type is
    found.

    Return:
    IF parent is found: outer_parent - ast Node - Outermost parent node
                        of a reguested type.
    ELSE: node - the parameter node itself.
    """

    outer_parent = node
    while (temp := get_parent(outer_parent, allowed, **kwargs)):
        outer_parent = temp
    return outer_parent


def has_same_parent(node, others, allowed, **kwargs): #denied=tuple()):
    # NOT YET TESTED
    parent = get_parent(node, allowed, **kwargs)
    if isinstance(others, (list, tuple, set)):
        for i in others:
            if not parent or (parent != get_parent(i, allowed, **kwargs)):
                return False
    elif not parent or (parent != get_parent(others, allowed, **kwargs)):
        return False
    return True


def get_child_instance(node, allowed, denied=tuple()):
    """
    Function to get child instance of a node.
    'allowed' argument defines type of the desired child, it should be
    any of the ast node types and can be tuple. Optional argument '
    denied' defines not allowed children as ast node types.

    If allowed type is found, returns found node, if denied type is
    found first or neither of them is found returns None.
    """

    child = None
    for child_node in ast.walk(node):
        if(isinstance(child_node, allowed)):
            child = child_node
            break
        elif(isinstance(child_node, denied)):
            break
    return child

# AST tests and value gets
def is_always_true(test):
    """
    Function to define cases where conditional test is always true.
    'test' should be ast.Compare type or ast.Constant. Returns truth
    value.
    TODO: Add more always true cases.
    """

    is_true = False
    try:
        if(isinstance(test, ast.Constant) and test.value == True):
            is_true = True
    except AttributeError:
        pass
    return is_true


def is_added_to_data_structure(node, data_stuct_node, data_stuct_name, add_attrs):
    """
    Helper function to detect if node is added to a datastucture.
    So far tested and commented only with ast.List.
    """

    is_added = False
    parent = get_parent(node, (data_stuct_node, ast.Call))

    # This detect list_name += [...] and list_name = list_name + [...]
    # and cases with extend where list_name.extend([...])
    if(isinstance(parent, data_stuct_node)):
        is_added = True

    # This detect list_name.append() and list_name.insert()
    # and in some cases list_name.extend()
    elif(isinstance(parent, ast.Call)
            and isinstance(parent.func, (ast.Attribute))
            and parent.func.attr in add_attrs):
        is_added = True

    #  This detect all cases inside list(...)-call
    elif(isinstance(parent, ast.Call) and parent.func.id == data_stuct_name):
        is_added = True

    return is_added


def get_attribute_name(node, splitted=False, omit_n_last=0):
    """
    Function to parse name from attributes. If the is only single Name
    node then node.id is enough. Otherwise add all attrs in front of
    the id.

    Optional parameters:
    1. "splitted" is used get result as list instead of joined string,
        i.e. "[like, this]" instead of "like.this".
    2. "omit_n_last" is used to leave n last attrs out.
    """

    try:
        name = node.id
    except AttributeError:
        # If omit_n_last != 0 then it is changed to negative
        # otherwise it will be None
        # This is used in substring [:-n] where [:None] is same as [:]
        omit_n_last = -omit_n_last or None

        try:
            name_parts = []
            temp = node
            while hasattr(temp, "attr"):
                name_parts.insert(0, temp.attr)
                temp = temp.value

            name = [temp.id] + name_parts[:omit_n_last]
            if not splitted:
                name = ".".join(name)

        except AttributeError:
            raise
        finally:
            name_parts.clear()
    return name


def get_class_name(node, **kwargs):
    """
    Function to get name of a class. The class can be 'called' with or
    without parenthesis. When parenthesis are not used creates
    ast.Attribute node and when they are used creates ast.Call node.
    Uses get_attribute_name function but with different node parameter
    depending on the case.

    Arguments:
    kwargs can be "splitted" or "omit_n_last".

    Return values:
    On success: name of the class (and trailing attributes depending on
                **kwargs.)
    On failure: empty str ''.
    """

    try:
        name = get_attribute_name(
            node,
            **kwargs
        )
    except AttributeError:
        try:
            name = get_attribute_name(
                node.func,
                **kwargs
            )
        except AttributeError:
            name = ""
    return name

####################################################################
#  Debug functions
def dump_node(node):
    try:
        print(f"{node.lineno}: {ast.dump(node)}")
    except AttributeError:
        print(f"No line: {ast.dump(node)}")


########################################################################
# pre_analyser.py
#
########################################################################
"""Class file. Contains PreAnalyser class."""

class PreAnalyser(ast.NodeVisitor):
    """
    TODO:
    1. Identify lib and main files
    2. Count that there are >= 2 function in lib file
    3. Add General store node function wrapper, maybe??
    """

   # ------------------------------------------------------------------------- #
   # Initialisation
    def __init__(self, library=None):
        self.import_dict = {}
        self.class_dict = {}
        self.function_dict = {}
        self.global_dict = {}
        self.constant_dict = {}
        self.call_dict = {}     # Global scope calls
        self.file_list = []     # Opened filehandles
        self.library = library

   # ------------------------------------------------------------------------- #
   # Getters
    def get_import_dict(self):
        return dict(self.import_dict)

    def get_function_dict(self):
        return dict(self.function_dict)

    def get_class_dict(self):
        return dict(self.class_dict)

    def get_global_dict(self):
        return dict(self.global_dict)

    def get_constant_dict(self):
        return dict(self.constant_dict)

    def get_call_dict(self):
        return dict(self.call_dict)

    def get_file_list(self):
        return list(self.file_list)

   # ------------------------------------------------------------------------- #
   # General methods
    def clear_all(self):
        self.import_dict.clear()
        self.function_dict.clear()
        self.class_dict.clear()
        self.global_dict.clear()
        self.constant_dict.clear()
        self.call_dict.clear()
        self.file_list.clear()
        # del self.library

    def _store_import(self, node, name, import_from=False):
        if self.library:
            name = f"{self.library}.{name}"
        if not name in self.import_dict.keys():
            self.import_dict[name] = []
        self.import_dict[name].append(ImportTemplate(
            name,
            node.lineno,
            node,
            import_from=import_from
        ))

    def _store_assign(self, node):
        def get_names(var, name):
            name.clear()
            try:
                if isinstance(var, ast.Attribute):
                    pass

                elif isinstance(var, ast.Tuple):
                    for i in var.elts:
                        name.append(i.id)

                else:
                    name.append(var.id)

            except AttributeError:
                pass
            return name

        # Global variable detection
        names = []
        for var in node.targets[:]:
            for name in get_names(var, names): # name must be str or int
                if name in self.global_dict.keys():
                    continue

                elif name in self.constant_dict.keys():
                    self.global_dict[name] = self.constant_dict.pop(name, None)

                elif (var.col_offset == 0
                        or get_parent(node, CLS_FUNC) is None):

                    # TODO: imporove this to detect tuples created with
                    # tuple(), which is Call not Tuple
                    if isinstance(node.value, (ast.Constant, ast.Tuple)):
                        self.constant_dict[name] = GlobalTemplate(
                            name,
                            var.lineno,
                            var
                        )
                    else:
                        self.global_dict[name] = GlobalTemplate(
                            name,
                            var.lineno,
                            var
                        )

    def _store_class(self, node):
        imported = False
        key = node.name
        parent = get_parent(node, CLS_FUNC)
        if(parent):
            key = f"{parent.name}.{key}"
        if(self.library):
            key = f"{self.library}.{key}"
            imported = True
        self.class_dict[key] = ClassTemplate(
            node.name,
            node.lineno,
            node,
            imported=imported
        )

    def _store_function(self, node):
        imported = False
        key = node.name
        pos_args = [i.arg for i in node.args.args]
        kw_args = [i.arg for i in node.args.kwonlyargs]

        parent = get_parent(node, CLS_FUNC)
        if parent:
            key = f"{parent.name}.{key}"
        if self.library:
            key = f"{self.library}.{key}"
            imported = True
        #  TODO: If key exist then there are two identically named functions
        # in same scope
        # Could use similar list solution as with imports
        self.function_dict[key] = FunctionTemplate(
            node.name,
            node.lineno,
            node,
            pos_args,
            kw_args,
            imported=imported
        )

    def _store_call(self, node):
        try:
            if (node.col_offset == 0
                    or get_parent(node, CLS_FUNC) is None):
                self.call_dict[node.func.id] = CallTemplate(
                    node.func.id,
                    node.lineno,
                    node
                )
        except AttributeError:
            pass

        try:
            if node.func.id == "open" and isinstance(node.parent_node, ast.Assign):
                # If Call is open call e.g. filehandle = open("filename")
                for opened_file in node.parent_node.targets:
                    self.file_list.append(FilehandleTemplate(
                        name=get_attribute_name(opened_file),
                        lineno=opened_file.lineno,
                        astree=node # or node.parent_node?
                    ))
        except AttributeError:
            pass


   # ------------------------------------------------------------------------- #
   # Visits
    # Imports
    def visit_Import(self, node, *args, **kwargs):
        for i in node.names:
            self._store_import(node, i.name, import_from=False)
        self.generic_visit(node)

    def visit_ImportFrom(self, node, *args, **kwargs):
        self._store_import(node, node.module, import_from=True)
        self.generic_visit(node)

    # Assigns
    def visit_Assign(self, node, *args, **kwargs):
        self._store_assign(node)
        self.generic_visit(node)

    # Classes
    def visit_ClassDef(self, node, *args, **kwargs):
        self._store_class(node)
        self.generic_visit(node)

    # Functions
    def visit_FunctionDef(self, node, *args, **kwargs):
        self._store_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node, *args, **kwargs):
        self._store_function(node)
        self.generic_visit(node)

    # Calls
    def visit_Call(self, node, *args, **kwargs):
        self._store_call(node)
        self.generic_visit(node)


########################################################################
# basic_command_analyser.py
#
########################################################################
"""Class file. Contains BasicsAnalyser class."""

class BasicsAnalyser(ast.NodeVisitor):
    """
    Class to do static analysis by visiting nodes of Abstract Syntax
    Tree. Uses 'ast' module and local 'utils_lib'.
    """

    def __init__(self, model):
        self.model = model
        self.searched_commands = SEARCHED_COMMANDS
        self.valid_naming = get_compiled_regex("valid_naming")

    def check_valid_name(self, node, name, *args, **kwargs):
        """
        Method to validate given name, e.g. variable name or function
        name. Valid names must match following regex pattern
        ^[a-zA-Z_][a-zA-Z0-9_]*$ i.e. they can have only letters from
        a to z (both upper and lowercase), underscore or numbers, and
        may not start with a number.
        """

        try:
            self.model.add_msg(
                "PT2",
                name,
                lineno=node.lineno,
                # Must be re.match, not re.search
                status=(self.valid_naming.match(name) is not None)
            )

        # TypeError Can oocur when name is not string or bytes-like object,
        # e.g. when importing module without as-keyword (as)name will be None.
        except TypeError:
            pass

        # NOTE: using keyword actually creates syntax error to ast.parse
        # therefore this test is no in use
        # if keyword.iskeyword(name):
        #     self.model.add_msg("PT2-1", name, lineno=node.lineno)
        return None

    def iterate_arg_names(self, node, *args, **kwargs):
        """Method to collect all argument names from a given function node.
        This include posonly, 'normal', keyword and prefix arguments (*arg and
        **kwargs).
        Return list of tuples in format [(node, name), (node, name)]
        """
        # TODO move this to preanalyser?

        arg_names = list()
        # Positional and keyword arguments, i.e. all but *args and **kwargs
        try:
            for arg_type in [node.args.posonlyargs,
                             node.args.args,
                             node.args.kwonlyargs]:
                for i in arg_type:
                    arg_names.append((node, i.arg))
        except AttributeError:
            pass

        # Prefix arguments, i.e. *args and **kwargs
        try:
            for prefix_arg in [node.args.vararg, node.args.kwarg]:
                if prefix_arg:
                    arg_names.append((node, prefix_arg.arg))
        except AttributeError:
            pass
        return arg_names

    def _check_function_naming(self, node, *args, **kwargs):
        """Wrapper to check function names."""

        names = self.iterate_arg_names(node)
        try:
            names.append((node, node.name)) # add function name among parameter names
        except AttributeError:
            pass

        for i in names:
            try:
                self.check_valid_name(i[0], i[1]) # i is tuple (node, name)
            except IndexError:
                pass
        return None

    def _check_import_naming(self, node, *args, **kwargs):
        """Wrapper to check import names."""

        try:
            for i in node.names:
                self.check_valid_name(node, i.asname)
        except AttributeError:
            pass

    def _check_unreachable_code(self, node, command_name, *args, **kwargs):
        """
        Method to check if there are lines after the given command. This
        is currently used to check unreachable code after commands:
        return, break, continue, raise, sys.exit, exit, quit
        """

        try:
            self.model.add_msg(
                "PT5",
                command_name,
                lineno=node.lineno,
                status=(node.next_sibling is None)
            )
        except AttributeError:
            pass

   # Grammar info
    # From : https://docs.python.org/3.7/library/ast.html#abstract-grammar

    #    stmt can be: FunctionDef, AsyncFunctionDef, ClassDef, Return, Delete,
    #                 Assign, AugAssign, AnnAssign, For, AsyncFor, While, If,
    #                 With, AsyncWith, Raise, Try, Assert, Import, ImportFrom,
    #                 Global, Nonlocal, Expr, Pass, Break, Continue

    #    expr can be: BoolOp, BinOp, UnaryOp, Lambda, IfExp, Dict, Set,
    #                 ListComp, SetComp, DictComp, GeneratorExp, Await, Yield,
    #                 YieldFrom, Compare, Call, Num, Str, FormattedValue,
    #                 JoinedStr, Bytes, NameConstant, Ellipsis, Constant,
    #                 Attribute, Subscript, Starred, Name, List, Tuple

   # Visits
    def visit_Call(self, node, *args, **kwargs):
        try:
            call_name = node.func.id  # Name of the called function or class
            attribute_name = None  # Library, class or object name which is referred

            # Command called check
            if (isinstance(node.func, ast.Name)
                    and call_name in self.searched_commands
            ):
                self.model.add_msg("PT1", call_name, lineno=node.lineno)

            # Unreachable code check
            if call_name == "exit":
                self._check_unreachable_code(
                    get_parent(node, ast.Expr),
                    "exit"
                )
            elif call_name == "quit":
                self._check_unreachable_code(
                    get_parent(node, ast.Expr),
                    "quit"
                )
        except AttributeError:
            try:
                call_name = node.func.attr  # Name of the called function or class
                attribute_name = node.func.value.id  # Library, class or object name which is referred

                # Unreachable code check
                if attribute_name == "sys" and call_name == "exit":
                    self._check_unreachable_code(
                        get_parent(node, ast.Expr),
                        "sys.exit"
                    )

            except AttributeError:
                pass
        self.generic_visit(node)

    def visit_While(self, node, *args, **kwargs):
        try:
            # Check if there is no break in infinite loop
            status = (not is_always_true(node.test)
                or (get_child_instance(
                    node,
                    (ast.Break, ast.Return, ast.Raise)
                ) is not None) # TODO: Add quit(), exit(), sys.exit()
            )

            self.model.add_msg(
                "PT4-1",
                lineno=node.lineno,
                status=status
            )
        except AttributeError:
            pass
        self.generic_visit(node)

    def visit_For(self, node, *args, **kwargs):
        # iter name check
        try:
            if(isinstance(node.target, ast.Tuple)):
                for i in node.target.elts:
                    self.check_valid_name(node, i.id)
            else:
                self.check_valid_name(node, node.target.id)
        except AttributeError:
            pass
        self.generic_visit(node)

    # Assigns
    def visit_Assign(self, node, *args, **kwargs):
        try:
            # Variable name check
            for i in node.targets:
                self.check_valid_name(node, i.id)
        except AttributeError:
            pass
        self.generic_visit(node)

    # Functions
    def visit_AsyncFunctionDef(self, node, *args, **kwargs):
        # Function name check
        self._check_function_naming(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node, *args, **kwargs):
        # Function name check
        self._check_function_naming(node)
        self.generic_visit(node)

    # Class definitions
    def visit_ClassDef(self, node, *args, **kwargs):
        try:
            # Class Name check
            self.check_valid_name(node, node.name)
        except AttributeError:
            pass
        self.generic_visit(node)

    # With statement
    def visit_With(self, node, *args, **kwargs):
        try:
            # Name check for alias variable after as-keyword
            for i in node.items:
                if(isinstance(i.optional_vars, ast.Tuple)):
                    for i in node.target.elts:
                        self.check_valid_name(node, i.optional_vars.id)
                else:
                    self.check_valid_name(node, i.optional_vars.id)
        except AttributeError:
            pass
        self.generic_visit(node)

    # Except handler
    def visit_ExceptHandler(self, node, *args, **kwargs):
        try:
            # Name check for alias variable after as-keyword
            self.check_valid_name(node, node.name)
        except AttributeError:
            pass
        self.generic_visit(node)

    # Imports
    # visit_alias would be great, but harder to get lineno
    def visit_Import(self, node, *args, **kwargs):
        # Name check for alias variable after as-keyword
        self._check_import_naming(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node, *args, **kwargs):
        # Name check for alias variable after as-keyword
        self._check_import_naming(node)
        self.generic_visit(node)

    # NOTE: Possibly checking Name node could check all the variable etc. names
    # It may give also other names, therefore not yet in use
    # At least function parameters and import aliases are not Name objects
    # def visit_Name(self, node, *args, **kwargs):
    #     try:
    #         self.check_valid_name(node.id)
    #     except AttributeError:
    #         pass
    #     self.generic_visit(node)

    def visit_Return(self, node, *args, **kwargs):
        self._check_unreachable_code(node, "return")

    def visit_Break(self, node, *args, **kwargs):
        self._check_unreachable_code(node, "break")

    def visit_Continue(self, node, *args, **kwargs):
        self._check_unreachable_code(node, "continue")

    def visit_Raise(self, node, *args, **kwargs):
        self._check_unreachable_code(node, "raise")

    # NOTE: yield or yield from can be followed by another code.


########################################################################
# function_analyser.py
#
########################################################################
"""Class file. Contains FunctionAnalyser class."""

class FunctionAnalyser(ast.NodeVisitor):
    # Initialisation
    def __init__(self, model):
        self.model = model
        self.MAIN_FUNC_NAME = MAIN_FUNC_NAME
        self.ALLOWED_FUNC = ALLOWED_FUNCTIONS
        self.DENIED_FUNC = DENIED_FUNCTIONS
        self.MISSING_RETURN_ALLOWED = MISSING_RETURN_ALLOWED
        self.ALLOWED_CONSTANTS = ALLOWED_CONSTANTS

        self.recursive_calls = {}

    def clear_all(self):
        self.recursive_calls.clear()
        return None

    # General methods
    def _check_return(self, node):
        """Method to check
        1. if function is missing a return

        NOTE 1:
        Functions with yield should not give return errors, e.g. AR6
        missing return at the end of the function. This partially
        works e.g. when yield is the last command AR6 is ignored.
        However, yield is rarely the last command of function body.
        """

        try:
            last = node.body[-1]
            status = (
                isinstance(last, ast.Return)
                or (isinstance(last, ast.Expr) and isinstance(last.value, YIELD))
                or "*" in self.MISSING_RETURN_ALLOWED
                or node.name in self.MISSING_RETURN_ALLOWED
            )
        except AttributeError:
            status=False

        finally:
            self.model.add_msg(
                "AR6",
                node.name,
                lineno=node.lineno,
                status=status
            )

    def _check_return_location(self, node):
        """Method to check if node is:
        1. return-statement at the middle of the function.
        """

        self.model.add_msg(
            "AR6-2",
            lineno=node.lineno,
            status=(isinstance(node.parent_node, FUNC))
        )

    def _check_return_value(self, node, *args, **kwargs):
        """Method to check if node is:
        1. Return with missing return value
        2. Returning a constant such as 1 or "abc"
        3. Also detect if return value is
            1. name constant i.e. keyword None, True, False
            2. variable, set, tuple, list, dictionary.
            3. object or other value with attributes
            4. function call, recursive call is detected in visit_Call
               method

        TODO Does not find:
        1. If there are multiple returns
        2. If return is unreachable due to the logical condition,
           trivial cases are check with basic command check for
           unreachable code.
        """

        return_value = node.value
        valid_return = False
        # Match return <without anything>, not return None
        if return_value is None:
            self.model.add_msg("AR6-3", lineno=node.lineno)

        # This match name constants None, True, False
        elif isinstance(return_value, ast.NameConstant):
            # NOTE: since Python 3.8 NameConstants create Constant node but this
            # check seem to work anyway.
            valid_return = True

        # This match variables
        elif isinstance(return_value, ast.Name):
            valid_return = True

        # This match function calls.
        elif isinstance(return_value, ast.Call):
            valid_return = True

        # This match objects and other values with attributes.
        elif (isinstance(return_value, ast.Attribute)
                or (hasattr(return_value, "func")
                and isinstance(return_value.func, ast.Attribute))
        ):
            valid_return = True
        # This match sets, lists, dictionaries.
        elif isinstance(return_value, (ast.List, ast.Dict, ast.Set)):
            valid_return = True

        # This match tuples include also multiple return values case.
        elif isinstance(return_value, ast.Tuple):
            # NOTE: Idea of this check is to detect if student returns e.g.
            # 'return a, b'  which creates a Tuple node, unfortunately then
            # 'return (a, b)' creates an error too. Idea is that in the first
            # one student is not aware what (s)he is doing.
            #
            # if-statement makes 'return (a,)' allowed, however never seen a
            # student doing like that. 'return (a)' will assumet it's an
            # aritmetic operation and will not create a Tuple node.
            if len(return_value.elts) > 1:
                self.model.add_msg("AR6-5", lineno=node.lineno)
            else:
                valid_return = True

        # This match constant strings and numbers.
        elif (isinstance(return_value, (ast.Num, ast.Str, ast.Constant))
                and return_value.value not in self.ALLOWED_CONSTANTS
        ):
            # NOTE: since Python 3.8 ast.Num and ast.Str create ast.Constant
            # node but this check seem to work anyway.
            self.model.add_msg("AR6-4", lineno=node.lineno)

        # This match e.g. aritmetic operations and boolean operations such as
        # return 1 + 2
        # return a or b
        else:
            self.model.add_msg("AR6-6", lineno=node.lineno)

        return valid_return

    def _check_nested_function(self, node, *args, **kwargs):
        """Method to check
        1. function definition is not at a global scope.
        """
        try:
            name = node.name
        except AttributeError:
            return None

        status = True
        # Col offset should detect every function definition which is indended
        if (node.col_offset > 0
            or get_parent(node, CLS_FUNC) is not None
        ):

            # This if check if there are allowed names for methods given.
            if (((not "*" in self.ALLOWED_FUNC and not name in self.ALLOWED_FUNC)
                    and (name in self.DENIED_FUNC or "*" in self.DENIED_FUNC))
                or (get_parent(node, ast.ClassDef) is None)
            ):
                # If function name is not in denied and not in allowed
                # AND there is class as parent, then no error.
                status = False

        self.model.add_msg(
            "AR2-1",
            name,
            lineno=node.lineno,
            status=status
        )
        return None

    def _check_function_attributes(self, node, *args, **kwargs):
        """Check if attribute is added directly to function.
        NOTE: quite identical to detection TR2-1, i.e. CLASS is used
        directly without an object.
        """

        functions = self.model.get_function_dict().keys()

        try:
            for var in node.targets[:]:
                name = get_attribute_name(var, splitted=True)
                if isinstance(var, ast.Attribute) and name[0] in functions:
                    self.model.add_msg("AR7", ".".join(name), lineno=var.lineno)
        except AttributeError:
            pass

    def _check_recursion(self, node, func, *args, **kwargs):
        """
        Private method to detect if function call is directly recursive,
        i.e. if function call inside a function is calling the function
        itself, e.g.:

        def func():
            ...
            func()
            ...

        If recursion is found, adds function to recursive_calls
        dictonary and adds the function call node to FunctionTemplate
        object in that dictionary.
        """

        try:
            # Recursive function calls
            if func == get_parent(node, FUNC).name:
                self.recursive_calls.setdefault(
                    func,
                    self.model.get_function_dict().get(func)
                ).add_recursive_call(node)
        except AttributeError:
            # AttributeError occurs e.g. when function name is searched from
            # the global scope OR when get_parent no match and returns value
            # None, which does not has a attribute name.
            pass

    def _check_paramenters(self, node, function_name, *args, **kwargs):

        def count_args(func_name, funcs, *args, **kwargs):
            func = funcs[func_name] # Shorthand variable for current function.

            has_args = True if func.astree.args.vararg else False
            has_kwargs = True if func.astree.args.kwarg else False
            default_count = len(func.astree.args.defaults)
            args_count = len(func.pos_args)  # This is directly from FunctionTemplate class

            call_arg_count = len(node.args)
            call_pos_args_with_value = 0
            for i in node.keywords:
                if i.arg in func.pos_args:
                    call_pos_args_with_value += 1

            # Checking if there are TOO FEW parameters given
            self.model.add_msg(
                "AR5-1",
                func_name,
                args_count - default_count,
                call_arg_count,
                lineno=node.lineno,
                status=(
                    (call_arg_count + call_pos_args_with_value) >= (args_count - default_count)
                )
            )

            # Checking if there are TOO MANY parameters given
            self.model.add_msg(
                "AR5-2",
                func_name,
                args_count,
                call_arg_count,
                lineno=node.lineno,
                status=(has_args or (call_arg_count <= args_count))
            )

            if not has_kwargs:
                # NOTE Same loop as above, check if possible to combine
                # (note that this is inside if)
                for i in node.keywords:
                    self.model.add_msg(
                        "AR5-3",
                        func_name,
                        i.arg,
                        lineno=node.lineno,
                        status=(i.arg in func.kw_args or i.arg in func.pos_args)
                    )
            return None

        # Parameter and argument check tested with Python 3.8.5
        try:
            funs = self.model.get_function_dict()
            function_names = funs.keys()
            if function_name in function_names:
                count_args(function_name, funs)
        except (AttributeError, KeyError):
            pass
        except:
            pass

    def _found_yield(self, node, yield_type="yield"):
        self.model.add_msg(
            "AR6-1",
            yield_type,
            get_parent(node, FUNC).name,
            lineno=node.lineno
        )

    def _found_global(self, node):
        try:
            for var in node.names:
                self.model.add_msg("AR3", var, lineno=node.lineno)
        except AttributeError:
            pass

    def check_main_function(self, *args, **kwargs):
        if len(self.model.get_call_dict().keys()) > 0:
            self.model.add_msg(
                "AR1",
                status=(
                    self.MAIN_FUNC_NAME in self.model.get_function_dict().keys()
                )
            )
        return None

    def check_element_order(self, body, element_order, *args, **kwargs):
        """Method to check if ast.nodes in 'body' are in desired order.
        Order is defined in element_order with following format:
        ((ast nodes), (must have names/id), (not allowed names/id), "msg ID")

        BKTA get correctly done ONLY when not a single item is wrong,
        but each incorrect one gives one wrong.
        """
        def check_name(tree, required, denied):
            valid = True
            name = ""
            if required or denied:
                for node in ast.walk(tree):
                    n = getattr(node, "name", None)
                    i = getattr(node, "id", None)
                    if n:
                        name = n
                        break
                    elif i:
                        name = i
                        break
                if required and not name in required:
                    valid = False
                elif denied and name in denied:
                    valid = False
            return valid

        cur = 0
        all_correct = True
        for item in body:  # Check items from top to bottom
            temp = cur
            for elem in element_order[cur:]:
                if isinstance(item, elem[0]):
                    try:
                        if check_name(item, elem[1], elem[2]):
                            cur = temp
                            break
                        elif ("Docstring" in elem[1]
                                and isinstance(item.value, ast.Constant)
                                and isinstance(item.value.value, str)
                        ):
                            # Only one docstring is allowed therefore moves to
                            # next element
                            cur = temp = temp + 1
                            break
                    except AttributeError:
                        pass
                temp += 1
            else:
                self.model.add_msg("MR1", lineno=item.lineno)
                all_correct = False

        if all_correct:
            self.model.add_msg("MR1", status=True)
        return None

    def check_global_variables(self):
        for i in sorted(self.model.get_global_variables().values(),
                        key=lambda elem: elem.lineno):
            self.model.add_msg("AR3", i.name, lineno=i.lineno)

    def _exclude_imported_functions(self, fun_dict_full):
        """
        Private method to exclude all the functions which are imported.
        """

        func_dict_local = dict(
            filter(
                lambda elem: not elem[1].imported,
                fun_dict_full.items()
            )
        )
        return func_dict_local

    def check_recursive_functions(self, func_dict):
        """
        Method to detected which functions are done without a single
        recursive call and which ones have one or more recursive call.

        NOTE EACH recursive CALL creates a violation, but each FUNCTION
        without a recursion creates ONE correctly done function.

        Attributes:
        1. func_dict - Dict[FunctionTemplate] - Dictionary containing
           function template objects (defined in templates.py file).
           Keys are str of function name in addition the format
           "parent.name" is also accepted and they are used to get
           values from recursive_calls dictionary.

        Return: None
        """

        try:
            local_functions = self._exclude_imported_functions(func_dict)
            for func_name, func_obj in local_functions.items():
                if (temp := self.recursive_calls.get(func_name)):
                    for node in temp.get_recursive_calls():
                        self.model.add_msg(
                            "AR4",
                            lineno=node.lineno,
                            status=False
                        )
                else:
                    self.model.add_msg(
                        "AR4",
                        lineno=func_obj.lineno,
                        status=True
                    )
        except AttributeError:
            pass

   # Visits
    def visit_Assign(self, node, *args, **kwargs):
        self._check_function_attributes(node)
        self.generic_visit(node)

    def visit_Global(self, node, *args, **kwargs):
        """Method to detect usage of global keyword."""

        self._found_global(node)
        self.generic_visit(node)

    def visit_Return(self, node, *args, **kwargs):
        """Method to detect usage of 'return'."""

        self._check_return_location(node)
        is_valid_return = self._check_return_value(node)

        self.generic_visit(node)

    def visit_Call(self, node, *args, **kwargs):
        """Method to check if node is:
        1. Recursive function call.
        2. Check that arguments and parameters match
        """

        try:
            if hasattr(node.func, "id"):
                fun = node.func.id
            else:
                fun = f"{node.func.value.id}.{node.func.attr}"
        except (AttributeError, Exception): # AttributeError occur e.g. with attribute/method calls.
            pass
        else:
            self._check_recursion(node, fun)
            self._check_paramenters(node, fun)

        self.generic_visit(node)

    def visit_FunctionDef(self, node, *args, **kwargs):
        """Method to find:
        1. Usage of return at the END of the function
        """

        self._check_return(node)
        self._check_nested_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node, *args, **kwargs):
        """Method to check usage of async functions. Currently checks:
        1. If function declaration is nested.
        """
        self._check_return(node)
        self._check_nested_function(node)
        self.generic_visit(node)

    def visit_Yield(self, node, *args, **kwargs):
        """Method to detect usage of yield."""
        self._found_yield(node, yield_type="yield")
        self.generic_visit(node)

    def visit_YieldFrom(self, node, *args, **kwargs):
        """Method to detect usage of yield from."""
        self._found_yield(node, yield_type="yield from")
        self.generic_visit(node)

########################################################################
# file_handling_analyser.py
#
########################################################################
"""Class file. Contains FileHandlingAnalyser class."""

class FileHandlingAnalyser(ast.NodeVisitor):
   # ------------------------------------------------------------------------- #
   # Initialisation
    def __init__(self, model):
        self.model = model
        self.file_operations = {"read", "readline", "readlines", "write", "writelines"}

   # ------------------------------------------------------------------------- #
   # General methods
    def check_left_open_files(self, opened_files, closed_files):
        """Method to detect left open filehandles."""

        for closed in closed_files:
            try:
                closed_name = get_attribute_name(closed)
            except AttributeError:
                continue

            temp = None
            for opened_obj in opened_files:
                if (closed_name == opened_obj.filehandle
                        and closed.lineno >= opened_obj.lineno
                        and get_parent(opened_obj.astree, FUNC)
                        is get_parent(closed, FUNC)):
                    # Lineno check is used to detect correct order when multiple
                    # filehandles have same name in same function. However, this
                    # can fail if opening and closing are e.g. in different
                    # conditional statement branches (and closing branch is
                    # before in line numbers), but then students structure is
                    # already questionable.
                    temp = opened_obj

            # After loop to find the last opened pair for closed filehandle.
            if temp:
                temp.set_closed(closed.lineno)

        for file_obj in opened_files:
            self.model.add_msg(
                "TK1",
                file_obj.name,
                lineno=file_obj.lineno,
                status=(file_obj.closed != 0)
            )

        return None

    def _has_open_and_close(self, node, func_handle, parent=FUNC):
        """Method to detect both, open() and close(), inside function
        and used for same filehandle as defined in "func_handle".

        Check has three return points:
        1. True if parent is with.
        2. True if same function contains open() and close() for same
           file handle as the "func_handle" parameter.
        3. False otherwise.
        """
        try:
            # Check usage of "with" keyword
            if get_parent(node, ast.With) is not None:
                return True

            # Otherwise check function body
            func_node = get_parent(node, parent)
            has_close = has_open = False

            # while (not has_open or not has_close) and (subnode := ast.walk(func_node)):
            for subnode in ast.walk(func_node):
                try:
                    if (not has_close
                        and isinstance(subnode, ast.Attribute)
                        and (subnode.attr == "close")
                        and (get_attribute_name(
                                subnode,
                                omit_n_last=1
                            ) == func_handle)):
                        # When attribute is close and functionhandles have same name
                        # e.g. file_h.close()
                        has_close = True

                    elif (not has_open
                        and isinstance(subnode, ast.Assign)
                        and (subnode.value.func.id == "open")
                        and (get_attribute_name(
                                subnode.targets[0]
                            ) == func_handle)):
                        # When filehandle is assigned for open()-call value.
                        has_open = True

                except AttributeError:
                    continue

                else:
                    if has_open and has_close:
                        return True

        except AttributeError:
            pass
        return False

    def _check_same_parent(self, node, attr, parent):
        """
        Method to detect that if filehandle is read/write inside
        function it is also opened and closed in same function.
        """

        func_handle = get_attribute_name(node.value)
        self.model.add_msg(
            "TK2",
            func_handle,
            attr,
            lineno=node.lineno,
            status=self._has_open_and_close(node, func_handle, parent)
        )

    def _check_file_closing(self, node):
        self.model.set_files_closed(node.value, append=True)
        attr_name = get_attribute_name(node.value)

        # TK1-2 closing file in except branch.
        self.model.add_msg(
            "TK1-2",
            attr_name,
            lineno=node.lineno,
            status=(get_parent(node, ast.ExceptHandler) is None)
        )

        # TK1-3 close has not parenthesis i.e. close not close().
        self.model.add_msg(
            "TK1-3",
            attr_name,
            "close",
            lineno=node.lineno,
            status=(get_parent(
                node,
                ast.Call,
                denied=(ast.Expr,)) is not None
            )
        )
        return None


   # ------------------------------------------------------------------------- #
   # Visits
    def visit_Attribute(self, node, *args, **kwargs):
        """Method to check if node is:
        1. Closing a file.
        2. Closing a file in except branch.
        """

        try:
            if node.attr == "close":
                self._check_file_closing(node)
        except AttributeError:
            pass

        try:
            # node.attr should work even for changed a.b.c.read() attributes.
            if node.attr in self.file_operations:
                self._check_same_parent(node, node.attr, FUNC)
        except AttributeError:
            pass

        self.generic_visit(node)


    def visit_With(self, node, *args, **kwargs):
        try:
            for i in node.items:
                if i.context_expr.func.id == "open":
                    self.model.add_msg("TK1-1", "with open", lineno=node.lineno)
        except AttributeError:
            pass
        self.generic_visit(node)

########################################################################
# data_structure_analyser.py
#
########################################################################
"""Class file. Contains DataStructureAnalyser class."""

class DataStructureAnalyser(ast.NodeVisitor):
   # ------------------------------------------------------------------------- #
   # Initialisations
    def __init__(self, model):
        self.model = model
        self._local_objects = {}    # store objects created in analysed functions
        self._analysed_TR3_2 = {}   # store analysed (function, object) tuples
        self._list_addition_attributes = {"append", "extend", "insert"}


   # ------------------------------------------------------------------------- #
   # General methods
    def _detect_objects(self, tree):
        _objects = []

        classes = self.model.get_class_dict().keys()
        parent = tree.name

        # Linenumber are positive therefore this inactivate skip
        skip_end = -1
        for node in ast.walk(tree):

            # Used to skip nested functions and classes
            try:
                if skip_end >= node.lineno:
                    continue
                elif isinstance(node, CLS_FUNC) and node is not tree:
                    skip_end = node.end_lineno
                    continue
            except AttributeError:
                continue

            # Object detection
            try:
                name = node.value.func.id
                if (isinstance(node, ast.Assign)
                    and ((name in classes)
                        or (f"{parent}.{name}" in classes))
                ):
                    for i in node.targets:
                        _objects.append(
                            ObjectTemplate(
                                get_attribute_name(i),
                                node.lineno,
                                i
                            )
                        )
            except AttributeError:
                pass

        self._local_objects[tree] = _objects
        return None

    def _get_local_object_names(self, func=None):
        """
        Method to return names of the objects within given function. If
        no func-argument is given search objects from every function.

        Names are returned as a list of strings.
        """

        names = []
        if func:
            for i in self._local_objects.get(func, []):
                names.append(i.name)
        else:
            for value in self._local_objects.values():
                for i in value:
                    names.append(i.name)
        return names

    def _get_object_by_name(self, obj_name, func=None):
        """
        Method to return the first object with given name obj_name. If
        func-argument is given search objects only from that function.
        """

        obj = None
        if func:
            for i in self._local_objects.get(func, []):
                if i.name == obj_name:
                    obj = i
                    break
        else:
            for value in self._local_objects.values():
                for i in value:
                    if i.name == obj_name:
                        obj = i
                        # NOTE: using break instead of return would allow same
                        # object from different function to be returned,
                        # therefore it would not be the first object.
                        return obj
        return obj

    def _check_creation_without_parenthesis(self, node):
        """
        Private method to check if object is created (tried to create)
        without parenthesis. Check works when assigned value i.e.
        node.id is class name.
        """

        classes = self.model.get_class_dict().keys()

        try:
            parent = get_parent(node, CLS_FUNC)

            if (temp := self._is_class_call(node, parent, classes)):
                self.model.add_msg(
                    "TR2-2",
                    node.id,
                    lineno=node.lineno,
                    status=(temp > 0) # -1 means class call without parenthesis
                )
        except AttributeError:
            pass
        return None

    def _check_attribute_addition_to_list(self, node):
        """
        Method to detect violation if object's attributes are added to
        a list inside a loop. The expected way is to add the object
        itself, not the attribute.
        """
        status = False

        try:
            # Get parent function and name of the object

            # NOTE: name is take from outermost attribute e.g. in case of
            # example_list = [param.object.value]
            # the param creates the outermost Attribute node. In this case the
            # last attribute is ommitted because it is ATTRIBUTE's name not name
            # of the OBJECT.
            func = get_parent(node, FUNC)
            outermost_attr = get_outer_parent(
                node,
                ast.Attribute,
                denied=(ast.List, ast.Call)
            )

            if outermost_attr == node:
                obj = get_attribute_name(node)
                status = True
            else:
                obj = get_attribute_name(outermost_attr, omit_n_last=1)

            # Test if object (or its attribute) is added to the list inside a
            # loop
            if (obj in self._get_local_object_names(func)
                and get_parent(node, LOOP)
                and is_added_to_data_structure(
                        node,
                        ast.List,
                        "list",
                        self._list_addition_attributes
                    )
            ):
                self.model.add_msg(
                    "TR3-1",
                    lineno=node.lineno,
                    status=status
                )
        except (AttributeError, KeyError):
            pass
        return None

    def _check_object_outside_loop(self, node, assing_loop):
        """
        Method to check if object creation is outside a loop and object
        (attribute) values are assigned inside the loop and then object
        is put into a list.
        """

        # Get the function where object is created, if there is no parent
        # function, func is None and all the objects are searched in later step.
        func = get_parent(node, FUNC)

        for var in node.targets:
            try:
                # Check that value is assigned to an object (or other attribute)
                # If not, it is irrelevant var for this check and we continue.
                if not isinstance(var, ast.Attribute):
                    continue

                # Get an object and a loop where values are assigned to object's
                # attributes.
                name = get_attribute_name(var, omit_n_last=1)
                if (not (obj := self._get_object_by_name(name, func))
                    or obj.lineno > node.lineno
                ):
                    continue

                creation_loop = get_parent(obj.astree, LOOP)

            except AttributeError:
                continue

            # TODO: This is now done everytime object attribute is assigned
            # inside a loop. Optimize this such that objects are first gathered
            # and then only one walk to check all of them.
            for elem in ast.walk(assing_loop):
                try:
                    # NOTE: condition "not (func, obj.name) in self._analysed_TR3_2.keys()"
                    # would limits analysis of each object to single case
                    # because otherwise each list.append(obj) and obj.attr
                    # triggers new BTKA result
                    if ((obj.name == get_attribute_name(elem))
                        # and not (func, obj.name) in self._analysed_TR3_2.keys()
                        and is_added_to_data_structure(
                            elem,
                            ast.List,
                            "list",
                            self._list_addition_attributes
                        )
                    ):
                    # 'status' tells if creation of object is in the same
                    # loop as value is assigned to the attribute. If yes, no
                    # violation.
                        self.model.add_msg(
                            "TR3-2",
                            lineno=obj.lineno,
                            status=(creation_loop == assing_loop)
                        )

                        self._analysed_TR3_2.setdefault(
                            (func, obj.name),
                            []
                        ).append(elem.lineno)
                except AttributeError:
                    continue
        return None

    def _is_class_call(self, node, parent, classes):
        """
        Method to check if node is a call of a class.

        Arguments:
        node: node itself usually Name node which is e.g. in Assign
                nodes value.
        parent: can be name of a class, function or imported module,
                which is parent of the node.
        classes: is list dict_keys() of class names. If class has parent
                it is included into a name 'parent.class_name'.

        Three different return values:
         0: No class name and not a call, i.e. something not relevant.
         1: Class name and call, e.g. obj = CLASS()
        -1: Class name but not a call, e.g. obj = CLASS
        """

        _IRRELEVANT = 0
        _CLASS_CALL = 1
        _CALL_WITHOUT_PARENTHESIS = -1

        is_call = False
        try:
            if (temp := get_parent(
                    node,
                    ast.Call,
                    denied=(ast.Assign,) + CLS_FUNC)):
                # There is a Call node as a parent
                is_call = True
                name = get_class_name(temp)

            elif (temp := get_outer_parent(
                    node,
                    ast.Attribute,
                    denied=(ast.Assign, ast.Call) + CLS_FUNC)):
                # There is one or more Attribute nodes as parents
                name = get_attribute_name(temp)

            else:
                name = get_attribute_name(node)

            if (name in classes) or (f"{parent.name}.{name}" in classes):
                if is_call:
                    return _CLASS_CALL
                else:
                    return _CALL_WITHOUT_PARENTHESIS

        except AttributeError:
            pass

        return _IRRELEVANT

    def _check_class(self, node):
        """
        Method to check
        1. Class is created in global scope
        2. Class name is written with UPPERCASE letters.
        """

        name = node.name

       # Class is at global scope check
        # Col offset should detect every class definition which is indended
        # but status is verified with parent check.
        self.model.add_msg(
            "TR2-3",
            name,
            lineno=node.lineno,
            status=(
                node.col_offset == 0
                or get_parent(node, CLS_FUNC) is None
            )
        )

       # Class name is UPPERCASE check
        self.model.add_msg(
            "TR2-4",
            name,
            lineno=node.lineno,
            status=(name.isupper())
        )

   # ------------------------------------------------------------------------- #
   # Visits
    def visit_Assign(self, node, *args, **kwargs):
        """Method to find:
        1. Direct usage of CLASS variables via class itself.
        2. Assiging CLASS to variable, i.e. object = CLASS <without parenthesis>
        3. Object creation outside a loop and object (attribute) values
           are assigned inside the loop and then object is put into a
           list.
        """

        classes = self.model.get_class_dict().keys()

        try:
            for var in node.targets[:]:
                name = get_attribute_name(var, splitted=True)
                # TODO change check such that when attribute is used via object
                # it is fine and when it is used via class (this now detects
                # this case) it is not fine.
                if isinstance(var, ast.Attribute) and (name[0] in classes):
                    self.model.add_msg("TR2-1", ".".join(name), lineno=var.lineno)
        except AttributeError:
            pass

        # Check if assigning value to object attribute is inside a loop,
        # if not, no other target can be inside a loop either.
        if (loop := get_parent(node, LOOP)):
            self._check_object_outside_loop(node, loop)

        self.generic_visit(node)

    def visit_Name(self, node, *args, **kwargs):
        """Method to do checks for ast.Name nodes."""

        self._check_creation_without_parenthesis(node)
        self._check_attribute_addition_to_list(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node, *args, **kwargs):
        """Method to call class checks of ClassDef nodes."""

        self._check_class(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node, *args, **kwargs):
        """Method to call detect objects for current namespace."""

        self._detect_objects(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node, *args, **kwargs):
        """Method to call detect objects for current namespace."""

        self._detect_objects(node)
        self.generic_visit(node)


########################################################################
# exception_handling_analyser.py
#
########################################################################
"""Class file. Contains ExceptionHandlingAnalyser class."""

class ExceptionHandlingAnalyser(ast.NodeVisitor):
   # ------------------------------------------------------------------------- #
   # Initialisation
    def __init__(self, model):
        self.model = model
        self.file_operations = {
            "read", "readline", "readlines", "write", "writelines"
        }
   # ------------------------------------------------------------------------- #
   # Getters

   # ------------------------------------------------------------------------- #
   # Setters

   # ------------------------------------------------------------------------- #
   # General methods
    def _has_exception_handling(self, node, denied=FUNC):
        """Check to determine if node is inside exception handling."""

        if get_parent(node, ast.Try, denied=denied) is None:
            return False
        return True

    def _check_exception_handling(self, node):
        """
        Method to check if node has:
        1. Missing try - except around file opening.
        """

        try:
            if node.func.id == "open":
                self.model.add_msg(
                    "PK3",
                    lineno=node.lineno,
                    status=self._has_exception_handling(node)
                )
        except AttributeError:
            pass

    def _check_exception_handlers(self, node):
        """
        Method to check if node is:
        1. Try with no exception branches
        2. Exception branch missing an error type. Excluding the last
            exception IF there are more than one exception branches.

        ast.Try has lists for each branchtype: handlers=[], orelse=[],
        finalbody=[], which are for excepts, else and finally,
        respectively

        Does not analyse
        1. finally branches
        2. else branches
        """

        try:
            self.model.add_msg(
                code="PK1",
                status=(len(node.handlers) >= 1),
                lineno=node.lineno
            )

            for handler in node.handlers:  # handler is ast.ExceptHandler object
                self.model.add_msg(
                    code="PK1-1",
                    status=(handler.type != None),
                    lineno=handler.lineno
                )

        except AttributeError:
            pass

   # ------------------------------------------------------------------------- #
   # Visits
    def visit_Try(self, node, *args, **kwargs):
        """Method to visit Try nodes."""

        self._check_exception_handlers(node)
        self.generic_visit(node)

    def visit_Call(self, node, *args, **kwargs):
        """Method to visit (function) Call nodes."""

        self._check_exception_handling(node)
        self.generic_visit(node)

    def visit_Attribute(self, node, *args, **kwargs):
        """
        Method to check if node is:
        1. Missing try - except around file.read().
        2. Missing try - except around file.readline().
        3. Missing try - except around file.readlines().
        4. Missing try - except around file.write().
        5. Missing try - except around file.writelines().
        """

        try:
            if node.attr in self.file_operations:
                self.model.add_msg(
                    "PK4",
                    get_attribute_name(node),
                    lineno=node.lineno,
                    status=self._has_exception_handling(node)
                )
        except AttributeError:
            pass
        self.generic_visit(node)

    def visit_For(self, node, *args, **kwargs):
        """
        Method to check if node is:
        1. For loop reading a file AND missing exception handling.
        """

        try:
            names = [i.filehandle for i in self.model.get_files_opened()]

            iter_name = ""
            if isinstance(node.iter, (ast.Name, ast.Attribute)):
                iter_name = get_attribute_name(node.iter)

            # Special case for 'for ... in enumerate(filehandle)'
            # Only works if there is one call, not call inside calls
            elif isinstance(node.iter, ast.Call) and node.iter.func.id == "enumerate":
                iter_name = get_attribute_name(node.iter.args[0])

            if iter_name in names:
                try:
                    msg_arg = f"for {node.target.id} in {iter_name}"
                except AttributeError:
                    msg_arg = f"for ... in ..."
                finally:
                    self.model.add_msg(
                        "PK4",
                        msg_arg,
                        lineno=node.lineno,
                        status=self._has_exception_handling(node)
                    )

        except (AttributeError, TypeError):
            pass
        self.generic_visit(node)


########################################################################
# file_structure_analyser.py
#
########################################################################
"""Class file. Contains FileStructureAnalyser class."""

class FileStructureAnalyser(ast.NodeVisitor):
    """
    TODO:
    1. Identify lib and main files
    2. Count that there are >= 2 function in lib file
    """

   # ------------------------------------------------------------------------- #
   # Initialisations
    def __init__(self, model):
        self.model = model

   # ------------------------------------------------------------------------- #
   # General methods
    def check_info_comments(self, content, n=10):
        """
        Function to check the info comments at the beginning of the
        file. Beginning is n fist lines, default 10. Checked infos are:
        1. Author            ('Tekijä')
        2. Student number    ('Opiskelijanumero')
        3. Date              ('Päivämäärä')
        4. Co-operation      ('Yhteistyö')

        Currently does NOT check that they are in comments or docstring.
        """

        # file.__doc__ could be used to check docstring.
        # Could use regex to match 10 lines and find words from there.
        author = student_num = date = coop = all_found = False
        for line in content.split("\n", n)[:n]:
            # Could add error for each of missing words (then use regex)
            line = line.strip()
            if "Tekijä" in line:
                author = True
            elif "Opiskelijanumero" in line:
                student_num = True
            elif "Päivämäärä" in line:
                date = True
            elif "Yhteistyö" in line:
                coop = True

            if author and student_num and date and coop:
                all_found = True
                break

        self.model.add_msg("MR5", n, lineno=1, status=all_found)
        return None

    def has_main_function(self, tree):
        """
        TODO: change this to check of main level function calls
        """

        call_count = 0
        # TODO: Parse nested function names, which are in format parent.functionName
        fun_list = self.model.get_function_dict().keys()
        for node in tree.body:
            if hasattr(node, "value") and isinstance(node.value, ast.Call):
                call_count += 1
                try:
                    name = get_attribute_name(node.value.func)
                    # TODO Call count could be replaced by model's call_dict()
                    # if call_dict would contain every call not just every
                    # unique call name.
                    if name in fun_list:
                        self.model.add_msg(
                            "MR2-3",
                            name,
                            call_count,
                            lineno=node.lineno,
                            status=(call_count <= 1)
                        )
                except AttributeError:
                    pass

                try:
                    # TODO: Check that node is not class which has the main
                    # function in it
                    func = node.value.func
                    self.model.add_msg(
                        "MR2-4",
                        get_attribute_name(func),
                        lineno=node.lineno,
                        status=(not isinstance(func, ast.Attribute))
                    )
                except AttributeError:
                    pass

    def check_duplicate_imports(self, import_dict):
        for value in import_dict.values():
            if len(value) <= 1: # Correctly done only 1 import per module
                self.model.add_msg(
                    "MR3-1" if value[0].import_from else "MR3",
                    value[0].name,
                    lineno=value[0].lineno,
                    status=True
                )
            else: # Too many imports i.e. incorrectly done (in course's context)
                for i in sorted(value, key=lambda elem: elem.lineno)[1:]:
                    ID = "MR3-1" if i.import_from else "MR3"
                    self.model.add_msg(
                        ID,
                        i.name,
                        lineno=i.lineno,
                        status=False
                    )
        return None

    def _check_import(self, node, lib_name, importFrom=False):
        """Method to check if import is not at global namespace."""

        self.model.add_msg(
            "MR4",
            lib_name,
            lineno=node.lineno,
            status=(get_parent(node, CLS_FUNC) is None)
        )

   # ------------------------------------------------------------------------- #
   # Visits
    def visit_Import(self, node, *args, **kwargs):
        for i in node.names:
            self._check_import(node, i.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node, *args, **kwargs):
        self._check_import(node, node.module, importFrom=True)
        self.generic_visit(node)

########################################################################
# analysis_lib.py
#
########################################################################
"""File to handle ASPA static analysers."""


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.settings = self.controller.get_settings()
        self.violation_occurances = {}

        try:
            self.language = self.settings["language"]
        except KeyError:  # This should not be possible if defaults settings are not changed
            self.language = "FIN"
            self.controller.propagate_error_message("NO_LANGUAGE")

        try:
            self.checkbox_options = self.settings["checkbox_options"]
        except KeyError:   # This should not be possible if defaults settings are not changed
            # These could be in utils not in settings
            self.checkbox_options = [
                "basic",
                "function",
                "file_handling",
                "data_structure",
                "library",
                "exception_handling"
            ]
        # There is possibility that there are no 6 elements in checkbox options,
        # but that is modified in the code then, i.e. not by user
        try:
            self.analysers = {
                self.checkbox_options[0]: BasicsAnalyser(self),
                self.checkbox_options[1]: FunctionAnalyser(self),
                self.checkbox_options[2]: FileHandlingAnalyser(self),
                self.checkbox_options[3]: DataStructureAnalyser(self),
                self.checkbox_options[4]: FileStructureAnalyser(self),
                self.checkbox_options[5]: ExceptionHandlingAnalyser(self)
            }
        except IndexError:
            pass
        # Pre analyser
        self.pre_analyser = PreAnalyser()
        self.constant_variables = {}

        # Variable data structures (used by function_analyser)
        self.global_variables = {}
        self.local_variables = set()
        self.call_dict = {}

        # File handling (used by file_handling_analyser)
        self.files_opened = []
        self.files_closed =  []

        # File structure list and dict used by file_structure_analyser
        # and data_structure_analyser
        self.function_dict = {}
        self.class_dict = {}

        # File structure lists used by file_structure_analyser
        self.file_list = []
        self.lib_list = []
        self.import_dict = {}

        # Result list for checks from each category and list for storing
        # category_result lists
        self._category_results = []
        self.all_results = []

   # Datastructure getters
    def get_call_dict(self):
        return dict(self.call_dict)

    def get_global_variables(self):
        return dict(self.global_variables)

    def get_local_variables(self):
        return set(self.local_variables)

    def get_import_dict(self):
        return dict(self.import_dict)

    def get_files_opened(self):
        return list(self.files_opened)

    def get_files_closed(self):
        return list(self.files_closed)

    def get_file_list(self):
        return list(self.file_list)

    def get_lib_list(self):
        return list(self.lib_list)

    def get_function_dict(self):
        return dict(self.function_dict)

    def get_class_dict(self):
        return dict(self.class_dict)


   # List, dict and set setters
    def set_call_dict(self, value, key=None):
        if(key):
            self.call_dict[key] = value
        else:
            self.call_dict = dict(value)

    def set_global_variables(self, value, key=None):
        if(key):
            self.global_variables[key] = value
        else:
            self.global_variables = dict(value)

    def set_local_variables(self, value, add=False):
        if(add):
            self.local_variables.add(value)
        else:
            self.local_variables = set(value)

    def set_files_opened(self, value, append=False):
        if(append):
            self.files_opened.append(value)
        else:
            self.files_opened = list(value)

    def set_files_closed(self, value, append=False):
        if(append):
            self.files_closed.append(value)
        else:
            self.files_closed = list(value)

    def set_file_list(self, value):
        self.file_list = list(value)

    def set_import_dict(self, value, key=None):
        if(key):
            self.import_dict[key] = value
        else:
            self.import_dict = dict(value)

    def set_function_dict(self, value, key=None):
        if(key):
            self.function_dict[key] = value
        else:
            self.function_dict = dict(value)

    def set_class_dict(self, value):
        self.class_dict = dict(value)

    def set_lib_list(self, value, append=False):
        if(append):
            self.lib_list.append(value)
        else:
            self.lib_list = list(value)

   # General methods
    def clear_analysis_data(self):
        self.all_results.clear()
        self.global_variables.clear()
        self.local_variables.clear()
        self.files_opened.clear()
        self.files_closed.clear()
        self.function_dict.clear()
        self.class_dict.clear()
        self.file_list.clear()
        self.lib_list.clear()
        self.import_dict.clear()
        self.call_dict.clear()
        self.constant_variables.clear() # Not yet used but cleared anyway

    # TODO rename this method to something better, e.g. add_result
    def add_msg(self, code, *args, lineno=-1, status=False):
        """
        Method which creates a violation object based on arguments and
        add the object to result list.

        Arguments:
        1. code is ID for detected violation (or correctly done action).
        2. *args are possible arguments for message formating.
        3. lineno is linenumber where violation was detected.
        4. status is True or False, where True means something is done
           right, i.e. no violation, while False means it is done
           incorrectly, i.e. it is a violation.

        Return: None
        """

        if not ignore_check(code):
            self._category_results.append(
                ViolationTemplate(code, args, lineno, status)
            )

            # Very primitive statistic calculation
            try:
                self.violation_occurances[code] += 1
            except KeyError:
                self.violation_occurances[code] = 1
        return None

    def save_category(self, title):
        self.all_results.append((title, tuple(self._category_results)))
        self._category_results.clear()

    def default_analyse(self, selections, file_list, result_page, *args, **kwargs):
        """
        Method to handle default analysis steps where coding convention
        violations are detected. This includes:
        1. Initialising result file.
        2. Iterating analysed files.
        3. Formating each file's results
        4. Showing results.
        5. Clearing results.
        """

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        write_file(self.settings["result_path"], timestamp + "\n")

        for filepath in file_list:
            results = self.execute_analysis(filepath, selections)

            # Format results
            formated_results = self.format_violations(results)

            # Add filename and filepath at the beginning of the result list
            formated_results.insert(
                0, (create_dash(character="=", get_dash=True), GENERAL)
            )
            if (self.settings["shown_filepath_format"]
                    in OPTIONS_FOR_ALL + FILENAME_OPTIONS):
                formated_results.insert(1, (filepath.filename, GENERAL))

            if (self.settings["shown_filepath_format"]
                    in OPTIONS_FOR_ALL + FILEPATH_OPTIONS):
                formated_results.insert(1, (str(filepath.path), GENERAL))

            # Show results and clear results
            result_page.show_results(formated_results)
            self.clear_analysis_data()
            formated_results.clear()
        return None

    def BKT_analyse(self, selections, file_dict, *args, **kwargs):
        """
        Method to control Bayesian Knowledge Tracing analysis steps.
        This includes:
        1. Initialising result file.
        2. Iterating analysed files.
        3. Showing results.
        4. Clearing results.
        """
        return None

    def execute_analysis(self, filepath, selections):
        """
        Method to handle analysis execution steps:
        1. Reading file.
        2. Parsing AST from file.
        3. Calling AST analyser.
        4. Returning results.

        Return: List of tuples, where tuples include result messages.
        """

        content = read_file(filepath.path)
        filename = filepath.filename
        dir_path = filepath.path.parent

        # No check for tree being None etc. before analysis because analyses
        # will create violation if tree is not valid. Only in dumping checks
        # if tree exist.
        tree = self.parse_ast(content, filename)

        # Dump tree
        if(tree and self.settings["dump_tree"]):
            self.dump_tree(tree)

        # Call analyser
        results = self.analyse(
            tree,
            content,
            dir_path,
            filename,
            selections
        )
        return results

    def parse_ast(self, content, filename, create_msg=True):
        """
        Creates an abstract syntax tree and adds both parent and sibling
        nodes.

        Return: Python ast typed tree or None if parse fails.
        """

        tree = None
        try:
            tree = ast.parse(content, filename)

        except SyntaxError:
            if create_msg:
                self.add_msg("syntax_error")
                self.save_category("file_error")

        # When content is not str or AST (e.g. None), usually due failed
        # file reading.
        except TypeError:
            if create_msg:
                self.add_msg("type_error")
                self.save_category("file_error")

        else:
            add_parents(tree)
            add_siblings(tree)

        finally:
            return tree

    def analyse(self, tree, content, dir_path, filename, selections):
        """
        Analysis wrapper for preanalyser and analyser which do analysis
        for abstract syntax tree and file content from the ast is
        created.

        Return: List of violation messages.
        """

        try:
            files_in_dir = os.listdir(dir_path)
            self.pre_analyse_tree(tree, files_in_dir, dir_path)
            self.analyse_tree(tree, files_in_dir, content, selections)

        except Exception:
            self.clear_analysis_data()
            self._category_results.clear()
            self.add_msg("tool_error", filename)
            self.save_category("analysis_error")

        return self.all_results

    def pre_analyse_tree(self, tree, files, dir_path):
        """
        Preanalyses abstract syntax tree and all imported local
        libraries.
        """

        self.pre_analyser.visit(tree)
        self.class_dict = self.pre_analyser.get_class_dict()
        self.function_dict = self.pre_analyser.get_function_dict()
        self.import_dict = self.pre_analyser.get_import_dict()
        self.global_variables = self.pre_analyser.get_global_dict()
         # This need setter, getter and initialisation if used
        self.constant_variables = self.pre_analyser.get_constant_dict()
        self.call_dict = self.pre_analyser.get_call_dict()
        self.files_opened = self.pre_analyser.get_file_list()
        self.pre_analyser.clear_all()

        imported = self.import_dict.keys()
        for i in imported:
            filename = f"{i}.py"
            if(filename in files):
                self.lib_list.append(i)
                content = read_file(pathlib.Path.joinpath(dir_path, filename))

                if not (tree := self.parse_ast(content, filename, create_msg=False)):
                    continue

                # Preanalysing imported local files
                analyser = PreAnalyser(library=i)
                analyser.visit(tree)
                for func, value in analyser.get_function_dict().items():
                    if(not func in self.function_dict.keys()):
                        self.function_dict[func] = value
                analyser.clear_all()

    def analyse_tree(self, tree, file_list, content, selections):
        """
        Analyses abstract syntax tree and file content from the ast is
        created. Execute only analyses marked with selections argument.

        Return: List of violation messages.
        """

        # self.file_list = file_list

        for opt in self.checkbox_options:
            if(selections[opt]):
                analyser = self.analysers[opt]
                analyser.visit(tree)

                if(opt == "file_handling"):
                    # Check left open files
                    analyser.check_left_open_files(
                        self.files_opened,
                        self.files_closed
                    )

                elif(opt == "function"):
                    analyser.check_main_function()
                    analyser.check_element_order(tree.body, ELEMENT_ORDER)
                    analyser.check_global_variables()
                    analyser.check_recursive_functions(self.function_dict)
                    analyser.clear_all()

                elif(opt == "library"):
                    # Info comments check, i.e. author, date etc.
                    analyser.check_info_comments(content)

                    # Duplicate import check
                    analyser.check_duplicate_imports(self.import_dict)

                    # Main file check
                    if(analyser.has_main_function(tree)): # True this should be a main file
                        pass
                    else: # Else means library file.
                        pass

                self.save_category(opt)

    def format_violations(self, all_results):
        """
        Method to format results to violations. Category titles are
        included between results. Includes only results which are
        violations.

        Return: List of violation tuples.
        """

        line_list = []
        violations = []
        for title_key, results in all_results:
            violations.clear()

            # Every line after each topics is empty to make view less crowded.
            line_list.append(("", GENERAL))

            # Include only violations
            for violation in results:
                if violation.status == False:  # False means there is a violation
                    violations.append(violation)

            # Check if there are violations in this topic/title, if not go to
            # next title/analysis category.
            if len(violations) == 0:
                line_list.append(
                    create_title('OK', title_key, lang=self.language)
                )
                continue

            # There is one or more violations in this topic/title so need to add
            # a note.
            line_list.append(
                create_title('NOTE', title_key, lang=self.language)
            )

            for violation in violations:
                line_list.append(violation.get_msg(self.language))
        violations.clear()

        return line_list

   ####################################################################
   #  Debug functions
    def dump_tree(self, tree):
        create_dash()
        print(ast.dump(tree, include_attributes=True))
        print()
        print(ast.dump(tree, include_attributes=False))
        print()
        print(ast.dump(tree, annotate_fields=False, include_attributes=False))
        create_dash()

########################################################################
# view_lib.py
#
########################################################################
"""Module for TKinter GUI frames."""

# Constants
# BG_COLOR = cnf.BG_COLOR # None #"#bababa" #None # "#383838"
# FRAME_COLOR = cnf.FRAME_COLOR # None #"#ffcfcf"
# PAD = cnf.PAD # 5
# LARGE_FONT = cnf.LARGE_FONT # "None 12 bold"
# NORMAL_FONT = cnf.NORMAL_FONT # "None 10"
# SMALL_FONT = cnf.SMALL_FONT # "None 8"
# FONT_COLOR = cnf.FONT_COLOR # "black"
# BD_STYLE = cnf.BD_STYLE # tk.RIDGE # Border style
# BD = cnf.BD # 2              # Border width
# HIGHLIGHT = cnf.HIGHLIGHT

def set_style_constants(settings):

    def parse_font(font_style, value):
        if value:
            parts = font_style.split(" ")
            parts[1] = str(value)
            font_style = " ".join(parts)
        return font_style

    global LARGE_FONT, NORMAL_FONT, SMALL_FONT, TEXTBOX_FONT

    LARGE_FONT = parse_font(LARGE_FONT, settings.get("title_font_size")) # "None 12 bold"
    NORMAL_FONT = parse_font(NORMAL_FONT, settings.get("normal_font_size")) # "None 10"
    SMALL_FONT = parse_font(SMALL_FONT, settings.get("small_font_size")) # "None 8"

    # Tk Text (i.e. textboxs)
    TEXTBOX_FONT = font.nametofont("TkFixedFont")
    TEXTBOX_FONT.configure(size=settings.get("normal_font_size", 10))

    # Ttk buttons
    ttk.Style().configure("TButton", font=NORMAL_FONT)
    return None

################################################################################
class MainFrame(tk.Frame):
    def __init__(self, parent, lang):
       # -------------------------------------------------------------------- #
       # Variable and grid initialisations
        controller = parent
        tk.Frame.__init__(self, controller)

        self.LANG = lang
        self.pack(side="top", fill="both", expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        settings = controller.get_settings()
        set_style_constants(settings)

       # --------------------------------------------------------------------- #
       # Content pages
        self.pages = {}

         # CLASS names are keys.
        for page_class in (AnalysePage, ResultPage):
            page = page_class(self, controller, settings)
            self.pages[page_class] = page
            page.grid(row=0, column=0, sticky=tk.NSEW)
        self.show_page(AnalysePage)

    def get_page(self, page_class):
        """Method to return object of asked page class."""
        return self.pages[page_class]

    def show_page(self, page_class):
        """Method to show asked page based on given page_class."""
        # TODO: Hide pages on background if possible
        page = self.pages[page_class]
        page.tkraise()


################################################################################
class CheckboxPanel(tk.Frame):
    """Class to view checkbox panel. Usage clarification:
    in __init__ the self (i.e. inherited tk.Frame)
    is a master to all elements in this frame.
    """

    def __init__(self, parent, checkbox_options):
        tk.Frame.__init__(self, parent, bd=BD, relief=BD_STYLE)
        tk.Label(
            self,
            text=GUI[parent.LANG]["select_analysis_title"],
            bg=BG_COLOR,
            fg=FONT_COLOR,
            font=LARGE_FONT
        ).grid(row=0, column=0, columnspan=2, padx=PAD, pady=PAD)

        self.selected_analysis = {}
        count = 0
        for i in checkbox_options:
            count += 1
            self.selected_analysis[i] = tk.IntVar()
            self.selected_analysis[i].set(1)
            try:
                option = TEXT[parent.LANG][i]
            except KeyError:
                option = i

            cb = tk.Checkbutton(
                master=self,
                text=option,
                font=NORMAL_FONT,
                width=20,
                anchor=tk.W,
                variable=self.selected_analysis[i]
            )
            cb.grid(row=count, column=1, sticky=tk.W)

    def check(self, keys, value=1):
        """Method to set given value for given checkboxes."""
        for key in self.selected_analysis.keys():
            self.selected_analysis[key].set(0)
        if value != 0:
            try:
                for key in keys:
                    self.selected_analysis[key].set(1)
            except KeyError:
                pass
        return None

    def get_selections(self):
        return self.selected_analysis


################################################################################
class FiledialogPanel(tk.Frame):
    def __init__(self, parent, root, default_files):
        tk.Frame.__init__(self, parent, bd=BD, relief=BD_STYLE)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.root = root
        self.parent = parent

        # Title label
        tk.Label(
            self,
            text=GUI[parent.LANG]["filepaths"],
            bg=BG_COLOR,
            fg=FONT_COLOR,
            font=LARGE_FONT
        ).grid(row=0, column=0, sticky=tk.W, padx=PAD, pady=PAD)

        # File dialog buttons
        ttk.Button(
            self,
            text=GUI[parent.LANG]["select_file"],
            command=self.get_filedialog
        ).grid(row=0, column=1, padx=PAD, pady=PAD, sticky=tk.E)

        ttk.Button(
            self,
            text=GUI[parent.LANG]["select_folder"],
            command=lambda: self.get_filedialog(directory=True)
        ).grid(row=0, column=2, padx=PAD, pady=PAD, sticky=tk.E)

        ttk.Button(
            self,
            text=GUI[parent.LANG]["clear"],
            command=self.clear_files
        ).grid(row=0, column=3, padx=PAD, pady=PAD, sticky=tk.E)


        # Create output text box
        self.filebox = tk.Text(
            self,
            width=50,
            height=10,
            bg=BG_COLOR,
            fg=FONT_COLOR,
            font=TEXTBOX_FONT, #font=SMALL_FONT
        )
        self.filebox.grid(
            row=1,
            column=0,
            columnspan=4,
            sticky=tk.NSEW,
            padx=PAD,
            pady=PAD
        )

        for filepath in default_files:
            self.add_file(filepath)

    def get_filedialog(self, directory=False):
        initdir = self.root
        # File dialog
        if directory:
            path = filedialog.askdirectory(
                initialdir=initdir,
                title=GUI[self.parent.LANG]["select_folder"]
            )
        else:
            path = filedialog.askopenfilename(
                initialdir=initdir,
                title=GUI[self.parent.LANG]["select_file"],
                filetypes=(
                    ("Python", "*.py"),
                    (GUI[self.parent.LANG]["all_files"], "*")
                ),
                multiple=True
            )

        if isinstance(path, tuple):
            for p in path:
                self.add_file(p)
        elif path:
            self.add_file(path)
        return None

    def add_file(self, path):
        self.filebox.config(state="normal")
        self.filebox.insert(tk.END, path + "\n")
        self.filebox.config(state="disabled")

    def clear_files(self):
        self.filebox.config(state="normal")
        self.filebox.delete(1.0, tk.END)
        self.filebox.config(state="disabled")

    def parse_filepaths(self, clear=False):
        pathset = set()
        for path in self.filebox.get(0.0, tk.END).split("\n"):
            path = path.strip()
            if path != "":
                pathset.add(path)
        if clear:
            self.clear_files()
        return pathset

    def get_filepath_list(self, clear=False):
        return self.parse_filepaths(clear)

class ControlPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bd=BD, relief=BD_STYLE)
        button_group = tk.Frame(master=self, bg=FRAME_COLOR)
        button_group.pack(side=tk.TOP)

        run_button = ttk.Button(
            button_group,
            text=GUI[parent.LANG]["execute_analysis"],
            command=lambda: parent.analyse(
                controller.analyse_wrapper,
                analysis_type="default"
            )
        )
        run_button.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=tk.E)

################################################################################
class AnalysePage(tk.Frame):
    """Class to view analyse page. Usage clarification:
    in __init__ the self (i.e. inherited tk.Frame)
    is a master to all elements in this frame.
    """

    def __init__(self, parent, controller, settings):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.LANG = self.controller.get_lang()
        self.CLEAR_FILEPATHS = settings.get("clear_filepaths", False)
        # self.model = model

        self.ctrl_panel = ControlPanel(self, controller)
        self.check_panel = CheckboxPanel(self, settings["checkbox_options"])
        self.file_panel = FiledialogPanel(
            self,
            settings["root"],
            settings.get("default_paths", [])
        )

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.check_panel.grid(row=0, column=0, sticky=tk.NSEW)
        self.file_panel.grid(row=0, column=1, sticky=tk.NSEW)
        self.ctrl_panel.grid(row=1, columnspan=2, sticky=tk.EW)

    def analyse(self, analysis_func, analysis_type="default"):
        """
        Analysis wrapper function to redirect analysis call from GUI
        element to controller (and model) for actual analysis.
        """

        # NOTE this could be changed such that analysis_func (or analysis_wrapper)
        # would be decorator or similar wrapper but currently it is still
        # normal class method.
        analysis_func(
            self.check_panel.get_selections(),
            self.file_panel.get_filepath_list(clear=self.CLEAR_FILEPATHS),
            analysis_type
        )


################################################################################
class ResultPage(tk.Frame):
    """Class to view result page. Usage clarification:
    in __init__ the self (i.e. tk.Frame typed class)
    is a master to all elements in this frame.
    """

    def __init__(self, parent, controller, settings):
        tk.Frame.__init__(self, parent)
        self.LANG = controller.get_lang()
        self.settings = controller.get_settings()# settings
        self.line_counter = 0

        # Title label
        label = tk.Label(
            self,
            text=GUI[self.LANG]["analysis_result"],
            bg=BG_COLOR,
            fg=FONT_COLOR,
            font=LARGE_FONT
        )
        label.pack(padx=PAD, pady=PAD)

        # Result textbox frame
        result_frame = tk.Frame(self, bg=FRAME_COLOR)
        result_frame.pack(fill="both", expand=True, padx=PAD, pady=PAD)
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

        self.result_textbox = tk.Text(
            result_frame,
            font=TEXTBOX_FONT,
            state="disabled",
            height=15
        )
        self.result_textbox.grid(column=0, row=0, pady=PAD, sticky=tk.NSEW)
        scrollbar = ttk.Scrollbar(
            result_frame,
            orient=tk.VERTICAL,
            command=self.result_textbox.yview
        )
        scrollbar.grid(column=1, row=0, sticky=tk.NS, pady=PAD)
        self.result_textbox.configure(yscrollcommand=scrollbar.set)

        # Control buttons
        button_group = tk.Frame(master=self, bg=FRAME_COLOR)
        button_group.pack(side=tk.BOTTOM)

        back_button = ttk.Button(
            button_group,
            text=GUI[self.LANG]["back"],
            command=lambda: parent.show_page(AnalysePage)
        )
        back_button.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=tk.E)

    def set_line_counter(self, counter, update=False):
        if update:
            self.line_counter += counter
        else:
            self.line_counter = counter

    def show_info(self):
        infos = [
            create_msg("NOTE_INFO", lang=self.LANG),
            create_msg("WARNING_INFO", lang=self.LANG),
            create_msg("ERROR_INFO", lang=self.LANG)
        ]
        self.display_result(infos)
        infos.clear()

    def display_result(self, messages, counter=0):
        if not counter:
            counter = self.line_counter
        line_counter = counter

        self.result_textbox.config(state="normal")
        for msg in messages:
            # Text box lines start from 1 therefore add at the beginning
            line_counter += 1
            self.result_textbox.insert(tk.END, f"{msg[0]}\n")
            if len(msg) >= 4:
                s = f"{line_counter}.0 + {msg[2]}c"
                e = f"{line_counter}.0 + {msg[3]}c"
                self.colour_text(msg[1], start=s, end=e)

        self.result_textbox.config(state="disabled")
        self.line_counter = line_counter

    def colour_text(self, tag, start="1.0", end=tk.END):
        textbox = self.result_textbox
        try:
            color = HIGHLIGHT[tag]
        except KeyError:
            color = FONT_COLOR

        textbox.tag_configure(
            tag,
            font=font.Font(textbox, textbox.cget("font")),
            foreground=color
        )
        textbox.tag_add(tag, start, end)

    def clear_result(self):
        """Method to clear results textbox."""

        self.result_textbox.config(state="normal")
        self.result_textbox.delete(1.0, tk.END)
        self.result_textbox.config(state="disabled")

    def show_results(self, line_list):
        """Method to show analysis results in selected output channels."""

        # Last \n is added because of file.write() command doesn't add it.
        content = "\n".join((map(lambda elem: elem[0], line_list))) + "\n"
        if self.settings["console_print"]:
            print(content, end="")

        if self.settings["file_write"]:
            write_file(self.settings["result_path"], content, mode="a")

        if self.settings["GUI_print"]:
            self.display_result(line_list)

################################################################################
class CLI():
    """
    Upcoming class for command line views.
    """

    def __init__(self, lang):
        self.LANG = lang

    def print_error(self, error_code, *args, error_type="error"):
        if error_type == "error":
            print(CLI_ERROR[self.LANG][error_code])

        elif error_type == "conflict":
            print(SETTINGS_CONFLICTS[self.LANG][error_code])

########################################################################
# GUI.py
#
########################################################################
"""GUI controller"""

# Constants
TOOL_NAME = TOOL_NAME


class GUICLASS(tk.Tk):
    """Main class for GUI. Master for every used GUI element. The main
    frame and menubar are inlcuded in the here other GUI elements are
    in view. Works as a MVP model presenter/ MVC model controller.
    """

    def __init__(self, *args, settings={}, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default="icon.ico")  # To change logo icon
        tk.Tk.title(self, TOOL_NAME)

        self.settings = settings
        self.LANG = settings.setdefault("language", "FIN")
        self.cli = CLI(self.LANG)

        # Detect and solve possible settings conflicts
        conflicts = detect_settings_conflicts(settings)
        if conflicts:
            solve_settings_conflicts(conflicts, settings)
            for c in conflicts:
                self.propagate_error_message(c, error_type="conflict")


        self.model = Model(self)
        self.main_frame = MainFrame(self, self.LANG)

    def get_lang(self):
        return self.LANG

    def get_settings(self):
        # Settings are not changed when where asked so no need to send copy.
        return self.settings

    def propagate_error_message(self, error_code, *args, error_type="error"):
        self.cli.print_error(error_code, *args, error_type=error_type)

    def check_selection_validity(self, selections, filepaths):
        valid = True
        if sum(selections.values()) == 0:
            valid = False
            # TODO: Show GUI message of missing analysis selections
            if self.settings.get("console_print"):
                self.propagate_error_message("NO_SELECTIONS")

        if not filepaths:
            valid = False
            # TODO: Show GUI message of missing files
            if self.settings.get("console_print"):
                self.propagate_error_message("NO_FILES")
        return valid

    def tkvar_2_var(self, tk_vars, to_type):
        selections = {}
        if(isinstance(tk_vars, dict)):
            selections = dict(tk_vars)
            for key in selections.keys():
                if(to_type == "int"):
                    selections[key] = int(selections[key].get())
        return selections

    def analyse_wrapper(self, selected_analysis, filepaths, analysis_type):
        """
        Method to call when starting analysis. Calls correct functions
        to execute selected analysis type.
        """

        selections = self.tkvar_2_var(selected_analysis, "int")
        if not self.check_selection_validity(selections, filepaths):
            return None

        if analysis_type == "BKTA":
            output_format = "dict"
        else:  # default
            output_format = "list"

        file_structure = directory_crawler(
            filepaths,
            only_leaf_files=self.settings["only_leaf_files"],
            excluded_dirs=self.settings["excluded_directories"],
            excluded_files=self.settings["excluded_files"],
            output_format=output_format
        )

        result_page = self.main_frame.get_page(ResultPage)
        result_page.clear_result()  # Clears previous results

        if analysis_type == "BKTA":
            pass
        else:
            result_page.show_info()  # Init new results with default info
            self.main_frame.show_page(ResultPage)  # Show "result page"

            self.model.default_analyse(
                selections,
                file_structure,
                result_page=result_page
            )
            result_page.set_line_counter(0)

        return None

########################################################################
# ASPA_main.py
#
########################################################################
def main():
    settings = init_settings()
    gui = GUICLASS(settings=settings)
    gui.mainloop()


if(__name__ == "__main__"):
    main()
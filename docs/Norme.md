
<https://softwareengineering.stackexchange.com/questions/308972/python-file-naming-convention>

Quoting https://www.python.org/dev/peps/pep-0008/#package-and-module-names:



Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability. Python packages should also have short, all-lowercase names, although the use of underscores is discouraged.
For classes:

Class names should normally use the CapWords convention.
And function and (local) variable names should be:

lowercase, with words separated by underscores as necessary to improve readability
See this answer for the difference between a module, class and package:

A Python module is simply a Python source file, which can expose classes, functions and global variables.
A Python package is simply a directory of Python module(s).
So PEP 8 tells you that:

modules (filenames) should have short, all-lowercase names, and they can contain underscores;
packages (directories) should have short, all-lowercase names, preferably without underscores;
classes should use the CapWords convention.
PEP 8 tells that names should be short; this answer gives a good overview of what to take into account when creating variable names, which also apply to other names (for classes, packages, etc.):

variable names are not full descriptors;
put details in comments;
too specific name might mean too specific code;
keep short scopes for quick lookup;
spend time thinking about readability.


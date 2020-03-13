#
#			common.py
#
#	Common functions
#

def empty(name, value):
    if 0 == len(value):
        return name + " is empty\n"
    else:
        return ""

def exists(name, dict):
    if name in dict:
        return name + " already exists\n"
    else:
        return ""

def notExists(name, dict):
    if name not in dict:
        return name + " does not exist\n"
    else:
        return ""
        
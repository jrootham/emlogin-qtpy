def empty(name, value):
    """Test for empty value"""
    if 0 == len(value):
        return name + " is empty\n"
    else:
        return ""

def exists(name, dict):
    """Check if name exsts"""
    if name in dict:
        return name + " already exists\n"
    else:
        return ""

def notExists(name, dict):
    """Check if name does not exist"""
    if name not in dict:
        return name + " does not exist\n"
    else:
        return ""
        
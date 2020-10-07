import re

def is_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False   

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False  

def regular_int(data):
    reger = r'^(0|[1-9][0-9]{0,2})$'
    compiled = re.compile(reger)
    return compiled.match(data)

def regular_float(data):
    reger = r'^([1-9]\d*|0)(\.\d+)$'
    compiled = re.compile(reger)
    return compiled.match(data)

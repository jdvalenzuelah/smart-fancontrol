
SPECIAL_CHARS = '`!@#$%^&*()-_+={}|[]\\;\':",.<>?/ '

def scapeStr(str: str) -> str:
    return ''.join([c if c not in SPECIAL_CHARS else f'\{c}' for c in str])

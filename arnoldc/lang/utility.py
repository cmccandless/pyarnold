def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

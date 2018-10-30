from .keywords import KWD


class ArnoldCParseException(BaseException):
    def __init__(self, line_content=None, lineno=None, filename=None,):
        message = KWD.PARSE_ERROR
        details = [str(x) for x in (filename, lineno, line_content) if x]
        if details:
            message += '\n' + ':'.join(details)
        BaseException.__init__(self, message)

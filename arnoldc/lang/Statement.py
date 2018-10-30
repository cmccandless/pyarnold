import logging
import shlex

from .exceptions import ArnoldCParseException
from .keywords import KWD, OPERATORS
from .utility import is_integer

logger = logging.getLogger()


def split_args(line):
    # parts = line.split(' ')
    parts = shlex.split(line)
    for i, p in enumerate(parts):
        if p is None:
            continue
        if p.startswith('@'):
            combo = ' '.join(parts[i:i+2])
            for k, v in KWD.MACRO.all().items():
                if combo == v:
                    parts[i] = '0' if v == '@I LIED' else '1'
                    parts[i + 1] = None
    return [p for p in parts if p]


class Statement(object):
    def __init__(self, line, lineno=None, filename=None):
        self.lineno = lineno
        self.text = line
        self.filename = filename
        self._parse_line(line)

    def err(self):
        return ArnoldCParseException(self.text, self.lineno, self.filename)

    def _parse_line(self, line):
        for k, v in KWD.all().items():
            if k == 'MACRO':
                continue
            if line.startswith(v):
                rem_line = line[len(v):]
                parts = split_args(rem_line)
                nargs = KWD.nargs(v)
                if nargs != '*' and nargs != len(parts):
                    break
                self.keyword_name = k
                self.keyword = v
                self.args = parts
                return True
        raise self.err()

    def __repr__(self):
        return '({}) {} {}'.format(
            self.keyword_name,
            self.keyword,
            ' '.join(self.args)
        )

    def run(self, stack, vars=None):
        if vars is None:
            vars = {}
        logger.debug(repr(self))
        if self.keyword == KWD.DECLARE_INT:
            var_name = self.args[0]
            if is_integer(var_name):
                raise self.err()
            stack.append(var_name)
        elif self.keyword == KWD.SET_INITIAL_VALUE:
            var_value = self.args[0]
            if not is_integer(var_value):
                raise self.err()
            var_name = stack.pop()
            vars[var_name] = var_value
        elif self.keyword == KWD.PRINT:
            value = self.args[0]
            if value in vars:
                value = vars[value]
            print(value)
        elif self.keyword == KWD.ASSIGN_VARIABLE:
            var_name = self.args[0]
            if is_integer(var_name):
                raise self.err()
            vars[var_name]
            stack.append(var_name)
        elif self.keyword == KWD.END_ASSIGN_VARIABLE:
            value = stack.pop()
            var_name = stack.pop()
            vars[var_name] = value
        elif self.keyword == KWD.ADD_VALUE_TO_STACK:
            value = self.args[0]
            if not is_integer(value):
                value = vars[value]
            stack.append(int(value))
        elif self.keyword in OPERATORS:
            operand = self.args[0]
            if not is_integer(operand):
                operand = vars[operand]
            operand = int(operand)
            left = stack.pop()
            stack.append(
                int(OPERATORS[self.keyword](left, operand))
            )
        elif self.keyword == KWD.CALL_METHOD:
            func_name = self.args[0]
            func_args = [
                a if is_integer(a) else vars[a]
                for a in self.args[1:]
            ]
            vars[func_name].run(stack, vars, args=func_args)
        elif self.keyword == KWD.ASSIGN_VARIABLE_FROM_METHOD_CALL:
            var_name = self.args[0]
            vars[var_name]
            stack.append(var_name)
        elif self.keyword == KWD.RETURN:
            value = self.args[0]
            if not is_integer(value):
                value = vars[value]
            return value
        elif self.keyword == KWD.READ_INTEGER:
            value = input()
            if not is_integer(value):
                raise TypeError('input must be an integer')
            var_name = stack.pop()
            vars[var_name] = int(value)
        else:
            logger.error('{} | {}'.format(
                repr(stack),
                repr(vars)
            ))
            raise NotImplementedError(
                '{}:{}:{}'.format(self.filename, self.lineno, self.text)
            )

import logging
import shlex


logging.basicConfig(
    # level=logging.DEBUG,
    level=logging.INFO,
    format='%(message)s',
)
logger = logging.getLogger()
STOP_LOOP = '==%STOP_LOOP%=='


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class SpecialEnum(object):
    @classmethod
    def all(cls):
        return {
            k: v for k, v in cls.__dict__.items()
            if k.isupper() and isinstance(v, str)
        }


class KWD(SpecialEnum):
    class MACRO(SpecialEnum):
        TRUE = '@NO PROBLEMO'
        FALSE = '@I LIED'

    BEGIN_MAIN = "IT'S SHOWTIME"
    END_MAIN = 'YOU HAVE BEEN TERMINATED'
    IF = "BECAUSE I'M GOING TO SAY PLEASE"
    ELSE = 'BULLSHIT'
    END_IF = 'YOU HAVE NO RESPECT FOR LOGIC'
    WHILE = 'STICK AROUND'
    END_WHILE = 'CHILL'
    ADD = 'GET UP'
    SUBTRACT = 'GET DOWN'
    MULTIPLY = "YOU'RE FIRED"
    DIVIDE = 'HE HAD TO SPLIT'
    MODULO = 'I LET HIM GO'
    EQ = 'YOU ARE NOT YOU YOU ARE ME'
    GT = 'LET OFF SOME STEAM BENNET'
    OR = 'CONSIDER THAT A DIVORCE'
    AND = 'KNOCK KNOCK'
    DECLARE_METHOD = 'LISTEN TO ME VERY CAREFULLY'
    NON_VOID_METHOD = 'GIVE THESE PEOPLE AIR'
    METHOD_ARGUMENTS = 'I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE'
    RETURN = "I'LL BE BACK"
    END_METHOD_DECLARATION = 'HASTA LA VISTA, BABY'
    CALL_METHOD = 'DO IT NOW'
    ASSIGN_VARIABLE_FROM_METHOD_CALL = 'GET YOUR ASS TO MARS'
    DECLARE_INT = 'HEY CHRISTMAS TREE'
    SET_INITIAL_VALUE = 'YOU SET US UP'
    PRINT = 'TALK TO THE HAND'
    READ_INTEGER = (
        'I WANT TO ASK YOU A BUNCH OF QUESTIONS AND I WANT TO HAVE THEM '
        'ANSWERED IMMEDIATELY'
    )
    ASSIGN_VARIABLE = 'GET TO THE CHOPPER'
    ADD_VALUE_TO_STACK = 'HERE IS MY INVITATION'
    END_ASSIGN_VARIABLE = 'ENOUGH TALK'
    PARSE_ERROR = 'WHAT THE FUCK DID I DO WRONG'

    @classmethod
    def nargs(cls, keyword):
        if keyword in (cls.CALL_METHOD, cls.PRINT):
            return '*'
        if keyword in {
            cls.BEGIN_MAIN, cls.ELSE, cls.END_ASSIGN_VARIABLE, cls.END_IF,
            cls.END_MAIN, cls.END_METHOD_DECLARATION, cls.NON_VOID_METHOD,
            cls.PARSE_ERROR, cls.END_WHILE,
        }:
            return 0
        return 1


class ArnoldCParseException(BaseException):
    def __init__(self, line_content=None, lineno=None, filename=None,):
        message = KWD.PARSE_ERROR
        details = [str(x) for x in (filename, lineno, line_content) if x]
        if details:
            message += '\n' + ':'.join(details)
        BaseException.__init__(self, message)


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
            vars[var_name] = self.args[0]
        elif self.keyword == KWD.PRINT:
            value = self.args[0]
            if value in vars:
                print(vars[value])
            else:
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
        elif self.keyword == KWD.ADD:
            operand = self.args[0]
            if not is_integer(operand):
                operand = vars[operand]
            stack[-1] += int(operand)
        elif self.keyword == KWD.SUBTRACT:
            operand = self.args[0]
            if not is_integer(operand):
                operand = vars[operand]
            stack[-1] -= int(operand)
        elif self.keyword == KWD.MULTIPLY:
            operand = self.args[0]
            if not is_integer(operand):
                operand = vars[operand]
            stack[-1] *= int(operand)
        elif self.keyword == KWD.DIVIDE:
            operand = self.args[0]
            if not is_integer(operand):
                operand = vars[operand]
            stack[-1] = stack[-1] // int(operand)
        elif self.keyword == KWD.MODULO:
            operand = self.args[0]
            if not is_integer(operand):
                operand = vars[operand]
            stack[-1] %= int(operand)
        elif self.keyword == KWD.EQ:
            operand = self.args[0]
            if not is_integer(operand):
                operand = vars[operand]
            operand = int(operand)
            stack[-1] = 1 if stack[-1] == operand else 0
        elif self.keyword == KWD.GT:
            operand = self.args[0]
            if not is_integer(operand):
                operand = vars[operand]
            operand = int(operand)
            stack[-1] = 1 if stack[-1] > operand else 0
        elif self.keyword == KWD.OR:
            operand = self.args[0]
            if not is_integer(operand):
                operand = vars[operand]
            operand = int(operand)
            stack[-1] |= operand
        elif self.keyword == KWD.AND:
            operand = self.args[0]
            if not is_integer(operand):
                operand = vars[operand]
            operand = int(operand)
            stack[-1] &= operand
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
        else:
            logger.error('{} | {}'.format(
                repr(stack),
                repr(vars)
            ))
            raise NotImplementedError(
                '{}:{}:{}'.format(self.filename, self.lineno, self.text)
            )


class Logic(object):
    instances = 0

    def __init__(self, condition):
        self.index = self.__class__.instances
        self.__class__.instances += 1
        self.condition = condition
        self.text = []

    def _check(self, vars):
        if is_integer(self.condition):
            condition = int(self.condition)
        else:
            if self.condition in vars:
                condition = int(vars[self.condition])
            else:
                raise KeyError(self.condition)
        return condition != 0


class Loop(Logic):
    def run(self, stack, vars):
        local_vars = dict(vars)
        do_return = False
        while self._check(local_vars) and not do_return:
            for statement in self.text:
                ret = statement.run(stack, local_vars)
                if ret is not None:
                    return_var_name = stack.pop()
                    vars[return_var_name] = ret
                    do_return = True
                    break


class Conditional(Logic):
    def __init__(self, condition):
        Logic.__init__(self, condition)
        self.false_text = []
        use_false_block = False  # NOQA

    def run(self, stack, vars):
        local_vars = dict(vars)
        if self._check(local_vars):
            for statement in self.text:
                ret = statement.run(stack, local_vars)
                if ret is not None:
                    return_var_name = stack.pop()
                    vars[return_var_name] = ret
                    break
        else:
            for statement in self.false_text:
                ret = statement.run(stack, local_vars)
                if ret is not None:
                    return_var_name = stack.pop()
                    vars[return_var_name] = ret
                    break


class Function(object):
    def __init__(self, name, lines, params=None, returns_value=False):
        self.name = name
        self.text = lines
        self.params = params or []
        self.returns_value = returns_value

    def run(self, stack, vars, args=None):
        if args is None:
            args = []
        if len(args) < len(self.params):
            raise IndexError(
                'not enough arguments provided to {}'.format(self.name)
            )
        local_vars = dict(vars)
        local_vars.update(zip(self.params, args))
        for statement in self.text:
            ret = statement.run(stack, local_vars)
            if ret is not None:
                return_var_name = stack.pop()
                vars[return_var_name] = ret
                break
        return 0

    def __repr__(self):
        r = '{}({})'.format(self.name, ', '.join(self.params))
        if self.returns_value:
            return 'ret ' + r
        return r


class Program(Function):
    def __init__(self, methods, filename=None):
        self.main = methods.pop('main')
        self.methods = methods
        self.filename = filename

    def run(self):
        stack = []
        vars = dict(self.methods)
        ret = self.main.run(stack, vars=vars, args=None)
        return ret

    def __repr__(self):
        methods = list(self.methods.values())
        methods.insert(0, self.main)
        return '\n'.join(map(repr, methods))


def parse(text, filename=None):
    methods = {}
    params = []
    block = []
    current_func = None
    returns_value = False
    lines = text.split('\n')
    logic_stack = []
    for i, line in enumerate(lines, 1):
        line = line.strip()
        # Blank lines
        if not line:
            continue
        # Comments
        if line.startswith('#') or line.startswith('//'):
            continue
        statement = Statement(line, i, filename)
        if statement.keyword == KWD.BEGIN_MAIN:
            current_func = 'main'
        elif statement.keyword == KWD.DECLARE_METHOD:
            current_func = statement.args[0]
        elif statement.keyword == KWD.METHOD_ARGUMENTS:
            param = statement.args[0]
            params.append(param)
        elif statement.keyword == KWD.NON_VOID_METHOD:
            returns_value = True
        elif statement.keyword in (KWD.END_MAIN, KWD.END_METHOD_DECLARATION):
            methods[current_func] = Function(
                current_func, block, params, returns_value
            )
            current_func = None
            block = []
            params = []
            returns_value = False
        elif statement.keyword == KWD.WHILE:
            loop = Loop(statement.args[0])
            logic_stack.append(loop)
        elif statement.keyword == KWD.IF:
            conditional = Conditional(statement.args[0])
            logic_stack.append(conditional)
        elif statement.keyword == KWD.ELSE:
            logic_stack[-1].use_false_block = True
        elif statement.keyword == KWD.END_IF:
            conditional = logic_stack.pop()
            if logic_stack:
                logic = logic_stack[-1]
                if getattr(logic, 'use_false_block', False):
                    logic.false_text.append(conditional)
                else:
                    logic.text.append(conditional)
            else:
                block.append(conditional)
        elif statement.keyword == KWD.END_WHILE:
            loop = logic_stack.pop()
            if logic_stack:
                logic = logic_stack[-1]
                if getattr(logic, 'use_false_block', False):
                    logic.false_text.append(loop)
                else:
                    logic.text.append(loop)
            else:
                block.append(loop)
        else:
            if logic_stack:
                logic = logic_stack[-1]
                if getattr(logic, 'use_false_block', False):
                    logic_stack[-1].false_text.append(statement)
                else:
                    logic_stack[-1].text.append(statement)
            else:
                block.append(statement)
    if 'main' not in methods:
        raise ArnoldCParseException('no main function found')
    return Program(methods, filename)

import logging

from .lang import (
    Conditional,
    ArnoldCParseException,
    Function,
    KWD,
    Loop,
    Program,
    Statement,
)


logging.basicConfig(
    # level=logging.DEBUG,
    level=logging.INFO,
    format='%(message)s',
)
logger = logging.getLogger()
STOP_LOOP = '==%STOP_LOOP%=='


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

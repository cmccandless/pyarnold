from .utility import is_integer


class LogicBlock(object):
    def __init__(self, condition):
        self.condition = condition
        self.text = []

    def _check(self, vars):
        if is_integer(self.condition):
            condition = self.condition
        else:
            condition = vars[self.condition]
        return int(condition) != 0


class Loop(LogicBlock):
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


class Conditional(LogicBlock):
    def __init__(self, condition):
        LogicBlock.__init__(self, condition)
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

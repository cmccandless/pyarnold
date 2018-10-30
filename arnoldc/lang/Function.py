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

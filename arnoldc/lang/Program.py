class Program(object):
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

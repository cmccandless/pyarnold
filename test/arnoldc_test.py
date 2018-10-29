from contextlib import contextmanager
from io import StringIO
import sys
import unittest

from arnoldc import parse


@contextmanager
def capture():
    old = sys.stdout, sys.stderr
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = old
        for i in range(2):
            out[i] = out[i].getvalue()


class ArnoldCTest(unittest.TestCase):
    def run_prog(self, text, return_code=0):
        prog = parse(text)
        with capture() as out:
            ret = prog.run()
        self.assertEqual(ret, return_code)
        return ret, out[0].strip(), out[1].strip()

    @staticmethod
    def main():
        unittest.main()


if __name__ == '__main__':
    unittest.main()

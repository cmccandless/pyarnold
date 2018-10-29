from ddt import ddt, data, unpack
from inspect import isclass
import operator

from arnoldc.arnoldc import KWD
from .arnoldc_test import ArnoldCTest

OPERATOR_CASES = [
    ('ADD', 1, 2, 3),
    ('ADD', 0, 1, 1),
    ('ADD', 1, 0, 1),
    ('ADD', 3, 8, 11),
    ('SUBTRACT', 1, 2, -1),
    ('SUBTRACT', 0, 1, -1),
    ('SUBTRACT', 1, 0, 1),
    ('SUBTRACT', 8, 3, 5),
    ('SUBTRACT', 17, 9, 8),
    ('MULTIPLY', 1, 1, 1),
    ('MULTIPLY', -1, 1, -1),
    ('MULTIPLY', 1, -1, -1),
    ('MULTIPLY', 0, 1, 0),
    ('MULTIPLY', 1, 0, 0),
    ('MULTIPLY', 7, 8, 56),
    ('DIVIDE', 1, 1, 1),
    ('DIVIDE', -1, 1, -1),
    ('DIVIDE', 1, -1, -1),
    ('DIVIDE', 0, 1, 0),
    ('DIVIDE', 1, 0, ZeroDivisionError),
    ('DIVIDE', 56, 8, 7),
    ('MODULO', 10, 3, 1),
    ('MODULO', 10, 5, 0),
    *(
        (op_name, a, b, op(a, b))
        for op_name, op in (
            ('EQ', lambda x, y: 1 if x == y else 0),
            ('GT', lambda x, y: 1 if x > y else 0),
            ('OR', operator.or_),
            ('AND', operator.and_),
        )
        for a in range(2)
        for b in range(2)
    ),
    *(
        (op_name, t, f, op(a, b))
        for op_name, op in (
            ('EQ', lambda x, y: 1 if x == y else 0),
            ('GT', lambda x, y: 1 if x > y else 0),
            ('OR', operator.or_),
            ('AND', operator.and_),
        )
        for a, t in enumerate(('@I LIED', '@NO PROBLEMO'))
        for b, f in enumerate(('@I LIED', '@NO PROBLEMO'))
    ),
]


class AnnotatedCase(list):
    def __init__(self, seq):
        list.__init__(self, seq)
        setattr(self, '__name__', '_'.join(map(str, seq)))


OPERATOR_CASES = [AnnotatedCase(c) for c in OPERATOR_CASES]


@ddt
class OperatorTest(ArnoldCTest):
    @data(*OPERATOR_CASES)
    @unpack
    def test_operator(self, operator, left, right, expected):
        text = """IT'S SHOWTIME
        HEY CHRISTMAS TREE x
        YOU SET US UP {left}
        GET TO THE CHOPPER x
        HERE IS MY INVITATION x
        {operator} {right}
        ENOUGH TALK
        TALK TO THE HAND x
        YOU HAVE BEEN TERMINATED
        """.format(
            left=left,
            operator=KWD.__dict__[operator],
            right=right,
        )
        if isclass(expected) and issubclass(expected, Exception):
            with self.assertRaises(expected):
                self.run_prog(text)
        else:
            ret, out, err = self.run_prog(text)
            self.assertEqual(out, str(expected))

    @data(*OPERATOR_CASES)
    @unpack
    def test_operator_two_vars(self, operator, left, right, expected):
        text = """IT'S SHOWTIME
        HEY CHRISTMAS TREE x
        YOU SET US UP {left}
        HEY CHRISTMAS TREE y
        YOU SET US UP {right}
        GET TO THE CHOPPER x
        HERE IS MY INVITATION x
        {operator} y
        ENOUGH TALK
        TALK TO THE HAND x
        YOU HAVE BEEN TERMINATED
        """.format(
            left=left,
            operator=KWD.__dict__[operator],
            right=right,
        )
        if isclass(expected) and issubclass(expected, Exception):
            with self.assertRaises(expected):
                self.run_prog(text)
        else:
            ret, out, err = self.run_prog(text)
            self.assertEqual(out, str(expected))


if __name__ == '__main__':
    ArnoldCTest.main()

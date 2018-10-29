from arnoldc import parse, ArnoldCParseException
from .arnoldc_test import ArnoldCTest


class BasicTest(ArnoldCTest):
    def test_error_no_main_function(self):
        with self.assertRaisesRegex(
            ArnoldCParseException,
            '.*no main.*'
        ):
            parse('')

    def test_empty_program(self):
        text = """IT'S SHOWTIME
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '')
        self.assertEqual(err, '')

    def test_hello_world(self):
        text = """IT'S SHOWTIME
        TALK TO THE HAND "Hello World!"
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, 'Hello World!')

    def test_macro_true(self):
        text = """IT'S SHOWTIME
        TALK TO THE HAND @NO PROBLEMO
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '1')

    def test_macro_false(self):
        text = """IT'S SHOWTIME
        TALK TO THE HAND @I LIED
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '0')

    def test_assign_variable(self):
        text = """IT'S SHOWTIME
        HEY CHRISTMAS TREE x
        YOU SET US UP 1
        TALK TO THE HAND x
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '1')


if __name__ == '__main__':
    ArnoldCTest.main()

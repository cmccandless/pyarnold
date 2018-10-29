
from .arnoldc_test import ArnoldCTest


class LogicTest(ArnoldCTest):
    def test_if_true(self):
        text = """IT'S SHOWTIME
        BECAUSE I'M GOING TO SAY PLEASE 1
        TALK TO THE HAND "Hello World!"
        YOU HAVE NO RESPECT FOR LOGIC
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, 'Hello World!')

    def test_if_false(self):
        text = """IT'S SHOWTIME
        BECAUSE I'M GOING TO SAY PLEASE 0
        TALK TO THE HAND "Hello World!"
        YOU HAVE NO RESPECT FOR LOGIC
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '')

    def test_if_else_true(self):
        text = """IT'S SHOWTIME
        BECAUSE I'M GOING TO SAY PLEASE 1
        TALK TO THE HAND "Hello Adam!"
        BULLSHIT
        TALK TO THE HAND "Hello Bob!"
        YOU HAVE NO RESPECT FOR LOGIC
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, 'Hello Adam!')

    def test_if_else_false(self):
        text = """IT'S SHOWTIME
        BECAUSE I'M GOING TO SAY PLEASE 0
        TALK TO THE HAND "Hello Adam!"
        BULLSHIT
        TALK TO THE HAND "Hello Bob!"
        YOU HAVE NO RESPECT FOR LOGIC
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, 'Hello Bob!')

    def test_if_nested(self):
        text = """IT'S SHOWTIME
        BECAUSE I'M GOING TO SAY PLEASE 1
        BECAUSE I'M GOING TO SAY PLEASE 0
        TALK TO THE HAND "Hello Adam!"
        BULLSHIT
        TALK TO THE HAND "Hello Bob!"
        YOU HAVE NO RESPECT FOR LOGIC
        BULLSHIT
        TALK TO THE HAND "Hello Chris!"
        YOU HAVE NO RESPECT FOR LOGIC
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, 'Hello Bob!')

    def test_while(self):
        text = """IT'S SHOWTIME
        HEY CHRISTMAS TREE i
        YOU SET US UP @I LIED
        HEY CHRISTMAS TREE continue
        YOU SET US UP @NO PROBLEMO
        STICK AROUND continue
        TALK TO THE HAND i
        GET TO THE CHOPPER i
        HERE IS MY INVITATION i
        GET UP @NO PROBLEMO
        ENOUGH TALK
        GET TO THE CHOPPER continue
        HERE IS MY INVITATION 10
        LET OFF SOME STEAM BENNET i
        ENOUGH TALK
        CHILL
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '\n'.join('0123456789'))

    def test_while_nested(self):
        text = """IT'S SHOWTIME
        HEY CHRISTMAS TREE i
        YOU SET US UP 0
        HEY CHRISTMAS TREE ci
        YOU SET US UP 1
        STICK AROUND ci
        HEY CHRISTMAS TREE j
        YOU SET US UP 0
        HEY CHRISTMAS TREE cj
        YOU SET US UP 1
        STICK AROUND cj
        TALK TO THE HAND j
        GET TO THE CHOPPER j
        HERE IS MY INVITATION j
        GET UP 1
        ENOUGH TALK
        GET TO THE CHOPPER cj
        HERE IS MY INVITATION 3
        LET OFF SOME STEAM BENNET j
        ENOUGH TALK
        CHILL
        GET TO THE CHOPPER i
        HERE IS MY INVITATION i
        GET UP 1
        ENOUGH TALK
        GET TO THE CHOPPER ci
        HERE IS MY INVITATION 3
        LET OFF SOME STEAM BENNET i
        ENOUGH TALK
        CHILL
        YOU HAVE BEEN TERMINATED
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '\n'.join('012012012'))


if __name__ == '__main__':
    ArnoldCTest.main()

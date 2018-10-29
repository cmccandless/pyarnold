from .arnoldc_test import ArnoldCTest


class MethodTest(ArnoldCTest):
    def test_method(self):
        text = """IT'S SHOWTIME
        DO IT NOW hello
        YOU HAVE BEEN TERMINATED

        LISTEN TO ME VERY CAREFULLY hello
        TALK TO THE HAND "Hello World!"
        HASTA LA VISTA, BABY
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, 'Hello World!')

    def test_method_param(self):
        text = """IT'S SHOWTIME
        DO IT NOW print 2
        YOU HAVE BEEN TERMINATED

        LISTEN TO ME VERY CAREFULLY print
        I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE x
        TALK TO THE HAND x
        HASTA LA VISTA, BABY
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '2')

    def test_method_multiple_params(self):
        text = """IT'S SHOWTIME
        DO IT NOW add 2 4
        YOU HAVE BEEN TERMINATED

        LISTEN TO ME VERY CAREFULLY add
        I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE x
        I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE y
        HEY CHRISTMAS TREE z
        YOU SET US UP 0
        GET TO THE CHOPPER z
        HERE IS MY INVITATION x
        GET UP y
        ENOUGH TALK
        TALK TO THE HAND z
        HASTA LA VISTA, BABY
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '6')

    def test_method_return(self):
        text = """IT'S SHOWTIME
        HEY CHRISTMAS TREE x
        YOU SET US UP 0
        GET YOUR ASS TO MARS x
        DO IT NOW f
        TALK TO THE HAND x
        YOU HAVE BEEN TERMINATED

        LISTEN TO ME VERY CAREFULLY f
        GIVE THESE PEOPLE AIR
        I'LL BE BACK 2
        HASTA LA VISTA, BABY
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '2')

    def test_method_params_return(self):
        text = """IT'S SHOWTIME
        HEY CHRISTMAS TREE x
        YOU SET US UP 3
        GET YOUR ASS TO MARS x
        DO IT NOW square x
        TALK TO THE HAND x
        YOU HAVE BEEN TERMINATED

        LISTEN TO ME VERY CAREFULLY square
        I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE n
        GIVE THESE PEOPLE AIR
        GET TO THE CHOPPER n
        HERE IS MY INVITATION n
        YOU'RE FIRED n
        ENOUGH TALK
        I'LL BE BACK n
        HASTA LA VISTA, BABY
        """
        ret, out, err = self.run_prog(text)
        self.assertEqual(out, '9')


if __name__ == '__main__':
    ArnoldCTest.main()

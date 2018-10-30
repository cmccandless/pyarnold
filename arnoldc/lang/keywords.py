import operator


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
            cls.PARSE_ERROR, cls.END_WHILE, cls.READ_INTEGER
        }:
            return 0
        return 1


OPERATORS = {
    KWD.ADD: operator.add,
    KWD.SUBTRACT: operator.sub,
    KWD.MULTIPLY: operator.mul,
    KWD.DIVIDE: operator.truediv,
    KWD.MODULO: operator.mod,
    KWD.EQ: lambda a, b: 1 if a == b else 0,
    KWD.GT: lambda a, b: 1 if a > b else 0,
    KWD.OR: operator.or_,
    KWD.AND: operator.and_,
}

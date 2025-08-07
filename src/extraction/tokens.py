class Token:
    def __init__(self, page_number, text, type, font=None, size=None, line=None, start=None, end=None) -> None:
        self.page_number = page_number
        self.text = text
        self.type = type
        self.font = font
        self.size = size
        self.line = line
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'Token{{{self.text}, {self.type}, {self.start}, {self.end}, {self.line}}}'
    
    def __repr__(self) -> str:
        return self.__str__()


class Literals:
    NUMBER = "NUMBER"
    BOLD_ITALIC = "BOLD_ITALIC"
    ITALIC = "ITALIC"
    REGULAR = "REGULAR"

    @staticmethod
    def get_literal_name(text, font):
        try:
            int(text) 
            return Literals.NUMBER
        except:
            # italic is used for the latin words
            if font and font.find("BoldItalicMT") >= 0:
                return Literals.BOLD_ITALIC
            if font and font.find("ItalicMT") >= 0:
                return Literals.ITALIC
            
            return Literals.REGULAR


class SymbolNotFoundError(Exception):
    def __init__(self, value):
        super().__init__(f"Symbol with value {value} not found.")
        self.value = value

class _SymbolsMeta(type):
    def __getitem__(cls, value: int):
        return cls.get_symbol_name(value)

class Symbols(metaclass=_SymbolsMeta):
    EQUALS = 'EQUALS'
    EQUIVALENT = 'EQUIVALENT'
    MINUS = 'MINUS'
    OPEN_SQUARE_BRACKET = 'OPEN_SQUARE_BRACKET'
    CLOSED_SQUARE_BRACKET = 'CLOSED_SQUARE_BRACKET'
    OPEN_BRACKET = 'OPEN_BRACKET'
    CLOSED_BRACKET = 'CLOSED_BRACKET'
    OPEN_DQUOTE = 'OPEN_DQUOTE'
    CLOSED_DQUOTE = 'CLOSED_DQUOTE'
    OPEN_QUOTE = 'OPEN_QUOTE'
    CLOSED_QUOTE = 'CLOSED_QUOTE'
    DASH = 'DASH'
    LDASH = 'LDASH'
    CDOT = 'CDOT'
    PLUS = 'PLUS'
    QUESTION = 'QUESTION'
    COMMA = 'COMMA'
    WSPACE = 'WSPACE'
    EOL = 'EOL'

    __ascii_mapping = {
        61 : 'EQUALS',
        8801 : 'EQUIVALENT',
        8211 : 'MINUS', # name but not synonym
        91 : 'OPEN_SQUARE_BRACKET',
        93 : 'CLOSED_SQUARE_BRACKET',
        40 : 'OPEN_BRACKET',
        41 : 'CLOSED_BRACKET',
        8220 : 'OPEN_DQUOTE',
        8221 : 'CLOSED_DQUOTE',
        8216 : 'OPEN_QUOTE',
        8217 : 'CLOSED_QUOTE',
        45 : 'DASH',
        8212 : 'LDASH',
        9679 : 'CDOT',
        43 : 'PLUS',
        63 : 'QUESTION', 
        44 : 'COMMA',
        32 : 'WSPACE',
        10 : 'EOL'
    }

    @staticmethod
    def get_symbol_name(value):
        try:
            return Symbols.__ascii_mapping[value]
        except KeyError:
            raise SymbolNotFoundError(value)


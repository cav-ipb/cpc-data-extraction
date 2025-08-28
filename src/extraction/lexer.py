import pdfplumber
from .tokens import *


def chars_from_pages(file, start_page, end_page):
    chars = []

    with pdfplumber.open(file) as pdf:
        for i in range(start_page, end_page + 1):
            page = pdf.pages[i]
            chars += page.chars

    return chars


def get_tokens(stream):

    tokens = []
    text = ''
    last_font = None
    last_size = None
    last_pos = None
    last_page = None
    start = None

    for i, char in enumerate(stream):

        # discard page header and footer
        if 55 > char['y0'] or char['y0'] > 750:
            continue

        if last_page and last_page < char['page_number']:
            tokens.append(Token(last_page, Symbols.EOL, Symbols.EOL, None, None, tokens[-1].line))

        try:
            typex = Symbols[ord(char['text'])] 
            # print(typex)
            if text:
                typey = Literals.get_literal_name(text, font=last_font)

                # check if the line changed by comparing the y coordinate with the previous token
                if len(tokens) > 0 and (tokens[-1].line > last_pos or last_pos > tokens[-1].line + 100) :
                    tokens.append(Token(last_page, Symbols.EOL, Symbols.EOL, None, None, tokens[-1].line))

                # save the token that it was being parse
                tokens.append(Token(last_page, text, typey, last_font, last_size, char['y1'], start, i))

            # change if the symbol changed line with respect to the previous token
            if tokens and (tokens[-1].line > char['y1'] or char['y1'] > tokens[-1].line + 100):
                tokens.append(Token(last_page, Symbols.EOL, Symbols.EOL, None, None, tokens[-1].line))
            
            # append the symbol
            tokens.append(Token(last_page, char['text'], typex, char['fontname'], last_size, char['y1'], i, i))

            text = ''
            last_font = None
            last_pos = char['y1']
            last_page = char['page_number']
            start = None

        except SymbolNotFoundError:
            text += char['text']
            last_font = char['fontname'] if char['fontname'] else last_font
            last_size = char['size']
            last_pos = char['y1']
            last_page = char['page_number']
            if not start:
                start = i
        
    return tokens
from .tokens import *

def parse_index(tokens : list[Token]): 
    open = False
    entries = []
    entry = []
    for token in tokens:
        if open:
            entry.append(token)
            if token.type == Literals.NUMBER:
                entries.append([x for x in entry])
                open = False
        elif (token.type == Literals.BOLD_ITALIC or token.type == Symbols.OPEN_SQUARE_BRACKET):
            entry = [token]
            open = True
        else:
            continue
    return entries


class Sections:
    NAME = 'name'
    HABIT = 'habit'
    DISTRIBUTION = 'distribution'
    FORMATION = 'formation'
    EXCLUDED = 'excluded'
    DISCUSSION = 'discussion'
    DISCUSSION1 = 'discussion1'
    DISCUSSION2 = 'discussion2'
    FORMULA = 'formula'

    lookaheads = {
        "hábito:": HABIT,
        "distribución:" : DISTRIBUTION,
        "taxón": EXCLUDED,
        "formaciones": FORMATION,
        "discusión:": DISCUSSION,
        "discusión": DISCUSSION1,
        "fórmula": FORMULA
    }

    @staticmethod
    def parse_section(tokens, token, i):
        try:
            section = Sections.lookaheads[token.text.lower()]

            if section in [Sections.EXCLUDED, Sections.DISCUSSION1, Sections.FORMATION,  Sections.FORMULA] and i+2 >= len(tokens):
                return None

            if section == Sections.EXCLUDED and tokens[i+2].text.lower() != 'excluido:': # match taxón excluido:
                return None
            
            if section == Sections.FORMATION and tokens[i+2].text.lower() != 'vegetales:':
                return None

            if section == Sections.FORMULA and tokens[i+2].text.lower() != 'híbrida:':
                return None
            
            if section == Sections.DISCUSSION1:

                if tokens[i+2].text.lower() == 'i:':
                    return Sections.DISCUSSION1
                
                if tokens[i+2].text.lower() == 'ii:':
                    return Sections.DISCUSSION2
            
            return section
        except KeyError:
            return None
        


def get_plants(tokens):

    plants = []
    last_type = Symbols.EOL
    plant = {}

    section = None
    text = ''
    eol_count = 0

    for i in range(len(tokens)):
        token = tokens[i]

        if token.type == Symbols.EOL:
            eol_count += 1
            last_type = Symbols.EOL
            text += '\n'
            continue

        # plant sections end with Reference section
        if token.text == 'Referencias' and token.font.find('Bold'):
            break

        if last_type == Symbols.EOL: # in order to recognize sections we need to match an EOL first
            if Sections.parse_section(tokens, token, i) is not None: # matched a new section that starts so in any case I need to save the results of the previous one
                
                plant[section] = text
                section = Sections.parse_section(tokens, token, i)
                text = token.text

            elif token.type == Symbols.WSPACE: # if it didn't match the beginning of a new section then 
                continue

            elif section == Sections.NAME:
                text += token.text

            elif section != Sections.NAME and (section not in [Sections.DISCUSSION, Sections.DISCUSSION1, Sections.DISCUSSION2] or eol_count > 1) and (token.type == Literals.BOLD_ITALIC or (token.type == Symbols.OPEN_SQUARE_BRACKET and tokens[i + 1].type == Literals.BOLD_ITALIC)):
                
                if section:
                    plant[section] = text
                if plant:
                    plants.append(plant)

                plant = {'page_number': token.page_number}
                section = Sections.NAME
                text = token.text

            elif section is None:
                continue

            else:
                text += token.text
            
            last_type = token.type
        else:
            text += token.text
            
            last_type = token.type
        
        if token.type not in [Symbols.EOL, Symbols.WSPACE]:
            eol_count = 0

    if section:
        plant[section] = text
    if plant:
        plants.append(plant)

    return plants

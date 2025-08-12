import pandas as pd

formations_es = [
    'bosque nublado',
    'bosque pluvial de baja altitud',
    'bosque pluvial montano',
    'bosque pluvial',
    'bosque siempreverde mesófilo',
    'bosque siempreverde microfilo',
    'bosque siempreverde',
    'bosque semideciduo mesófilo',
    'bosque semideciduo microfilo',
    'bosque semideciduo',
    'bosque de ciénaga',
    'bosque de galería',
    'bosque de mangles',
    'bosque de pinos de llanuras',
    'bosque de pinos montano',
    'bosque de pinos',
    'matorral xeromorfo costero y subcostero',
    'matorral xeromorfo espinoso sobre serpentina',
    'matorral xeromorfo subespinoso sobre serpentina',
    'matorral montano',
    'comunidades acuáticas de agua dulce', 
    'herbazal de orillas de arroyos y ríos',
    'herbazal de ciénaga y pantano',
    'comunidades halófitas',
    'pastos marinos',
    'complejo de vegetación de costa arenosa',
    'complejo de vegetación de costa rocosa',
    'complejo de vegetación de mogotes',
    'bosque secundario',
    'matorral secundario',
    'sabanas seminaturales',
    'sabanas antrópicas',
    'sabanas',
    'vegetación ruderal',
    'vegetación segetal'
]

formations_en = [
    'cloud forest',
    'low altitued rainforest',
    'montane rainforest',
    'rainforests',
    'mesophyllous evergreen forest',
    'microphyllous evergreen forest',
    'evergreen forest',
    'meshophyllous semidecidous forest',
    'microphyllous semidecidous forest',
    'semidecidous forest',
    'swamp forest',
    'gallery forest',
    'mangrove forest',
    'lowland pine forest',
    'montane pine forest',
    'pine forest',
    'coastal and subcoastal xeromorphic thicket',
    'xeromorphic thorny thicket on serpentine',
    'xeromorphic subthorny thicket on serpentine',
    'montane thicket',
    'fresh-water aquatic communities',
    'herbaceous vegetation on banks of streams and rivers',
    'herbaceous formations of swamps and marshes',
    'halophytic communities',
    'marine herbaceous formations',
    'sandy coasts vegetation complex',
    'rocky coasts vegetation complex',
    'mogotes vegetation complex',
    'secondary forest',
    'secondary thicket',
    'seminatural savannas',
    'anthropic savannas',
    'savannas',
    'ruderal vegetation',
    'segetal vegetation'
]

terms_acronyms = {
    'acuáticas': 'Ac',
    'agua': 'Ag',
    'altitud': 'Al',
    'antrópicas': 'Ant',
    'arenosa': 'Ar',
    'arroyos': 'Ay',
    'baja': 'Ba',
    'bosque': 'B',
    'ciénaga': 'Ci',
    'complejo': 'Cp',
    'comunidades': 'Cm',
    'costa': 'C',
    'costero': 'Co',
    'dulce': 'D',
    'espinoso': 'E',
    'galería': 'G',
    'halófitas': 'Ha',
    'herbazal': 'Hb',
    'llanuras': 'L',
    'mangles': 'Man',
    'marinos': 'Ma',
    'matorral': 'Mt',
    'mesófilo': 'Me',
    'microfilo': 'Mi',
    'mogotes': 'Mg',
    'montano': 'Mn',
    'nublado': 'N',
    'orillas': 'O',
    'pantano': 'Pn',
    'pastos': 'Ps',
    'pinos': 'Pi',
    'pluvial': 'Pl',
    'rocosa': 'Ro',
    'ruderal': 'Ru',
    'ríos': 'R',
    'sabanas': 'Sab',
    'secundario': 'Sec',
    'segetal': 'Sgt',
    'semideciduo': 'Sd',
    'seminaturales': 'Sn',
    'serpentina': 'Sp',
    'siempreverde': 'Sv',
    'subcostero': 'Sc',
    'subespinoso': 'Se',
    'vegetación': 'Vg',
    'xeromorfo': 'X'
}


formations_acronyms = []

for f in formations_es:
    a = ""
    for word in f.split(' '):
        try:
            a += terms_acronyms[word]
        except KeyError:
            pass
    formations_acronyms.append(a)


formations_class = ['forests or tree formations'] * 16 + ['thickets or shrub formations'] * 4 + ['herbaceous formations'] * 5 + ['vegetation complex'] * 3 + ['secondary vegetation'] * 7

formations_all = [
    'bosque nublado',
    'bosque pluvial de baja altitud',
    'boque pluvial montano', # error in the book
    'bosque pluvial montano',
    'bosque pluvial',
    'bosque siempreverde mesófilo',
    'bosque siempreverde microfilo',
    'bosqie siempreverde microfilo',
    'bosque bosque siempreverde microfilo', # error in the book
    'bosque siempreverde',
    'bosque semideciduo mesófilo',
    'bosque semideciduo microfilo',
    'bosque semideciduo',
    'bosque de ciénaga',
    'bosque de galería',
    'bosque de mangles',
    'bosque de mangle',
    'bosque de pinos de llanuras',
    'bosque de pinos montano',
    'bosque de pinos submontano',
    'bosque de pinos',
    'matorral xeromorfo costero y subcostero',
    'matorral xeromorfo costero y subcsotero', # error in the book
    'matorral xeromorfo subcostero y subcostero',
    'matorral xeromorfo espinoso sobre serpentina',
    'matorral xeromorfo subespinoso sobre serpentina',
    'matorral montano',
    'comunidades acuáticas de agua dulce', 
    'comunidades acuáticas de aguas dulces', # inconsistency in the book
    'comunidades acuáticas de aguas dulce', # error
    'herbazal de orillas de arroyos y ríos',
    'herbazal de ciénaga y pantano',
    'comunidades halófitas',
    'pastos marinos',
    'complejo de vegetación de costa arenosa',
    'complejo de vegetación costa de arenosa', # error in the book
    'complejo de vegetación de costa rocosa',
    'complejo de vegetación de mogotes',
    'complejo de vegetación de mogote', # error 
    'complejo de vegetacion de mogotes', #error
    'bosque secundario',
    'matorral secundario',
    'matoral secundario', # error
    'sabanas seminaturales',
    'sabanas antrópicas',
    'sábanas antrópicas',
    'sabana antrópica',
    'sabanas',
    'vegetación ruderal',
    'vegetación segetal'
    
]

errors = {
    'boque pluvial montano' :'bosque pluvial montano',
    'bosque bosque siempreverde microfilo' : 'bosque siempreverde microfilo', # error in the book
    'matorral xeromorfo costero y subcsotero': 'matorral xeromorfo costero y subcostero',
    'comunidades acuáticas de aguas dulces' : 'comunidades acuáticas de agua dulce', 
    'complejo de vegetación costa de arenosa' : 'complejo de vegetación de costa arenosa',
    'sabana antrópica':  'sabanas antrópicas',
    'sábanas antrópicas' : 'sabanas antrópicas',
    'complejo de vegetación de mogote': 'complejo de vegetación de mogotes',
    'matorral xeromorfo subcostero y subcostero' : 'matorral xeromorfo costero y subcostero',
    'bosqie siempreverde microfilo': 'bosque siempreverde microfilo',
    'bosque de mangle' : 'bosque de mangles',
    'comunidades acuáticas de aguas dulce' : 'comunidades acuáticas de agua dulce',
    'matoral secundario' : 'matorral secundario',
    'complejo de vegetacion de mogotes' : 'complejo de vegetación de mogotes'
}


assert len(formations_en) ==len(formations_es) == len(formations_class)
formations_table = [{'id': i, 'name_es' : es, 'name_en': en, 'acronym': a, 'classification': cat} for i, (es, en, a, cat) in enumerate(zip(formations_es, formations_en, formations_acronyms, formations_class))]
formations_index = dict([(f,i) for (i,f) in enumerate(formations_es)])

def parse_formations(string:str) -> list[str]:

    temp = string.split(':', 1)[1].lower()
    formations = []
    opar = False
    text = ''
    for c in temp:
        if c == '(':
            opar = True
        if c == ')':
            opar = False
        if c == ',' and not opar:

            for f in formations_all:
                if text.strip(' ').startswith(f) or text.strip(' ').startswith('¿' + f + '?'):
                    formations.append(text)
                    text = ''
                    break
            
            if text:
                formations[-1] = formations[-1] + ',' + text
                text = ''
            
            continue

        text += c
    
    for f in formations_all:
        if text.strip(' ').startswith(f) or text.strip(' ').startswith('¿' + f + '?'):
            formations.append(text)
            text = ''
            break
    
    if text:
        if formations:
            formations[-1] = formations[-1] + ',' + text
        else:
            formations.append(text)
    
    return [x.strip(', ').lower() for x in formations ]


def normalize_formations(formations):
    result = []
    for formation in formations:
        ok = False
        for formation_term in formations_all:

            doubt = formation.startswith('¿') 
            match = formation.startswith(formation_term) if not doubt else formation[1:].startswith(formation_term)

            if match:
                info = formation[len(formation_term):] if not doubt else formation[len(formation_term)+2:]
                if info.startswith('s'):
                    print(formation)
                try:
                    formationid = formations_index[errors[formation_term]]
                except:
                    formationid = formations_index[formation_term]

                result.append({'formationid': formationid, 'doubt': doubt, 'info': info})
                break
    return result
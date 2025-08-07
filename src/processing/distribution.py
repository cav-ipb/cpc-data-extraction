locations_acronyms = [
    "PR",
    "Art",
    "Hab",
    "May",
    "Mat",
    "IJ",
    "VC",
    "Ci",
    "SS",
    "CA",
    "Cam",
    "LT",
    "Ho",
    "Gr",
    "SC",
    "Gu",
    "COc",
    'CCe',
    "COr",
    "Ja",
    "Esp",
    "PRc",
    "Men",
    "Bah",
    "Cay",
    "AmN",
    "AmC",
    "AmS",
    "VM"
]

locations_acronyms_sorted = list(sorted(locations_acronyms, key= lambda x: len(x), reverse=True))

locations_names = [
    "Pinar del Río",
    "Artemisa",
    "La Habana",
    "Mayabeque",
    "Matanzas",
    "Isla de la Juventud",
    "Villa Clara",
    "Cienfuegos",
    "Sancti Spíritus",
    "Ciego de Ávila",
    "Camagüey",
    "Las Tunas",
    "Holguín",
    "Granma",
    "Santiago de Cuba",
    "Guantánamo",
    "Cuba Occidental",
    'Cuba Central',
    "Cuba Oriental",
    "Jamaica",
    "La Española",
    "Puerto Rico",
    "Antillas Menores",
    "Bahamas",
    "Islas Caimán",
    "América del Norte",
    "América Central",
    "América del Sur",
    "Viejo Mundo"
]

locations = [ {'id': i, 'acronym': a, 'name': l} for i, (a, l) in enumerate(zip(locations_acronyms, locations_names))]
locations_index = dict([(a,i) for (i,a) in enumerate(locations_acronyms)])


presence_es = [
    "nativa",
    "endémica",
    "exótica naturalizada",
    "exótica cultivada",
    "exótica subespontánea casual",
    "exótica efímera",
    "exótica escasamente cultivada",
]

presence_mappings = {
    "naturalizada":  "exótica naturalizada",
    "cultivada" : "exótica cultivada",
    "subespontánea casual" :   "exótica subespontánea casual",
    "efímera" : "exótica efímera",
    "escasamente cultivada" :  "exótica escasamente cultivada",
}

presence_all = [
    "nativa",
    "endémica",
    "exótica naturalizada",
    "exótica cultivada",
    "exótica subespontánea casual",
    "exótica efímera",
    "exótica escasamente cultivada",
    "naturalizada",
    "cultivada",
    "subespontánea casual",
    "efímera",
    "escasamente cultivada"
]


def match_item_list(list:list[str], string:str):
    for x in list:
        if string.startswith(x.lower()):
            return x
    return None

def parse_distribution(distribution:str):
    result = []

    temp = distribution.split(':', 1)[1].lower()
    i = 0 
    current_dist = None
    locations = []
    doubt = False
    foreign = False



    while i < len(temp):
        if temp[i] == "¿":
            doubt = True

        if temp[i] == "|":
            for l in locations:
                l['presence'] = current_dist
                result.append(l)
            foreign = True
            locations = []

        location = match_item_list(locations_acronyms_sorted, temp[i:])
        if location:
            if not foreign:
                locations.append({'locationid': locations_index[location], 'doubt': doubt})
            else:
                result.append({'locationid': locations_index[location], 'doubt': doubt, 'presence': None})
            
            i += len(location)
            doubt = False
            continue
        
        presence = match_item_list(presence_all, temp[i:])
        if presence:
            i += len(presence)
            
            try:
                presence = presence_mappings[presence]
            except:
                pass

            for l in locations:
                l['presence'] = current_dist
                result.append(l)
            current_dist = presence
            locations = []
            
            continue

        i += 1
        
    for l in locations:
        l['presence'] = current_dist
        result.append(l)

    
    
    return result
    

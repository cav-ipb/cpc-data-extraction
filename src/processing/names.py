

synonym_types = {
    61 : 'hetero',
    8801 : 'homo',
    8211 : 'false'
}

def parse_names(names):
    accepted_name = None
    synonyms = []
    name = ""
    stype = None
    for c in names:
        try:
            new_type = synonym_types[ord(c)]
           
            if accepted_name:
                synonyms.append({'type': stype, 'name': name.strip()})
            else:
                accepted_name = name.strip()
            
            stype = new_type
            name = ""
        except KeyError:
            name += c

    if stype:
        synonyms.append({'type': stype, 'name': name.strip()})
    else:
        accepted_name = name.strip()
    
    return accepted_name, synonyms

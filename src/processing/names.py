import requests
import json

class IdGenerator:

    def __init__(self):
        self.count = 0

    def next(self):
        self.count += 1
        return self.count

class Synonym:
    def __init__(self, stype, name, doubt):
        self.stype = stype
        self.name = name
        self.doubt = doubt

    def __str__(self):
        return f'Synonym( {self.name} - {self.stype} )'
    
    def __repr__(self):
        return self.__str__()
    

class TaxonName:
    def __init__(self, id:int, fullname:str):
        self.id : int = id
        self.fullname : str = fullname.strip().lstrip('.')
        self.name : str = None
        self.relatedto : int = None
        self.reltype : str = None

    def __str__(self):
        return f'({self.id}): {self.name} - {self.fullname} - {self.relatedto} - {self.reltype}'
    
    def __repr__(self):
        return self.__str__()
    

synonym_types = {
    61 : 'hetero',
    8801 : 'homo',
    8211 : 'false'
}


def _get_synonyms_groups(names:str):
    synonyms = []
    synonyms_group = []
    name = ""
    stype = "accepted"
    doubt = False

    def __add_synonym(stype:str, name:str, doubt:bool):
        clean = name.strip().lstrip('.')
        if clean == 'Ipomoea rubra var. palustris Urb. Ipomoea palustris (Urb.) Urb.':
            synonyms_group.append(Synonym(stype, 'Ipomoea rubra var. palustris Urb.', doubt))
            synonyms_group.append(Synonym('unknown', 'Ipomoea palustris (Urb.) Urb.', doubt))
        elif clean == 'Asimina blainii Griseb. Cananga blainii (Griseb.) Britton':
            synonyms_group.append(Synonym(stype, 'Asimina blainii Griseb.', doubt))
            synonyms_group.append(Synonym('unknown', 'Cananga blainii (Griseb.) Britton', doubt))
        elif clean == 'Fimbristylis ovata (Burm. f.) J. Kern Cyperus caribaeus Pers.':
            synonyms_group.append(Synonym(stype, 'Fimbristylis ovata (Burm. f.) J. Kern', doubt))
            synonyms_group.append(Synonym('unknown', 'Cyperus caribaeus Pers.', doubt))
        else:
            synonyms_group.append(Synonym(stype, clean, doubt))

    i = 0
    while i < len(names):
        c = names[i]
        
        try:
            new_type = synonym_types[ord(c)]

            if name.strip():
                __add_synonym(stype, name, False)
            
            stype = new_type
            name = ""

        except KeyError:

            if c == "\n":
                if i + 1 >= len(names) or synonym_types.get(ord(names[i+1])) is not None:
                    if name.strip():
                        __add_synonym(stype, name, doubt)
                    synonyms.append([s for s in synonyms_group])
                    synonyms_group = []
                    name = ""
                    doubt = False
            elif c == '?':
                if name.strip():
                    synonyms_group.append(Synonym(stype, name.strip().lstrip('.'), doubt))
                name = ""
                doubt = True
            else:
                name += c

        i += 1
    
    return synonyms



def remove_modifiers(name:str):
    name = name.lstrip('[').rstrip(']')
    index = name.find(',')
    if index >= 0:
        return name[:index]
    return name

def remove_non(name:str):
    index = name.find('[non')
    if index >= 0:
        return name[:index], name[index+4:-1]
    return name, None

def fix_name_hybrid(name:str):
    index = name.find('×')
    if index >= 0:
        return name[:index].strip() + ' × ' + name[index+1:]
    return name


def take_error(name:str):
    if name.startswith('“') or name.startswith('‘'):
        index = max(name.find('”'), name.find('’'))
        return name[1:index].strip()
    return name

def replace_error(name:str):
    k = name.find('(sphalm. ')
    if k >= 0:
        name = name[:k] + '(' + name[k+len('(sphalm. '):]

    chunks = name.split(' ')
    cleaned_chunks = []
    error = None
    error_index = -1
    for i, chunk in enumerate(chunks):
        if chunk.startswith('(\'') or chunk.startswith('(‘') or chunk.startswith('(sphalm.'):
            index = max(chunk.find('\''), chunk.find('‘'))
            error = chunk[index+1:-2]
            if error in ['acuñai', 'microphylla', 'acunaeanus']:
                error_index = i
            else:
                error_index = i-1
        else:
            cleaned_chunks.append(chunk)
        
    names = [' '.join(cleaned_chunks)]
    if error_index >= 0:
        cleaned_chunks[error_index] = error
        names.append(' '.join(cleaned_chunks))
    
    return names

def clean_pipeline(name, idgen: IdGenerator) -> list[TaxonName]:
    nameid = idgen.next()
    name, non_name = remove_non(name)

    names = []

    correctName = TaxonName(nameid, name)

    names.append(correctName)


    if non_name is not None:
        non_name_id = idgen.next()
        non_taxon_name = TaxonName(non_name_id, non_name)
        non_taxon_name.relatedto = nameid
        non_taxon_name.reltype = 'earlier homonym'
        names.append(non_taxon_name)

    result = []

    for n in names:

        t = remove_modifiers(n.fullname)
        t = fix_name_hybrid(t)
        t = take_error(t)
        ts = replace_error(t)
        n.name = ts[0]
        result.append(n)
        for o in ts[1:]:
            new_synonym = TaxonName(idgen.next(), o)
            new_synonym.name = o
            new_synonym.relatedto = n.id
            new_synonym.reltype = 'orto error'
            result.append(new_synonym)

    return result


def parse_names(names:str, idgen : IdGenerator):
    result = []
    synonym_groups = _get_synonyms_groups(names)

    accepted_name_id = None
    for i, group in enumerate(synonym_groups):
        group_lead_id = None
        for j, s in enumerate(group):
            cleaned_names = clean_pipeline(s.name, idgen)
            if j > 0:
                cleaned_names[0].relatedto = group_lead_id
                cleaned_names[0].reltype = s.stype
            if j == 0:
                group_lead_id = cleaned_names[0].id
                if i == 0:
                    accepted_name_id = cleaned_names[0].id
                else:
                    cleaned_names[0].relatedto = accepted_name_id
                    cleaned_names[0].reltype = s.stype

            result.extend(cleaned_names)
    return result


def use_name_parser(names):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    request = {
        "names": [n['name'] for n in names],
        "withDetails": True,
        "csv": False
    }

    response = requests.post('http://localhost:80/api/v1/', headers=headers, json=request)

    parser_response = response.json()

    results = []

    for i, result in enumerate(parser_response):
        if not result['parsed']:
            if names[i]['name'] != 'NeoGomez-mazaea shaferi':
                raise Exception('Wrong name')
        else:
            data = {
                'nameid': names[i]['id'],
                'normalized_name': result['normalized'],
                'canonical_name': result['canonical']['full']
            }

            try:
                data['rank'] = result['rank']
            except KeyError:
                data['rank'] = None

            try:
                data['authorship'] = result['authorship']['normalized']
                data['originalAuthorship'] = '|'.join(result['authorship']['originalAuth']['authors'])
                data['combinationAuthorship'] = '|'.join(result['authorship']['combinationAuth']['authors'])
            except KeyError:
                data['authorship'] = None
                data['originalAuthorship'] = None
                data['combinationAuthorship'] = None
        
            results.append(data)
            # raise Exception("name not parsed")
    return results
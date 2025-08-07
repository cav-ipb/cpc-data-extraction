from processing import *
import pandas as pd
import json

raw_path = 'data/raw'
processed_path = 'data/processed'

with open(f'{raw_path}/raw_data.json', 'r') as f:
    data = json.load(f)




c = 0


taxons = []
taxon_synonyms = []
taxon_formations = []
taxon_distributions = []

for family, ts in data.items():

    for taxon in ts:

        name, synonyms = parse_names(taxon['name'])
        formations = normalize_formations(parse_formations(taxon['formation']))
        
        distributions = []
        try:
            distributions = parse_distribution(taxon['distribution'])
        except KeyError:
            pass


        taxons.append({'id': c, 'page_number': taxon['page_number'], 'family': family, 'name': name})
        for s in synonyms:
            s['taxonid'] = c
            taxon_synonyms.append(s)

        if formations:
            for f in formations:
                f['taxonid'] = c
                taxon_formations.append(f)
        
        if distributions:
            for d in distributions:
                d['taxonid'] = c
                taxon_distributions.append(d)
        
        c+=1


taxons_df = pd.DataFrame(taxons)
taxon_synonyms_df = pd.DataFrame(taxon_synonyms)
taxon_formations_df = pd.DataFrame(taxon_formations)
formations_df = pd.DataFrame(formations_table)
taxon_locations_df = pd.DataFrame(taxon_distributions)
locations_df = pd.DataFrame(locations)


taxons_df.to_csv(f'{processed_path}/taxons.tsv', sep='\t', index=False)
taxon_synonyms_df.to_csv(f'{processed_path}/taxons_synonyms.tsv', sep='\t', index=False)
taxon_formations_df.to_csv(f'{processed_path}/taxons_formations.tsv', sep='\t', index=False)
formations_df.to_csv(f'{processed_path}/formations.tsv', sep='\t', index=False)
taxon_locations_df.to_csv(f'{processed_path}/taxons_locations.tsv', sep='\t', index=False)
locations_df.to_csv(f'{processed_path}/locations.tsv', sep='\t', index=False)
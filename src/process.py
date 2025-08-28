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
taxon_names = []
idgen = IdGenerator()

for family, ts in data.items():

    for taxon in ts:

        namesx = parse_names(taxon['name'], idgen)
        formations = normalize_formations(parse_formations(taxon['formation']))
        
        distributions = []
        try:
            distributions = parse_distribution(taxon['distribution'])
        except KeyError:
            pass


        taxons.append({'id': c, 'page_number': taxon['page_number'], 'family': family, 'nameid': namesx[0].id})
        for s in namesx:
            taxon_names.append(s.__dict__)

        if formations:
            for f in formations:
                f['taxonid'] = c
                taxon_formations.append(f)
        
        if distributions:
            for d in distributions:
                d['taxonid'] = c
                taxon_distributions.append(d)
        
        c+=1


chunk_size = 4000
iters = len(taxon_names) // chunk_size + 1
names_details = []

for i in range(iters):
    start = i * chunk_size
    end = start + chunk_size
    if start >= len(taxon_names):
        break
    names_details.extend(use_name_parser(taxon_names[start:min(end, len(taxon_names) - 1)]))



taxons_df = pd.DataFrame(taxons)
taxon_names_df = pd.DataFrame(taxon_names)
names_details_df = pd.DataFrame(names_details)
taxon_formations_df = pd.DataFrame(taxon_formations)
formations_df = pd.DataFrame(formations_table)
taxon_locations_df = pd.DataFrame(taxon_distributions)
locations_df = pd.DataFrame(locations)


taxons_df.to_csv(f'{processed_path}/taxons.tsv', sep='\t', index=False)
taxon_names_df.to_csv(f'{processed_path}/taxons_names.tsv', sep='\t', index=False)
names_details_df.to_csv(f'{processed_path}/names_details.tsv', sep='\t', index=False)
taxon_formations_df.to_csv(f'{processed_path}/taxons_formations.tsv', sep='\t', index=False)
formations_df.to_csv(f'{processed_path}/formations.tsv', sep='\t', index=False)
taxon_locations_df.to_csv(f'{processed_path}/taxons_locations.tsv', sep='\t', index=False)
locations_df.to_csv(f'{processed_path}/locations.tsv', sep='\t', index=False)
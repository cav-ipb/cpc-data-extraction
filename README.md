# A data extraction pipeline for the Catalogue of the Plants of Cuba

A repository with the source code to extract and structure the data from the Catalogue of the Plants of Cuba



## Methods



## Running the scripts



## Results

The data produced by the scripts can be found in the `src/data` directory, there files are divided into two categories:

- `src/data/raw`: The data as it was extracted from the catalogue

  - `index.json` Associates each Family with is initial page in the catalogue

  - `raw_data.json` Stores all the taxons by family found in the catalogue. This file is a dictionary that associates each family with a list of all the taxons of that family found in the book. The taxons have the following schema, some properties are optional and are mapped to each one of the sections of a taxon entry in the book.

    ```
    {
    	name: string, # is the section of the entry where all the taxon names (including synonyms are specified)
    	habit: string, # HÁBITO
    	distribution: string, # DISTRIBUCIÓN
    	formation: string, # FORMACIONES VEGETALES
    	excluded: string, # TAXÓN EXCLUIDO
    	discussion: string, # DISCUSIÓN
    	discussion1: string, # DISCUSIÓN I
    	discussion2: string, # DISCUSIÓN II
    	formula: string # FÓRMULA HÍBRIDA
    }
    ```

    

- `src/data/processed`: A processed version of the data (normalized, standardized)

  - `taxons.tsv`: The taxons extracted, each row represents and entry in the catalogue. The eschema of the table is.

    ```sql
    Taxons(
    	id INT,
    	page_number INT, -- page number in the PDF file (not by book index)
    	family VARCHAR(50),
      name VARCHAR(200), -- accepted name
    )
    ```

  - `locations.tsv`: All locations defined as per the conventions of _Flora de Cuba en Línea_ (pages 6-7)

    ```  sql
    Locations(
    	id INT,
    	acronym VARCHAR(3),
    	name VARCHAR(20)
    )
    ```

  - `formations.tsv`: Contains the vocabulary defined in the Catalogue for the vegetal formations (pages 7-9)

    ```
    Formations(
    	id INT,	
    	name_es VARCHAR(50),
    	name_en VARCHAR(50),
    	classification VARCHAR(50)
    )
    ```

  - `taxons_synonyms.tsv`: Associates each taxon with its synonyms

    ```
    TaxonsSynonyms(
    	taxonid INT REFERENCES Taxons(id),
    	type VARCHAR(6), -- heterotipic synonym, homotipic synonym, false synonym
    	name	
    )
    ```

  - `taxons_locations.tsv`: Associates each taxon with its locations 

    ```
    TaxonsLocations(
    	locationid INT REFERENCES Locations(id)	
    	taxonid INT REFERENCES Taxons(id)
    	doubt	BOOL, -- flags if the formation was enclosed by ¿?
    	presence VARCHAR(20), -- native, endemic, exotic, etc...
    )
    ```

  - `taxons_formations.tsv`: Associates each taxon with its formations, some taxons may not have any known formations

    ```
    TaxonsFormations(
    	formationid	INT REFERENCES Formation(id)
    	taxonid INT REFERENCES Taxon(id)
    	doubt	BOOL, -- flags if the formation was enclosed by ¿?
    	info TEXT -- additional comments for that specific formation
    )
    
    ```

## Legal notice

The repository is released under the MIT license, notice that the book's content are released under the Creative Commons Attribution License 4.0 (CC BY 4.0) and thus the use of any data produced of that work (by this code or any other) must comply with those terms and conditions.

This repository doesn't contain, reproduces or shares any data of the book.

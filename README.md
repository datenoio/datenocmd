# datenocmd
Command-line tool to use with Dateno dataset search engine


## Getting started

1. Install tool with command ```python3 setup.py install```
2. Obtain your Dateno API key at 'https://dateno.io'. Sign in and copy copy your key somethere locally
2. Create YAML config file .dateno.yaml in you working or user directory. Add line: "apikey: your_secret_ket". 

# Commands

## Dataset search

Examples:
- dateno index search 'Atlantic salmon' --headers id,dataset.title,source.name,source.uid --debug --mode results
- dateno index search 'budget' --filters '"source.langs.name"="English";"source.countries.name"="Kyrgyzstan"' --headers id,dataset.title,source.name,source.uid --debug --mode results


Supported modes: 
- raw - raw data as is from the source
- results - only results as table
- facets - only facets distribution, helpful to refine search
- totals - only estimated total results

Additional parameters:
- --headers header_fields - List of fields to be printed is 'results' mode selected. Nested fields separated by ., for example 'dataset.title'
- --debug - Add more debugging output. Warning, API key could be printed during debug
- --format - could be 'json' or 'yaml'. JSON is original, YAML is more human readable
- --output filename - writes results to the file instead of stdout

TBD

## Fetch dataset record

Examples:
- dateno index get 480906e2ae159fcf99037eecc7601d44aeb3c95f2372d98f0eb514acc7a38bc7

## Fetch data catalog metadata

TBD

## Search data catalogs metadata

TBD




# datenocmd
Command-line tool to use with Dateno dataset search engine


## Getting started

1. Install tool with command ```python3 setup.py install``` or ```python3 -m build .```
2. Obtain your Dateno API key at 'https://dateno.io'. Sign in and copy copy your key somethere locally
2. Create YAML config file .dateno.yaml in you working or user directory. Add line: "apikey: your_secret_key". 

# Commands

## Dataset search

Dataset search command is ```dateno index search``` it require *query* argument and several parameters could be added to format output and refine search results.

    # Search keywords "Atlantic salmon" and return table with id, dataset title, source name and source uid. Debug enabled
    $ dateno index search 'Atlantic salmon' --headers id,dataset.title,source.name,source.uid --debug --mode results --output Atlantic_salmon.csv

    # Search keywords "budget" and only in English and only for country Kyrgyzstan and return table with id, dataset title, source name and source uid. Debug enabled
    $ dateno index search 'budget' --filters "source.langs.name"="English";"source.countries.name"="Kyrgyzstan" --headers id,dataset.title,source.name,source.uid --debug --mode results

    # Return total number of available datasets for keyword "budget" and country Kyrgyzstan
    $ dateno index search 'budget' --filters "source.countries.name"="Kyrgyzstan" --mode totals

    # Return facets distribution for keyword "budget" and country Kyrgyzstan
    $ dateno index search 'budget' --filters "source.countries.name"="Kyrgyzstan" --mode facets

    # Search keywords "budget" and only in English and only for country Kyrgyzstan and return table with id, dataset title, source name and source uid with page 2 and 50 records
    $ dateno index search 'budget' --filters "source.countries.name"="Kyrgyzstan" --mode facets --page 2 --per-page 50

Note: Windows users should use single quotes with *filters* argument. Example
```dateno index search 'budget' --filters '"source.countries.name"="Kyrgyzstan"' --mode facets```


Additional parameters:
* --headers header_fields - List of fields to be printed is 'results' mode selected. Nested fields separated by ., for example 'dataset.title'
* --filters filters_text - Text of search filters to be applied, separated by ;. List of filters available from facets distribution
* --debug - Add more debugging output. Warning, API key could be printed during debug
* --format - could be 'json' or 'yaml'. JSON is original, YAML is more human readable
* --output filename - writes results to the file instead of stdout
* --mode mode_name - search output mode: raw, results, facets or totals
* --page number  - set search results page number
* --per_page number - set size of the results page


Supported modes: 
* raw - raw data as is from the source
* results - only results as table
* facets - only facets distribution, helpful to refine search
* totals - only estimated total results


## Fetch dataset record

Returns single dataset entry with links to the all resources

    # Get single record and print it as YAML to stdout
    $ dateno index get 480906e2ae159fcf99037eecc7601d44aeb3c95f2372d98f0eb514acc7a38bc7

    # Get single record and print it as JSON to the record.json file
    $ dateno index get 480906e2ae159fcf99037eecc7601d44aeb3c95f2372d98f0eb514acc7a38bc7 --format json --output record.json

Parameters:
* --debug - Add more debugging output. Warning, API key could be printed during debug
* --format - could be 'json' or 'yaml'. JSON is original, YAML is more human readable
* --output filename - writes results to the file instead of stdout


## Fetch data catalog metadata

Returns single data catalog entry by uid

    # Get data catalog record and print it as YAML to stdout
    $ dateno catalogs get cdi00004185

    # Get data catalog record and print it as JSON to the record.json file
    $ dateno catalogs get cdi00004185 --format json --output record.json

Parameters:
* --debug - Add more debugging output. Warning, API key could be printed during debug
* --format - could be 'json' or 'yaml'. JSON is original, YAML is more human readable
* --output filename - writes results to the file instead of stdout


## Questions

If you have any questions about Dateno command line tool, please add an issue to the repository [issues](https://github.com/datenoio/datenocmd/issues) or write to dateno@dateno.io

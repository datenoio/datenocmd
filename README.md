# DatenoCmd

Welcome to the DatenoCmd repository! This repository contains a command-line interface (CLI) tool designed to work seamlessly with the Dateno dataset search engine.

## Getting Started

Follow these steps to get started with our tool:

1. **Clone the Repository and Set Up the Environment**

    First, clone the repository and set up your environment. You can use `venv`, `conda`, or any other virtual environment manager of your choice.

    ```sh
    git clone git@github.com:datenoio/datenocmd.git
    # Activate your virtual environment
    pip install -r requirements.txt
    python3 setup.py install # or python3 -m build .
    ```

2. **Obtain Your Dateno API Key**

    Visit [Dateno.io](https://dateno.io) to sign in and obtain your API key. Copy the key and store it securely on your local machine.

3. **Create a Configuration File**

    In your working or user directory, create a configuration file named `.dateno.yaml` and add your API key. You can do this with the following command:

    ```sh
    echo "apikey: YOUR_SECRET_KEY" >> .dateno.yaml
    ```

4. **Make Your First Request**

    Now you're ready to make your first request using DatenoCmd.

    ```sh
    dateno index search 'Atlantic salmon' --limit 1 
    ```

Follow the documentation below for more details on available commands and options.

## Commands

There are three available commands:

- Search for datasets
- Fetch a single dataset, which requires a dataset ID
- Fetch metadata of a single catalog (data source), which requires a catalog ID

All commands share the following **common parameters**:

- `--debug`: Add more debugging output. **Warning:** API key could be printed during debug.
- `--format`: Output format, can be `yaml` (default) or `json`. JSON is the original format, YAML is more human-readable.
- `--output filename`: Writes results to the specified file instead of stdout.

### Dataset search

The dataset search command is `dateno index search`. It requires a *query* argument and supports several parameters to format the output and refine search results.

```sh
# Search for "Atlantic salmon" and return a table with id, dataset title, source name, and source uid. Debug mode enabled.
$ dateno index search 'Atlantic salmon' --headers id,dataset.title,source.name,source.uid --debug --mode results --output Atlantic_salmon.csv --limit 5

# Search for "budget" in English for the country Kyrgyzstan and return a table with id, dataset title, source name, and source uid. Debug mode enabled.
$ dateno index search 'budget' --filters "source.langs.name"="English";"source.countries.name"="Kyrgyzstan" --headers id,dataset.title,source.name,source.uid --debug --mode results --limit 5

# Return the total number of available datasets for the keyword "budget" in Kyrgyzstan.
$ dateno index search 'budget' --filters "source.countries.name"="Kyrgyzstan" --mode totals --limit 5

# Return facets distribution for the keyword "budget" in Kyrgyzstan.
$ dateno index search 'budget' --filters "source.countries.name"="Kyrgyzstan" --mode facets --limit 5

# Search for "budget" in English for the country Kyrgyzstan and return a table with id, dataset title, source name, and source uid with page 2 and 50 records.
$ dateno index search 'budget' --filters "source.countries.name"="Kyrgyzstan" --mode facets --page 2 --per-page 50
```

> **Note:** Windows users should use single quotes with the *filters* argument. For example:
> ```dateno index search 'budget' --filters '"source.countries.name"="Kyrgyzstan"' --mode facets --limit 5```

**Additional parameters**:

- `--mode mode_name`: Search output mode: `results` (default), `raw`, `facets`, or `totals`.
- `--headers header_fields`: List of fields to be printed in `--mode results`. Nested fields are separated by a dot (e.g., `dataset.title`).
- `--filters filters_text`: Text of search filters to be applied, separated by semicolons. List of filters available from facets distribution.
- `--page number`: Set the search results page number.
- `--per_page number`: Set the size of the results page.

**Supported `mode`s**:

- `raw`: Raw data as is from the source.
- `results`: Only results as a table.
- `facets`: Only facets distribution, helpful to refine search.
- `totals`: Only estimated total results.

### Fetch dataset record

Returns a single dataset entry with links to all resources.

```sh
# Get a single record and print it as YAML to stdout.
$ dateno index get 480906e2ae159fcf99037eecc7601d44aeb3c95f2372d98f0eb514acc7a38bc7

# Get a single record and print it as JSON to the record.json file.
$ dateno index get 480906e2ae159fcf99037eecc7601d44aeb3c95f2372d98f0eb514acc7a38bc7 --format json --output record.json
```

### Fetch data catalog metadata

Returns a single data catalog entry by uid.

```sh
# Get a data catalog record and print it as YAML to stdout.
$ dateno catalogs get cdi00004185

# Get a data catalog record and print it as JSON to the record.json file.
$ dateno catalogs get cdi00004185 --format json --output record.json
```

## Support

If you have any questions or encounter issues with the Dateno command-line tool, please feel free to:

- Open an issue in the repository [here](https://github.com/datenoio/datenocmd/issues).
- Reach out to us via email at <dateno@dateno.io>.
- [Join](https://discord.com/invite/tydNfp5EY8) the Discord community

## Other Dateno Resources

- [Quick Start Guide](https://docs.dateno.io/docs/quick-start/)
- [API Documentation](https://api.dateno.io/)
- Web Search <https://dateno.io>
- [Your Account](https://my.dateno.io)

# Dateno CLI (dateno-cmd)

Command-line interface for the Dateno APIs.

## Getting Started

1. **Clone and install**

```sh
git clone git@github.com:datenoio/datenocmd.git
cd datenocmd
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

> Optional (use local SDK with your changes):
> ```sh
> pip install -e ../dateno-sdk-python
> ```

2. **Configure API key**

Create `.dateno_cmd.yaml` in the working directory:

```sh
echo "apikey: YOUR_SECRET_KEY" > .dateno_cmd.yaml
```

Alternatively, set `DATENO_APIKEY` in your environment.

3. **Quick sanity check**

```sh
dateno service health
```

Check version:

```sh
dateno --version
```

## Command groups

- `search` — search datasets (query/dsl/similar/facets)
- `raw` — raw dataset entry by id
- `catalogs` — catalog registry (get/list)
- `service` — health check
- `stats` — statistics DB (namespaces, tables, indicators, timeseries, export)

Common flags:

- `--debug` — verbose logging
- `--format yaml|json` — output format
- `--output FILE` — write output to file

Shell completion:

```sh
dateno --install-completion
dateno --show-completion
```

## Examples

### Search

```sh
dateno search query "Atlantic salmon" --limit 5 --mode results
dateno search get 480906e2ae159fcf99037eecc7601d44aeb3c95f2372d98f0eb514acc7a38bc7
dateno search dsl --body '{"query":{"match_all":{}}}' --mode raw
dateno search facets
dateno search facet --key source.catalog_type
dateno search similar --entry-id d0e86b43e4a02053c0690e0375c052325c2b2e036cf9f45ae80d0b98f7c7d5ef --limit 5
```

### Raw

```sh
dateno raw get d0e86b43e4a02053c0690e0375c052325c2b2e036cf9f45ae80d0b98f7c7d5ef
```

### Catalogs

```sh
dateno catalogs get cdi00001616
dateno catalogs list --query environment --limit 10 --offset 0
```

### Stats

```sh
dateno stats ns
dateno stats ns-get ilostat
dateno stats tables ilostat --limit 10
dateno stats table ilostat CCF_XOXR_CUR_RT_A
dateno stats indicators ilostat --limit 10
dateno stats indicator ilostat CLD_TPOP_SEX_AGE_NB
dateno stats ts ilostat --limit 10
dateno stats ts-get ilostat CCF_XOXR_CUR_RT.ABW
dateno stats export-formats
dateno stats export ilostat CCF_XOXR_CUR_RT.ABW --format csv -o /tmp/ts_export.csv
```

## Project structure

```
dateno_cmd/
  cli.py              # root Typer app
  core.py             # compatibility wrapper
  commands/           # command groups (search/raw/catalogs/service/stats)
  services/           # settings + SDK context
  utils/              # shared helpers (errors/io/serialization/search/sdk)
```

## Support

- Issues: https://github.com/datenoio/datenocmd/issues
- Email: <dateno@dateno.io>
- Discord: https://discord.com/invite/tydNfp5EY8

## Other Dateno resources

- https://docs.dateno.io/docs/quick-start/
- https://api.dateno.io/
- https://dateno.io
- https://my.dateno.io

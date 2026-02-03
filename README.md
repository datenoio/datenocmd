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
- `config` — config init/show (local file only)

Common flags:

- `--debug` — verbose logging
- `--format yaml|json` — output format
- `--output FILE` — write output to file
- `--server-url URL` — override API base URL for this command only
- `--timeout-ms N` — override timeout in ms for this command only
- `--retries N` — override retry count for this command only
- `--apikey KEY` — override API key for this command only (may be stored in shell history)

Note: avoid `--apikey` on shared machines or recorded shells; prefer `.dateno_cmd.yaml` or env vars.

Error handling:

- Errors are printed to stderr
- Exit codes: `0` success, `2` user error, `3` network, `4` API, `1` internal
- HTTP 4xx → user error, HTTP 5xx → API error

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

### Config

```sh
dateno config init
dateno config show
```

## Recipes

```sh
# Use a different API base URL (one-off)
dateno --server-url https://api.dateno.io service health

# Save JSON output to file
dateno search query "environment" --mode raw --format json --output /tmp/search.json

# Export a timeseries to CSV
dateno stats export ilostat CCF_XOXR_CUR_RT.ABW --format csv -o /tmp/ts_export.csv
```

## Debug logging

Enable SDK tracing without leaking secrets:

```sh
dateno --debug service health
```

Logs are written to stderr and include request/response metadata only.
Query param `apikey` is redacted.

## FAQ

**Where does the config live?**  
`./.dateno_cmd.yaml` in your current directory. You can also use ENV vars like `DATENO_APIKEY`.

**How do I switch API environments?**  
Use `--server-url` for a one-off, or set `server_url` in `.dateno_cmd.yaml`.

**Why doesn't my YAML override take effect?**  
ENV and `.env` have higher priority than YAML. Use CLI overrides or unset conflicting ENV vars.

## Troubleshooting

**Error: User error (HTTP 4xx)**  
Check IDs/parameters; for example, verify `entry_id` or `catalog_id`.

**Error: Network error**  
Verify `server_url`, network connectivity, and proxies.

**API key is missing**  
Set `DATENO_APIKEY` or create `.dateno_cmd.yaml` with `apikey: ...`.

## Integration and contract tests

These tests hit the live API and are skipped unless required env vars are set.

Required:
- `DATENO_APIKEY`
- `DATENO_SERVER_URL` (optional, defaults to https://api.dateno.io)

Optional (for full coverage):
- `DATENO_TEST_ENTRY_ID`
- `DATENO_TEST_CATALOG_ID`
- `DATENO_TEST_QUERY`

Run:

```sh
pytest -m integration
pytest -m contract
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

# Grafana OpenHAB Persistence Data Source

## Introduction

This is simple flask server proof-of-concept implementation of  [Grafana Simple JSON Data Source API](https://github.com/grafana/simple-json-datasource),proxying requests to openHAB persistence REST API.

```text
Grafana (Simple JSON Data Source) <-> flask <-> openHAB REST API
```

## Requirements

Setup assumes linux system with docker. Tested only with fedora linux.

## Preparation

Encrypt secrets (one-time)
```bash
make generate_key
```
Enter your username (login email) and password. The username and password are encrypted in file `secret` while encryption key is stored in `key.key`.


## Usage

Start grafana and flask:
```bash
make start_grafana
make start_flask
```

## Missing features

- aggregation (`intervalMs`)
- support for various item types
- Grafana table format
- proper server
- authentication (pass to upstream)
- any cache

## License

MIT
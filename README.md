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

You can access Grafana at `http://127.0.0.1:3000`. Use `admin:admin` to login.

Follow these configuration steps:

1. Add new Data Source ![Edit data source](doc/add-data-source.png "Edit data source")
2. You can now use `timeserie` type targets in charts: ![Example chart](doc/chart-example.png "Example chart")

## Missing features

- aggregation (`intervalMs`)
- support for various item types
- Grafana table format
- proper server
- authentication (pass to upstream)
- any form of caching
- proper error handling
- ...

## License

MIT
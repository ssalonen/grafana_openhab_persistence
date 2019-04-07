PATH_KEY := $(shell readlink -f key.key)
PATH_SECRET := $(shell readlink -f secret)

.PHONY: start_grafana
start_grafana:
	docker run --rm --network host -e GF_INSTALL_PLUGINS="grafana-simple-json-datasource" --rm -p 3000:3000 grafana/grafana

.PHONY: start_flask
start_flask: build_flask
	docker run --rm --network host --rm -p 5000:5000 flask-proxy

.PHONY: build_flask
build_flask:
	docker build -t flask-proxy .
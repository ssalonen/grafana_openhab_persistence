PATH_KEY := $(shell readlink -f key.key)
PATH_SECRET := $(shell readlink -f secret)

.PHONY: start_grafana
start_grafana:
	docker run --rm --network host -e GF_INSTALL_PLUGINS="grafana-simple-json-datasource" --rm -p 3000:3000 grafana/grafana

.PHONY: start_flask
start_flask: build_flask key.key secret
	docker run --rm --network host --rm -v ${PATH_KEY}:/app/key.key:z -v ${PATH_SECRET}:/app/secret:z -p 5000:5000 flask-proxy

.PHONY: generate_key
generate_key: build_flask key.key secret
	docker run -it --rm --network host --rm -v ${PATH_KEY}:/app/key.key:z -v ${PATH_SECRET}:/app/secret:z -p 5000:5000 flask-proxy python3 generate_key.py

.PHONY: build_flask
build_flask:
	docker build -t flask-proxy .

key.key:
	touch key.key
secret:
	touch secret
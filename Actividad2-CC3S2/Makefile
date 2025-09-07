SHELL := /bin/bash
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
APP := app.py
PORT ?= 8080
MESSAGE ?= "Hola CC3S2"
RELEASE ?= "v1"
HOSTNAME := miapp.local
CERT_DIR := /etc/nginx/certs
NGX_AVAIL := /etc/nginx/sites-available
NGX_ENAB  := /etc/nginx/sites-enabled
NGX_SITE  := $(NGX_AVAIL)/$(HOSTNAME)

.PHONY: prepare run hosts-setup tls-cert nginx check-http check-tls dns-demo check-ports logs-demo clean

prepare:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flask

run:
	PORT=$(PORT) MESSAGE=$(MESSAGE) RELEASE=$(RELEASE) $(PY) $(APP)

hosts-setup:
	@echo "127.0.0.1 $(HOSTNAME)" | sudo tee -a /etc/hosts

tls-cert:
	sudo mkdir -p $(CERT_DIR)
	sudo openssl req -x509 -nodes -newkey rsa:2048 \
	  -keyout $(CERT_DIR)/$(HOSTNAME).key \
	  -out $(CERT_DIR)/$(HOSTNAME).crt \
	  -days 365 \
	  -subj "/CN=$(HOSTNAME)" \
	  -addext "subjectAltName=DNS:$(HOSTNAME)"

nginx:
	sudo cp nginx-miapp.local.conf $(NGX_AVAIL)/$(HOSTNAME)
	-@sudo ln -s $(NGX_AVAIL)/$(HOSTNAME) $(NGX_ENAB)/$(HOSTNAME) 2>/dev/null || true
	sudo nginx -t
	-@sudo systemctl restart nginx || sudo service nginx restart || sudo nginx -s reload

check-http:
	curl -v http://127.0.0.1:$(PORT)/ || true

check-tls:
	curl -k https://$(HOSTNAME)/ || true
	openssl s_client -connect $(HOSTNAME):443 -servername $(HOSTNAME) -brief </dev/null || true

dns-demo:
	dig +short $(HOSTNAME) || true
	getent hosts $(HOSTNAME) || true
	dig example.com A +ttlunits || true

check-ports:
	ss -ltnp | grep -E ':(443|$(PORT))' || true

logs-demo:
	$(PY) $(APP) | tee imagenes/app-stdout.log

clean:
	-rm -rf $(VENV) imagenes/app-stdout.log
	-@sudo rm -f $(NGX_SITE) $(NGX_ENAB)/$(HOSTNAME)
	-@sudo nginx -t && (sudo systemctl reload nginx || sudo service nginx reload || sudo nginx -s reload) || true

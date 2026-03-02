ifeq ($(OS),Windows_NT)
PYTHON := py -3
BACKEND_PYTHON := venv/Scripts/python.exe
NPM := npm.cmd
else
PYTHON := python3
BACKEND_PYTHON := venv/bin/python3
NPM := npm
endif

.PHONY: dev backend frontend

dev:
	$(PYTHON) scripts/dev_runner.py

backend:
	cd backend && $(BACKEND_PYTHON) app.py

frontend:
	cd frontend && $(NPM) start

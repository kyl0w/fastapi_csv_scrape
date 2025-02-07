# Variáveis
PYTHON = python
VENV = .venv
PACKAGE_NAME = app
UVICORN = uvicorn

venv:
	$(PYTHON) -m venv $(VENV)
	@echo "Ambiente virtual criado. Para ativá-lo, execute: source .venv/bin/activate"

install:
	$(PYTHON) -m pip install --upgrade pip
	pip install -r requirements.txt
	@echo "Dependências instaladas."

run:
	uvicorn $(PACKAGE_NAME).api:app --reload
	@echo "Servidor FastAPI rodando com Uvicorn..."

test:
	pytest app/tests
	@echo "Testes rodando..."

docs:
	$(VENV)/bin/uvicorn $(PACKAGE_NAME).main:app --reload
	@echo "Documentação disponível em: http://127.0.0.1:8000/docs"

clean:
	rm -rf $(VENV)
	@echo "Ambiente virtual excluído."

start-redis:
	docker-compose up -d redis
	@echo "Redis iniciado."

start-postgres:
	docker-compose up -d postgres
	@echo "PostgreSQL iniciado."
	
stop-containers:
	docker-compose down
	@echo "Containers Docker parados."

help:
	@echo "Comandos disponíveis:"
	@echo "  make install          - Instala dependências"
	@echo "  make run              - Inicia o servidor FastAPI com Uvicorn"
	@echo "  make test             - Executa os testes"
	@echo "  make docs             - Inicia a documentação no navegador"
	@echo "  make clean            - Limpa o ambiente virtual"
	@echo "  make start-redis      - Inicia o Redis com Docker"
	@echo "  make start-postgres   - Inicia o PostgreSQL com Docker"
	@echo "  make stop-containers  - Para os containers Docker"

# PdfSplit
Api para quebra de pdfs em arquivos menores.

## Depêndencias

Instalar dependências com: $ pip install -r requirements.txt
Para instalar manualmente os pacotes: $ pip install {packageName}=={packageVersion}

Verificar dependencias do requirements.txt com: pip list
ou pip check {packageName}

## Execução

Swagger: http://localhost:8000/docs

Dentro do diretório \PdfSplit: python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

OU
1) cd app
2) python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

## Configuração pra debug no VS Code:

{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Módulo",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args":[
                "app.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--loop",
                "asyncio"
            ]
        }
    ]
}
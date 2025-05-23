# carteira.py
import json
import os

ARQUIVO_SALDO = "saldo_btc.json"

# Carregar o saldo atual do arquivo
def carregar_saldo():
    if os.path.exists(ARQUIVO_SALDO):
        with open(ARQUIVO_SALDO, "r") as f:
            try:
                dados = json.load(f)
                return float(dados.get("saldo_btc", 0.0))
            except Exception:
                return 0.0
    return 0.0

# Salvar o saldo atual no arquivo
def salvar_saldo(valor):
    with open(ARQUIVO_SALDO, "w") as f:
        json.dump({"saldo_btc": valor}, f, indent=4)

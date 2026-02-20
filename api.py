from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

ARQUIVO = "logins.txt"

# Garante que exista
if not os.path.exists(ARQUIVO):
    open(ARQUIVO, "w", encoding="utf-8").close()

@app.get("/buscar")
def buscar_logins():
    termo = request.args.get("termo", "").lower()
    resultados = []

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        for linha in f.read().splitlines():
            partes = linha.strip().split(":")
            if len(partes) == 3:
                url, login, senha = partes
            elif len(partes) == 4:
                _, url, login, senha = partes
            else:
                continue

            if termo in url.lower():
                resultados.append({"login": login, "senha": senha})

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

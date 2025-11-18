import requests

def consultar_viacep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    if "erro" in data:
        return None
    return {
        "logradouro": data.get("logradouro", "").strip().lower(),
        "bairro": data.get("bairro", "").strip().lower(),
        "cidade": data.get("localidade", "").strip().lower(),
        "uf": data.get("uf", "").strip().lower()
    }

def consultar_brasilapi(cep):
    url = f"https://brasilapi.com.br/api/cep/v1/{cep}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    return {
        "logradouro": data.get("street", "").strip().lower(),
        "bairro": data.get("neighborhood", "").strip().lower(),
        "cidade": data.get("city", "").strip().lower(),
        "uf": data.get("state", "").strip().lower()
    }

def comparar_enderecos(e1, e2):
    iguais = 0
    total = 4
    if e1["logradouro"] == e2["logradouro"]:
        iguais += 1
    if e1["bairro"] == e2["bairro"]:
        iguais += 1
    if e1["cidade"] == e2["cidade"]:
        iguais += 1
    if e1["uf"] == e2["uf"]:
        iguais += 1
    return iguais / total

def validar_cep(cep):
    cep = cep.replace("-", "").strip()
    if not cep.isdigit() or len(cep) != 8:
        return {"status": "erro", "mensagem": "CEP inválido no formato"}

    via = consultar_viacep(cep)
    bra = consultar_brasilapi(cep)

    if via is None and bra is None:
        return {"status": "invalido", "mensagem": "CEP não encontrado"}

    if via is None or bra is None:
        return {"status": "suspeito", "mensagem": "Somente uma API encontrou o CEP"}

    match_score = comparar_enderecos(via, bra)

    if match_score == 1:
        return {"status": "valido", "mensagem": "CEP validado", "dados": via}

    elif match_score >= 0.5:
        return {
            "status": "divergente",
            "mensagem": "CEP encontrado, mas com divergências",
            "viaCEP": via,
            "BrasilAPI": bra
        }

    else:
        return {"status": "invalido", "mensagem": "Dados muito diferentes"}

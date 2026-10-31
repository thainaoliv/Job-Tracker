from datetime import date

# As etapas válidas de uma vaga, na ordem natural do processo.
ETAPAS_VALIDAS = [
    "Candidatada",
    "Em Processo",
    "Proposta",
    "Contratada",
    "Rejeitada",
]

ETAPA_INICIAL = "Candidatada" 

# Os campos que o usuário é obrigado a preencher.
CAMPOS_OBRIGATORIOS = ["empresa", "cargo", "link"]


def validar_vaga(dados):
    """Confere os dados de uma vaga.
    Devolve uma lista de erros. Lista vazia = tudo certo."""
    erros = []

    # Regra 1: campos obrigatórios não podem faltar nem vir vazios.
    for campo in CAMPOS_OBRIGATORIOS:
        valor = dados.get(campo)
        if valor is None or str(valor).strip() == "":
            erros.append(f"O campo '{campo}' é obrigatório.")

    # Regra 2: se veio um status, ele precisa ser uma etapa válida.
    status = dados.get("status")
    if status is not None and status not in ETAPAS_VALIDAS:
        erros.append(f"Status '{status}' não é uma etapa válida.")

    return erros


def preparar_vaga_nova(dados):
    """Recebe os dados do formulário e devolve a vaga pronta pra salvar,
    já com os valores automáticos preenchidos."""
    vaga = dict(dados)  # cópia, pra não alterar o dicionário original

    # Regra 3: toda vaga nova começa na etapa inicial.
    vaga["status"] = ETAPA_INICIAL

    # Regra 4: se não veio data, usa a data de hoje.
    if not vaga.get("data_candidatura"):
        vaga["data_candidatura"] = date.today().isoformat()

    return vaga


def status_valido(status):
    """Diz se um status é uma etapa válida. Usado ao mudar a etapa de uma vaga."""
    return status in ETAPAS_VALIDAS
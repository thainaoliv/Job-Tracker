from fastapi import FastAPI, HTTPException

from banco import supabase
from regras import validar_vaga, preparar_vaga_nova, status_valido

app = FastAPI(title="Rastreador de Vagas")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # libera qualquer origem — ok pra projeto local
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/vagas")
def listar_vagas():
    """Devolve todas as vagas, da mais recente pra mais antiga."""
    resposta = supabase.table("vagas").select("*").order("created_at", desc=True).execute()
    return resposta.data


@app.post("/vagas")
def criar_vaga(dados: dict):
    """Recebe os dados de uma vaga, valida, e salva no banco."""
    # 1. O porteiro confere os dados.
    erros = validar_vaga(dados)
    if erros:
        raise HTTPException(status_code=400, detail=erros)

    # 2. Prepara a vaga (status inicial + data de hoje).
    vaga = preparar_vaga_nova(dados)

    # 3. Salva no banco e devolve a vaga criada (já com o ID).
    resposta = supabase.table("vagas").insert(vaga).execute()
    return resposta.data[0]

@app.patch("/vagas/{vaga_id}")
def atualizar_status(vaga_id: str, dados: dict):
    """Muda a etapa (status) de uma vaga específica."""
    novo_status = dados.get("status")

    # 1. Confere se o status novo é uma etapa válida.
    if not status_valido(novo_status):
        raise HTTPException(status_code=400, detail=f"Status '{novo_status}' não é válido.")

    # 2. Atualiza só a vaga com esse id.
    resposta = supabase.table("vagas").update({"status": novo_status}).eq("id", vaga_id).execute()

    # 3. Se nada voltou, é porque não existe vaga com esse id.
    if not resposta.data:
        raise HTTPException(status_code=404, detail="Vaga não encontrada.")

    return resposta.data[0]


@app.delete("/vagas/{vaga_id}")
def deletar_vaga(vaga_id: str):
    """Deleta uma vaga específica de vez."""
    resposta = supabase.table("vagas").delete().eq("id", vaga_id).execute()

    if not resposta.data:
        raise HTTPException(status_code=404, detail="Vaga não encontrada.")

    return {"mensagem": "Vaga deletada com sucesso.", "id": vaga_id}
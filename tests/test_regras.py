from datetime import date

from regras import (
    validar_vaga,
    preparar_vaga_nova,
    status_valido,
    ETAPA_INICIAL,
)


def test_vaga_completa_passa():
    vaga = {"empresa": "iFood", "cargo": "Analista de dados", "link": "http://x"}
    assert validar_vaga(vaga) == []


def test_vaga_sem_empresa_reprova():
    vaga = {"cargo": "Analista", "link": "http://x"}
    assert len(validar_vaga(vaga)) == 1


def test_vaga_sem_empresa_e_sem_link_tem_dois_erros():
    vaga = {"cargo": "Analista"}
    assert len(validar_vaga(vaga)) == 2


def test_campo_so_com_espacos_nao_vale():
    vaga = {"empresa": "   ", "cargo": "Analista", "link": "http://x"}
    assert len(validar_vaga(vaga)) == 1


def test_status_invalido_reprova():
    vaga = {"empresa": "iFood", "cargo": "Analista", "link": "http://x", "status": "Banana"}
    assert len(validar_vaga(vaga)) == 1


def test_status_valido_passa():
    assert status_valido("Proposta") is True


def test_status_invalido_e_falso():
    assert status_valido("Banana") is False


def test_vaga_nova_comeca_como_candidatada():
    vaga = preparar_vaga_nova({"empresa": "iFood", "cargo": "Analista", "link": "http://x"})
    assert vaga["status"] == ETAPA_INICIAL


def test_vaga_nova_recebe_data_de_hoje():
    vaga = preparar_vaga_nova({"empresa": "iFood", "cargo": "Analista", "link": "http://x"})
    assert vaga["data_candidatura"] == date.today().isoformat()


def test_preparar_nao_altera_o_original():
    original = {"empresa": "iFood", "cargo": "Analista", "link": "http://x"}
    preparar_vaga_nova(original)
    assert "status" not in original
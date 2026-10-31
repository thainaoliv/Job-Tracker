const API = "http://127.0.0.1:8000";

const etapas = [
    "Candidatada",
    "Em Processo",
    "Proposta",
    "Contratada",
    "Rejeitada",
];

function classeStatus(status) {
  if (status === "Candidatada") return "status-candidatada";
  if (status === "Proposta" || status === "Contratada") return "status-proposta";
  if (status === "Rejeitada") return "status-rejeitada";
  return "status-processo";
}

async function carregarVagas() {
  const resposta = await fetch(`${API}/vagas`);
  const vagas = await resposta.json();
  const container = document.getElementById("lista-vagas");

  if (vagas.length === 0) {
    container.innerHTML = `<p class="vazio">Nenhuma vaga cadastrada ainda. Clique em "+ Adicionar candidatura" para começar.</p>`;
    return;
  }

  let html = "";
  for (const vaga of vagas) {
    let opcoes = "";
    for (const etapa of etapas) {
      const selecionado = etapa === vaga.status ? "selected" : "";
      opcoes += `<option value="${etapa}" ${selecionado}>${etapa}</option>`;
    }

    const temNota = vaga.anotacoes && vaga.anotacoes.trim() !== "";
    const iconeNota = temNota
      ? `<button class="btn-icone" onclick="toggleNota('${vaga.id}')" aria-label="Ver anotação">📝</button>`
      : "";
    const blocoNota = temNota
      ? `<div class="nota" id="nota-${vaga.id}" style="display:none;">${vaga.anotacoes}</div>`
      : "";

    html += `
      <div class="cartao">
        <div class="cartao-linha">
          <div class="cartao-info">
            <p class="cartao-empresa">${vaga.empresa}</p>
            <p class="cartao-cargo">${vaga.cargo}</p>
          </div>
          <select class="status ${classeStatus(vaga.status)}" onchange="mudarStatus('${vaga.id}', this.value)">
            ${opcoes}
          </select>
          <a class="link-vaga" href="${vaga.link}" target="_blank">Ver vaga</a>
          <div class="acoes">
            ${iconeNota}
            <button class="btn-icone btn-deletar" onclick="deletarVaga('${vaga.id}')" aria-label="Deletar">🗑️</button>
          </div>
        </div>
        ${blocoNota}
      </div>
    `;
  }

  container.innerHTML = html;
}

function toggleNota(id) {
  const nota = document.getElementById(`nota-${id}`);
  nota.style.display = nota.style.display === "none" ? "block" : "none";
}

async function deletarVaga(id) {
  const confirmou = confirm("Tem certeza que quer deletar esta vaga?");
  if (!confirmou) return;

  await fetch(`${API}/vagas/${id}`, { method: "DELETE" });
  carregarVagas();
}

async function mudarStatus(id, novoStatus) {
  await fetch(`${API}/vagas/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: novoStatus })
  });
  carregarVagas();
}

carregarVagas();

function abrirModal() {
  document.getElementById("msg-erro").textContent = "";
  document.getElementById("overlay").style.display = "flex";
}

function fecharModal() {
  document.getElementById("overlay").style.display = "none";
}

async function salvarVaga() {
  const vaga = {
    empresa: document.getElementById("empresa").value.trim(),
    cargo: document.getElementById("cargo").value.trim(),
    link: document.getElementById("link").value.trim(),
    fonte: document.getElementById("fonte").value,
    anotacoes: document.getElementById("anotacoes").value.trim(),
  };

  if (!vaga.empresa || !vaga.cargo || !vaga.link) {
    document.getElementById("msg-erro").textContent = "Preencha empresa, cargo e link.";
    return;
  }

  const resposta = await fetch(`${API}/vagas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(vaga),
  });

  if (resposta.ok) {
    document.getElementById("empresa").value = "";
    document.getElementById("cargo").value = "";
    document.getElementById("link").value = "";
    document.getElementById("anotacoes").value = "";
    fecharModal();
    carregarVagas();
  } else {
    document.getElementById("msg-erro").textContent = "Erro ao salvar. Tente de novo.";
  }
}
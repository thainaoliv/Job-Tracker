const API = "http://127.0.0.1:8000";

const form = document.getElementById("form-vaga");
const mensagem = document.getElementById("mensagem");

form.addEventListener("submit", async function (evento) {
  evento.preventDefault();

  // 1. Pega o que foi digitado em cada campo.
  const vaga = {
    empresa: document.getElementById("empresa").value.trim(),
    cargo: document.getElementById("cargo").value.trim(),
    link: document.getElementById("link").value.trim(),
    fonte: document.getElementById("fonte").value,
    anotacoes: document.getElementById("anotacoes").value.trim(),
  };

  // 2. Confere os obrigatórios aqui na tela, antes de enviar.
  if (!vaga.empresa || !vaga.cargo || !vaga.link) {
    mensagem.textContent = "Preencha empresa, cargo e link — são obrigatórios.";
    return;
  }

  // 3. Envia pro backend criar a vaga.
  const resposta = await fetch(`${API}/vagas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(vaga),
  });

  // 4. Reage conforme a resposta.
  if (resposta.ok) {
    mensagem.textContent = "Vaga salva com sucesso!";
    form.reset();
  } else {
    mensagem.textContent = "Algo deu errado ao salvar. Tente de novo.";
  }
});
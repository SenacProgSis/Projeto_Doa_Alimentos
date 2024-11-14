document.getElementById("doacaoForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const alimento = document.getElementById("alimento").value;
    const quantidade = document.getElementById("quantidade").value;

    // Verifica se todos os campos foram preenchidos
    if (!nome || !alimento || !quantidade) {
        document.getElementById("resposta").innerHTML = "<p style='color: red;'>Por favor, preencha todos os campos.</p>";
        return;
    }

    // Envia os dados do formulário para o servidor
    fetch("/doar", {
        method: "POST",
        body: new URLSearchParams({
            nome: nome,
            alimento: alimento,
            quantidade: quantidade
        }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "sucesso") {
            document.getElementById("resposta").innerHTML = `<p style='color: green;'>${data.message}</p>`;
        } else {
            document.getElementById("resposta").innerHTML = `<p style='color: red;'>${data.message}</p>`;
        }
    })
    .catch(error => {
        document.getElementById("resposta").innerHTML = "<p style='color: red;'>Erro ao enviar a doação. Tente novamente.</p>";
    });
});
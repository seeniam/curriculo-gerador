const form = document.querySelector("#resume-form");
const button = document.querySelector("#submit-button");
const feedback = document.querySelector("#feedback");

function setFeedback(type, html) {
    feedback.hidden = false;
    feedback.className = `feedback ${type}`;
    feedback.innerHTML = html;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        jobTitle: document.querySelector("#job-title").value.trim(),
        company: document.querySelector("#company").value.trim(),
        description: document.querySelector("#description").value.trim(),
    };

    if (!payload.description) {
        setFeedback("error", "Cole a descricao da vaga antes de gerar o curriculo.");
        return;
    }

    button.disabled = true;
    button.textContent = "Gerando...";
    setFeedback("loading", "Gerando curriculo personalizado...");

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await response.json();

        if (!response.ok || !data.ok) {
            throw new Error(data.error || "Nao foi possivel gerar o curriculo.");
        }

        setFeedback(
            "success",
            `Curriculo gerado com sucesso.<br>` +
                `<strong>${data.pdfName}</strong><br>` +
                `<span>${data.pdfPath}</span><br>` +
                `<a href="${data.downloadUrl}" target="_blank" rel="noopener">Abrir PDF</a>`
        );
    } catch (error) {
        setFeedback("error", error.message || "Erro inesperado ao gerar o curriculo.");
    } finally {
        button.disabled = false;
        button.textContent = "Gerar curriculo";
    }
});

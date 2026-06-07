const form = document.querySelector("#resume-form");
const button = document.querySelector("#submit-button");
const feedback = document.querySelector("#feedback");

function setFeedback(type, html) {
    feedback.hidden = false;
    feedback.className = `feedback ${type}`;
    feedback.innerHTML = html;
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
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
    button.innerHTML = "Gerando...";
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
            `<span class="success-icon" aria-hidden="true">` +
                `<svg viewBox="0 0 24 24"><path d="M20 6L9 17l-5-5"/></svg>` +
            `</span>` +
            `<span class="success-copy">` +
                `<strong class="success-title">Curriculo gerado com sucesso!</strong>` +
                `<strong class="success-file">${escapeHtml(data.pdfName)}</strong>` +
                `<span class="success-path">${escapeHtml(data.pdfPath)}</span>` +
            `</span>` +
            `<a class="success-action" href="${escapeHtml(data.downloadUrl)}" target="_blank" rel="noopener">` +
                `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h9l3 3v15H6z"/><path d="M14 3v4h4"/><path d="M9 14h6"/></svg>` +
                `Abrir PDF` +
            `</a>`
        );
    } catch (error) {
        setFeedback("error", error.message || "Erro inesperado ao gerar o curriculo.");
    } finally {
        button.disabled = false;
        button.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19c5.8-1.2 10.8-6.2 12-12l2-2-1 5 4 3-5 1c-1.5 3.5-4.3 6.3-7.8 7.8l-1 1 .2-3.2L5 19Z"/><path d="M7 15l-4 4M14 6l4 4"/></svg>Gerar curriculo`;
    }
});

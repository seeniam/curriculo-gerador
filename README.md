# AI Tailored CV Generator

An automated script that leverages Google's Gemini AI to perfectly tailor your resume (HTML Master Knowledge Base) to a specific job description.

## 🚀 Features

- Automatically reads your Master Resume (`default.html` / `default_pt.html`).
- Matches your background against a target job description (`vaga_exemplo.md`).
- Selects the best achievements from your history, applies necessary ATS-friendly keywords, and generates a **ready-to-print HTML** perfectly aligned with what recruiters are looking for.
- A virtual "Elite Headhunter" acts as the persona prompting the AI to maintain a professional, metric-driven language without completely fabricating experiences.

## ⚙️ Setup

1. **Install Python:** Ensure you have Python installed on your system.
2. **Get an API Key:** Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and generate a free API key.
3. **Configure Environment:**
   - Copy `.env.example` to a new file named `.env`.
   - Open `.env` and paste your API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

## 📝 Usage

1. **Update your Knowledge Base:** Edit `default.html` (English) and/or `default_pt.html` (Portuguese) with your comprehensive work history. Treat these files as your "data lake" of experiences, including all projects, metrics, and skills you possess.
2. **Set the Target Job:** Create or edit a `.md` file starting with `vaga` or `job` (e.g., `vaga_exemplo.md`) and paste the job description inside it. The script will automatically pick the *most recently modified* markdown file that matches this pattern.
3. **Execute:**
   - On Windows, just double-click `gerar_cv_automatico.bat`.
   - On other systems, run: `python gerador_de_cv.py`.
4. **Result:** A new tailored HTML file will be generated in the same directory (e.g., `Resume_Generated_vaga_exemplo_2026...html`).

### 🤖 Alternative: Using an AI IDE (Antigravity, Cursor, Copilot)

If you prefer not to use the API key directly or run the Python script, you can use the power of modern AI-assisted IDEs:

1. Open this folder in your favorite AI IDE (like **Google Antigravity**, **Cursor**, **GitHub Copilot Workspace**, etc.).
2. You can select your preferred LLM model within the IDE (e.g., Claude 3.5 Sonnet, GPT-4o, Gemini 2.5 Pro).
3. Select or @mention the following files in the chat context:
   - `default.html` (or `default_pt.html`)
   - The job description file (`vaga_exemplo.md`)
   - The persona file (`persona_headhunter_en.md` or `persona_headhunter_pt.md`)
4. Simply prompt the AI: *"Using the selected persona instructions, create a tailored HTML resume based on my master CV for this job description. Generate only the final HTML code."*

## 🖌️ Customizing the AI Behavior

If you want the AI to write with a different tone or focus on other specifics, edit the `persona_headhunter_en.md` or `persona_headhunter_pt.md` files (depending on the language of your job description). This tells the LLM the rules of engagement (e.g., "Don't use emojis", "Always include an ATS keyword section", "Preserve chronological order").

---

### 🖌️  Simple prompt pt-br
@persona_headhunter.md leia suas instruções e aplique-as usando o @default.html e o vaga1.md na pasta raiz


### Simple prompt (English) 📝
@persona_headhunter.md read your instructions and apply them using @default.html and vaga1.md in the repository root
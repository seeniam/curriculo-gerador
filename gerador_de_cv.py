import os
import glob
import time
from dotenv import load_dotenv

# Dependences:
# pip install google-generativeai python-dotenv
import google.generativeai as genai

def get_latest_vaga_file(directory):
    """Encontra o arquivo vaga*.md ou job*.md mais recentemente modificado no diretório."""
    pattern_vaga = os.path.join(directory, 'vaga*.md')
    pattern_job = os.path.join(directory, 'job*.md')
    
    files = glob.glob(pattern_vaga) + glob.glob(pattern_job)
    if not files:
        return None
    # Retorna o arquivo com a maior data de modificação
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def read_file(filepath):
    """Lê o conteúdo de um arquivo em texto."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler {filepath}: {e}")
        return ""

def main():
    # Detecta automaticamente a pasta onde o script está rodando
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("====================================")
    print(" AI Tailored CV Generator           ")
    print("====================================")
    
    # 1. Carregar variáveis de ambiente do arquivo .env (API Key)
    load_dotenv(os.path.join(base_dir, '.env'))
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("\n[!] ERROR: API Key not found!")
        print(f"Please create a '.env' file in {base_dir}")
        print("Add the following line: GEMINI_API_KEY=your_api_key_here")
        print("You can get a free key at: https://aistudio.google.com/app/apikey\n")
        return

    # Configurar API do Gemini
    genai.configure(api_key=api_key)
    
    # Instanciar o modelo. Recomendado: gemini-2.5-flash
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 2. Encontrar a vaga mais recente
    vaga_file = get_latest_vaga_file(base_dir)
    if not vaga_file:
        print(f"No job description file ('vaga*.md' or 'job*.md') found in {base_dir}.")
        return
        
    print(f"-> Latest job description detected: {os.path.basename(vaga_file)}")
    
    # 3. Ler todos os arquivos de contexto
    print("-> Reading knowledge base and persona instructions...")
    persona_en_path = os.path.join(base_dir, 'persona_headhunter_en.md')
    persona_pt_path = os.path.join(base_dir, 'persona_headhunter_pt.md')
    default_en_path = os.path.join(base_dir, 'default.html')
    default_pt_path = os.path.join(base_dir, 'default_pt.html')
    
    persona_en_content = read_file(persona_en_path)
    persona_pt_content = read_file(persona_pt_path)
    default_en_content = read_file(default_en_path)
    default_pt_content = read_file(default_pt_path)
    vaga_content = read_file(vaga_file)
    
    if not all([persona_en_content, persona_pt_content, default_en_content, default_pt_content, vaga_content]):
        print("ERROR: One or more base files (persona, default, or job description) is missing or empty.")
        print("Check if the following files are in the folder:")
        print(" - persona_headhunter_en.md\n - persona_headhunter_pt.md\n - default.html\n - default_pt.html")
        return
        
    # 4. Construir o Prompt Final
    print("-> Preparing prompt for the AI...")
    prompt = f"""
Você é a persona a seguir. USE A VERSÃO EM INGLÊS DA PERSONA SE A VAGA ESTIVER EM INGLÊS, OU A VERSÃO EM PORTUGUÊS SE ESTIVER EM PORTUGUÊS:

===== PERSONA (ENGLISH) =====
{persona_en_content}

===== PERSONA (PORTUGUÊS) =====
{persona_pt_content}

===== KNOWLEDGE BASE: CURRÍCULO BASE (INGLÊS) =====
{default_en_content}

===== KNOWLEDGE BASE: CURRÍCULO BASE (PORTUGUÊS) =====
{default_pt_content}

===== DESCRIÇÃO DA VAGA ALVO =====
{vaga_content}

===== INSTRUÇÕES FINAIS =====
Por favor, com base na vaga acima e nos perfis base fornecidos (se a vaga estiver em inglês, use o currículo em inglês como base para gerar o novo; se estiver em português, use o em português como base preferencial), aplique as instruções da persona.

Gere OBRIGATORIAMENTE APENAS o código HTML limpo resultante final (Currículo e/ou Cover Letter), sem QUALQUER texto explicativo no início ou no fim, sem tags de markdown como ```html e ```. O arquivo resultante deve começar com <!DOCTYPE html> (se for o caso) ou com a primeira tag html da página.
"""

    # 5. Enviar para o LLM
    print("-> Generating tailored Resume via Google Gemini... (please wait)")
    try:
        # Temperature 0.2 para maior aderência às regras
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.2)
        )
        
        # Limpeza preemptiva de tags do markdown
        html_output = response.text.replace("```html\n", "").replace("```html", "").replace("```", "").strip()
        
        # 6. Salvar o resultado
        vaga_name = os.path.basename(vaga_file).replace('.md', '')
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_filename = os.path.join(base_dir, f"Resume_Generated_{vaga_name}_{timestamp}.html")
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_output)
            
        print(f"\n[+] SUCCESS! The tailored resume was generated.")
        print(f"-> Saved as: {output_filename}\n")
        
    except Exception as e:
        print(f"\n[-] An error occurred during Gemini API generation: {str(e)}")

if __name__ == "__main__":
    main()

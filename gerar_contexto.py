import os

# --- CONFIGURAÇÃO: O que ignorar ---
IGNORE_DIRS = {'.git', '__pycache__', 'venv', '.venv', 'env', 'media', 'staticfiles', '.vscode', '.idea'}
IGNORE_FILES = {'db.sqlite3', '.env', 'package-lock.json', 'poetry.lock', 'gerar_contexto.py', 'contexto_projeto.txt'}
ALLOWED_EXTENSIONS = {'.py', '.html', '.css', '.js', '.txt', '.md'}

def should_process(path, name):
    if name in IGNORE_DIRS or name in IGNORE_FILES:
        return False
    return True

def get_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return "[Arquivo binário ou erro de leitura]"

def main():
    output_file = 'contexto_projeto.txt'
    
    with open(output_file, 'w', encoding='utf-8') as out:
        # 1. Cabeçalho
        out.write("=== ESTRUTURA DO PROJETO DJANGO ===\n")
        
        # 2. Desenha a árvore de pastas
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS] # Filtra pastas na hora
            
            level = root.replace('.', '').count(os.sep)
            indent = ' ' * 4 * (level)
            out.write(f"{indent}{os.path.basename(root)}/\n")
            
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if f not in IGNORE_FILES:
                    out.write(f"{subindent}{f}\n")
        
        out.write("\n\n=== CONTEÚDO DOS ARQUIVOS ===\n")
        
        # 3. Copia o conteúdo dos arquivos relevantes
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file in IGNORE_FILES:
                    continue
                
                _, ext = os.path.splitext(file)
                if ext in ALLOWED_EXTENSIONS:
                    filepath = os.path.join(root, file)
                    out.write(f"\n\n--- INICIO DO ARQUIVO: {filepath} ---\n")
                    out.write(get_file_content(filepath))
                    out.write(f"\n--- FIM DO ARQUIVO: {filepath} ---\n")

    print(f"✅ Sucesso! O arquivo '{output_file}' foi gerado na raiz.")

if __name__ == '__main__':
    main()
import os

# Arquivos e pastas que queremos ignorar
IGNORE_DIRS = {'.git', '__pycache__', 'venv', '.venv', 'env', 'media', 'staticfiles', '.vscode'}
IGNORE_FILES = {'db.sqlite3', '.env', 'package-lock.json', 'poetry.lock', 'gerar_contexto.py'}
# Extensões que queremos ler
ALLOWED_EXTENSIONS = {'.py', '.html', '.css', '.js', '.txt', '.md'}

def should_process(path, name):
    # Filtra diretórios e arquivos ignorados
    if name in IGNORE_DIRS or name in IGNORE_FILES:
        return False
    return True

def get_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return "[Erro ao ler arquivo ou arquivo binário]"

def main():
    output_file = 'contexto_projeto.txt'
    
    with open(output_file, 'w', encoding='utf-8') as out:
        # 1. Escreve a estrutura de diretórios (Tree)
        out.write("=== ESTRUTURA DO PROJETO ===\n")
        for root, dirs, files in os.walk('.'):
            # Modifica dirs in-place para pular pastas ignoradas
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            level = root.replace('.', '').count(os.sep)
            indent = ' ' * 4 * (level)
            out.write(f"{indent}{os.path.basename(root)}/\n")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if f not in IGNORE_FILES:
                    out.write(f"{subindent}{f}\n")
        
        out.write("\n\n=== CONTEÚDO DOS ARQUIVOS ===\n")
        
        # 2. Escreve o conteúdo dos arquivos importantes
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file in IGNORE_FILES:
                    continue
                
                _, ext = os.path.splitext(file)
                if ext in ALLOWED_EXTENSIONS:
                    filepath = os.path.join(root, file)
                    out.write(f"\n\n--- ARQUIVO: {filepath} ---\n")
                    out.write(get_file_content(filepath))

    print(f"✅ Contexto gerado com sucesso em: {output_file}")
    print("Agora arraste este arquivo para o chat da IA!")

if __name__ == '__main__':
    main()
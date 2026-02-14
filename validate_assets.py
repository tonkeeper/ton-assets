import os
import yaml
import json
import sys

def validate_yaml_files(directory):
    print(f"Validando arquivos em {directory}...")
    errors = 0
    files_checked = 0
    
    if not os.path.exists(directory):
        print(f"Diretório {directory} não encontrado.")
        return 0, 0

    for filename in os.listdir(directory):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            files_checked += 1
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
            except Exception as e:
                print(f"ERRO em {filename}: {str(e)}")
                errors += 1
                
    return files_checked, errors

if __name__ == "__main__":
    total_files = 0
    total_errors = 0
    
    for folder in ['accounts', 'collections', 'jettons']:
        checked, errs = validate_yaml_files(folder)
        total_files += checked
        total_errors += errs
        
    print(f"\nResumo da Validação:")
    print(f"Arquivos verificados: {total_files}")
    print(f"Erros encontrados: {total_errors}")
    
    if total_errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)

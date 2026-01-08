import sys
import os

# Importa as funções dos seus arquivos criados
from cleaning import processar_relatorio_direto
from filtrar_participantes import filtrar_relatorio_limpo

def executar_pipeline_completo():
    print("="*40)
    print("INICIANDO PROCESSAMENTO DE PRESENÇA")
    print("="*40)

    try:
        # Passo 1: Limpeza (Raw -> Processed)
        print("\nStep 1: Extraindo seção de participantes...")
        processar_relatorio_direto()
        
        # Passo 2: Filtragem e Formatação (Processed -> Final)
        print("\nStep 2: Filtrando duração (>30min) e formatando...")
        filtrar_relatorio_limpo()
        
        print("\n" + "="*40)
        print("PROCESSO CONCLUÍDO COM SUCESSO!")
        print("="*40)
        print("Verifique a pasta: ./data/final/")

    except Exception as e:
        print(f"\nERRO DURANTE A EXECUÇÃO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    executar_pipeline_completo()
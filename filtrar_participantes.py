import pandas as pd
import glob
import os
import re

def converter_para_minutos(texto_duracao):
    """Transforma strings 'Xh Ym Zs' em valor numérico (minutos)."""
    if pd.isna(texto_duracao) or texto_duracao == '':
        return 0.0
    
    h = re.search(r'(\d+)\s*h', str(texto_duracao))
    m = re.search(r'(\d+)\s*m', str(texto_duracao))
    s = re.search(r'(\d+)\s*s', str(texto_duracao))
    
    total_min = 0.0
    if h: total_min += int(h.group(1)) * 60
    if m: total_min += int(m.group(1))
    if s: total_min += int(s.group(1)) / 60
    return total_min

def formatar_completo(minutos_totais):
    """Converte minutos decimais para o formato 'Xh Ym Zs'."""
    total_segundos = int(round(minutos_totais * 60))
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60
    return f"{horas}h {minutos}m {segundos}s"

def filtrar_relatorio_limpo():
    # Caminhos
    diretorio_input = './data/processed/'
    diretorio_output = './data/final/' # Criando uma pasta para o resultado final
    os.makedirs(diretorio_output, exist_ok=True)

    # 1. Localiza o arquivo já limpo
    arquivos = glob.glob(os.path.join(diretorio_input, "limpo_*.csv"))
    if not arquivos:
        print("Nenhum arquivo limpo encontrado em ./data/processed/")
        return
    
    caminho_input = max(arquivos, key=os.path.getctime)
    print(f"Lendo arquivo limpo: {os.path.basename(caminho_input)}")

    # Como já é um CSV padrão, o pandas lê direto
    df = pd.read_csv(caminho_input, encoding='utf-8-sig')

    # 3. Processamento e Filtros
    # Filtra Função e calcula tempo
    if 'Função' in df.columns:
        df = df[df['Função'] == 'Participante'].copy()

    # Usa a coluna de duração original para o cálculo
    coluna_duracao = 'Duração da Reunião' 
    df['Minutos_Float'] = df[coluna_duracao].apply(converter_para_minutos)
    
    # Filtra > 30 minutos
    df_final = df[df['Minutos_Float'] > 30].copy()

    # 4. Formatação de Saída
    df_final['Duração'] = df_final['Minutos_Float'].apply(formatar_completo)
    
    # Retorna apenas Nome e Duração (ajuste 'Nome' se a coluna for 'Nome completo')
    coluna_nome = 'Nome' if 'Nome' in df.columns else 'Nome completo'
    df_resultado = df_final[[coluna_nome, 'Duração']]
    
    # Ordenar por nome para facilitar a conferência
    df_resultado = df_resultado.sort_values(by=coluna_nome)

    # 5. Salvamento
    nome_saida = f"FINAL_{os.path.basename(caminho_input)}"
    caminho_saida = os.path.join(diretorio_output, nome_saida)
    
    df_resultado.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
    
    print(f"Sucesso! Gerado relatório com {len(df_resultado)} pessoas.")
    print(f"Salvo em: {caminho_saida}")

if __name__ == "__main__":
    filtrar_relatorio_limpo()
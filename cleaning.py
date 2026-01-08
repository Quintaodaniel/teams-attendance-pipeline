import pandas as pd
import io
import glob
import os

def processar_relatorio_direto():
    diretorio_raw = './data/raw/'
    diretorio_processed = './data/processed/'
    os.makedirs(diretorio_processed, exist_ok=True)

    # Localiza o arquivo
    arquivos = glob.glob(os.path.join(diretorio_raw, "*.csv"))
    if not arquivos:
        print("Nenhum arquivo encontrado.")
        return

    caminho_input = max(arquivos, key=os.path.getctime)
    nome_original = os.path.basename(caminho_input)
    caminho_output = os.path.join(diretorio_processed, f"limpo_{nome_original}")

    print(f"Processando: {nome_original}")

    # --- LEITURA DO ARQUIVO ---
    linhas = None
    #loop de encoding porque arquivos do Teams variam muito entre UTF-16 e UTF-8
    for enc in ['utf-16', 'utf-8-sig', 'utf-8', 'iso-8859-1']:
        try:
            with open(caminho_input, 'r', encoding=enc) as f:
                linhas = f.readlines()
            break 
        except (UnicodeDecodeError, UnicodeError):
            continue

    if not linhas:
        print("Erro ao ler o arquivo.")
        return

    # --- EXTRAÇÃO DA SEÇÃO ---
    # Encontra onde começa a lista de nomes e onde termina
    inicio = -1
    fim = len(linhas)

    for i, linha in enumerate(linhas):
        if "2. Participantes" in linha:
            inicio = i + 1
        elif "3. Atividades" in linha:
            fim = i
            break

    # Se encontrar a seção, processa; se não, tenta ler o arquivo todo
    if inicio != -1:
        dados_tabela = "".join(linhas[inicio:fim])
    else:
        dados_tabela = "".join(linhas)

    # --- CONVERSÃO PARA PANDAS ---
    try:
        # O Teams usa Tabulação (\t) como padrão em seus CSVs
        df = pd.read_csv(io.StringIO(dados_tabela), sep='\t')
        
        # Limpeza básica: remove linhas totalmente vazias
        df = df.dropna(how='all')

        # Salva o resultado
        df.to_csv(caminho_output, index=False, encoding='utf-8-sig')
        print(f"Sucesso! Salvo em: {caminho_output} ({len(df)} registros)")
        
    except Exception as e:
        print(f"Erro ao processar dados: {e}")

if __name__ == "__main__":
    processar_relatorio_direto()
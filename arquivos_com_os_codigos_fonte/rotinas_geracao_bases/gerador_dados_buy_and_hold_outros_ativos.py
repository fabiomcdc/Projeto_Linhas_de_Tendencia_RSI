# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
#  Eliminando warnings indesejados 
# ---------------------------------------------------------------------

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)



#---------------------------------------------------------------------
# Setando localidade
#---------------------------------------------------------------------

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#---------------------------------------------------------------------
# Setando variáveis fixas
#---------------------------------------------------------------------

indices = { 
    1: "^BVSP",     # Ticker para Ibovespa
    2: "^GSPC",     # Ticker para S&P 500
    3: "^FTSE",     # Ticker para FTSE 100
    4: "^IXIC",     # Ticker para NASDAQ
    5: "PETR4.SA",  # Ticker para Petrobras
    6: "VALE3.SA",  # Ticker para Vale
    7: "ITUB",      # Ticker para Itaú Unibanco
    8: "BRLUSD=X",  # Ticker para BRL
    9: "EURUSD=X",  # Ticker para Euro
    10: "JPYUSD=X",  # Ticker para BRL
    11: "CNYUSD=X",  # Ticker para YUAN
}

# ---------------------------------------------------------------------
#  Faz a consolidação ativo a ativo
# ---------------------------------------------------------------------

ativo_vals = range(1,12)

# Consolidando todos os resultados a partir de base_dados_ativos_simulados ---------------------------------------------------------


# Criação do DataFrame para armazenar os resultados do cenario_validacao para todos os ativos

dados_consolidados_dos_ativo = pd.DataFrame(columns=[
    'Date',
    'Ativo',
    'Cenario',
    'Close',
])

# DataFrame para acumular resultados
resultados = pd.DataFrame(columns=[
    'Ativo', 'Cenario', 'Retorno_Anual_Medio', 'Volatilidade_Anual', 'Sharpe_Ratio'
])

cenario_vals = ['in_sample_1_1x', 'in_sample_2_1x', 'in_sample_3_1x', \
                'out_of_sample_val_1', 'out_of_sample_val_2', \
                'out_of_sample_final_1', 'out_of_sample_final_2']

taxa_livre_risco=0.0

# Criação do DataFrame para armazenar os resultados do cenario_validacao para todos os ativos

for cenario in cenario_vals:

    for ativo in ativo_vals: # aqui começa o loop ativo a ativo

        ticker = indices.get(ativo)
        ticker_clean = ticker.replace("^", "")
        
        folder_path = f'base_dados_outros_ativos/{ticker_clean}'
        file_name = f'{folder_path}/{cenario}_dados.csv'

        print("Carregando  ,", file_name)

        dados_dos_ativo = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")
        # Resetar o índice para que 'Date' vire uma coluna
        dados_dos_ativo = dados_dos_ativo.reset_index()
        dados_dos_ativo['Date'] = pd.to_datetime(dados_dos_ativo['Date'])
        dados_dos_ativo['Close'] = dados_dos_ativo['Close'].astype(float)
        dados_dos_ativo['Ativo'] = ticker_clean
        dados_dos_ativo = dados_dos_ativo.sort_values(['Ativo', 'Date'])

        for _, row in dados_dos_ativo.iterrows():
            nova_linha = {
                'Date': row['Date'],
                'Ativo': ticker_clean,
                'Cenario': cenario,
                'Close': row['Date'],
            }

            # Adicionando a nova linha ao DataFrame
            dados_consolidados_dos_ativo = pd.concat(
                [dados_consolidados_dos_ativo, pd.DataFrame([nova_linha])],
                ignore_index=True
            )

        # Calcular retornos diários somente na coluna 'Close'
        dados_dos_ativo['Retorno_Diario'] = dados_dos_ativo['Close'].pct_change()

        # Cálculo das métricas
        retorno_anual = 100*((1 + dados_dos_ativo['Retorno_Diario'].mean())**252 - 1)
        volatilidade_anual = 100*dados_dos_ativo['Retorno_Diario'].std() * np.sqrt(252)
        sharpe_ratio = (retorno_anual/100 - taxa_livre_risco) / volatilidade_anual/100 if volatilidade_anual != 0 else np.nan

        # Adicionar os resultados ao DataFrame acumulado
        resultados = pd.concat([resultados, pd.DataFrame([{
            'Ativo': ticker_clean,
            'Cenario': cenario,
            'Retorno_Anual_Medio': retorno_anual,
            'Volatilidade_Anual': volatilidade_anual,
            'Sharpe_Ratio': sharpe_ratio
        }])], ignore_index=True)


# ---------------------------------------------------------------------
# Salvar os resultados
# ---------------------------------------------------------------------
folder_path = 'base_dados_outros_ativos/'
file_name_resultado_cenario = f'{folder_path}/resultados.csv'
resultados.to_csv(file_name_resultado_cenario, sep=";", decimal=",", index=False, encoding="utf-8")

folder_path = 'base_dados_outros_ativos/'
file_name_resultado_cenario = f'{folder_path}/resultados_consolidados.csv'
dados_consolidados_dos_ativo.to_csv(file_name_resultado_cenario, sep=";", decimal=",", index=False, encoding="utf-8")
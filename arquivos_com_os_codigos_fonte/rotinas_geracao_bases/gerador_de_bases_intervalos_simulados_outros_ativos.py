# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import yfinance as yf
import os

# ---------------------------------------------------------------------
#  Eliminando warnings indesejados 
# ---------------------------------------------------------------------

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

# ---------------------------------------------------------------------
#  Importando rotinas
# ---------------------------------------------------------------------

from gerador_de_um_cenario import simulacao

#---------------------------------------------------------------------
# Setando localidade
#---------------------------------------------------------------------

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#---------------------------------------------------------------------
# Setando variáveis fixas
#---------------------------------------------------------------------

aplicar_log = False # flag se aplica ou não o log antes de calcular o RSI"

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


ativo_vals = range(1,13)
cenario = 1
cenarios_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")

    for cenario in cenarios_vals: # aqui começa o loop ativo a ativo

        match cenario:

            case 1: # ------------ Bloco in_sample_1_1x ----------------------------------

                start_date = "2000-01-01"
                end_date = "2005-08-19"
                tipo_intervalo = f'in_sample_1_1x'

            case 2: # ------------ Bloco in_sample_2_1x ----------------------------------

                start_date = "2008-01-15"
                end_date = "2013-10-29"
                tipo_intervalo =f'in_sample_2_1x'

            case 3: # ------------ Bloco in_sample_3_1x ----------------------------------

                start_date = "2016-04-29"
                end_date = "2019-09-18"
                tipo_intervalo =f'in_sample_3_1x'

            case 4: # ------------ Bloco in_sample_1_2x  ----------------------------------

                start_date = "2000-01-01"
                end_date = "2005-08-19"
                tipo_intervalo = f'in_sample_1_2x'

            case 5: # ------------ Bloco in_sample_2_2x ----------------------------------

                start_date = "2008-01-15"
                end_date = "2013-10-29"
                tipo_intervalo = f'in_sample_2_2x'

            case 6: # ------------ Bloco in_sample_3_2x ----------------------------------

                start_date = "2016-04-29"
                end_date = "2019-09-18"
                tipo_intervalo = f'in_sample_3_2x'

            case 7: # ------------ Bloco out_of_sample_val_1 ----------------------------------

                start_date = "2005-10-26"
                end_date = "2007-03-02"
                tipo_intervalo = f'out_of_sample_val_1'

            case 8: # ------------ Bloco out_of_sample_val_2 ----------------------------------

                start_date = "2019-03-06"
                end_date = "2021-09-17"
                tipo_intervalo = f'out_of_sample_val_2'

            case 9: # ------------ Bloco out_of_sample_final_1 ----------------------------------

                start_date = "2002-03-05"
                end_date = "2005-10-26"
                tipo_intervalo = f'out_of_sample_final_1'

            case 10: # ------------ Bloco out_of_sample_final_2 ----------------------------------

                start_date = "2021-09-18" 	
                end_date = "2024-11-01"
                tipo_intervalo = f'out_of_sample_final_2'


        # Criando folder -----------------------------------------
                
        folder_path = f'base_dados_outros_ativos/{ticker_clean}'

        # Verifica se o diretório já existe; se não, cria
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Salvando os dados -----------------------------------------

        file_name = f'base_dados_outros_ativos/{ticker_clean}/{tipo_intervalo}_dados.csv'

        if ticker:
            # Importa os dados do Yahoo Finace
            data = yf.download(ticker, start=start_date, end=end_date)
            print(f'Baixando dados de {ticker_clean} para o intervalo {tipo_intervalo}')
            data.to_csv(file_name, sep=";", decimal=",", index=True, encoding="utf-8")

        else:
            print("Índice inválido")
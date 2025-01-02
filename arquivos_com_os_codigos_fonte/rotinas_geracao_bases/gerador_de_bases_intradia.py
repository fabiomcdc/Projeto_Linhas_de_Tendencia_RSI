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

aplicar_log = False # flag se aplica ou não o log antes de calcular o RSI" 2, 6, 31, 24 e 19

indices = {
    2: "MSFT",       # Ticker para Microsoft
    6: "COST",       # Ticker para Costco
    19: "VMC",       # Ticker para Vulcan Materials Company
    24: "AFL",       # Ticker para Aflac
    31: "BAC",       # Ticker para Bank of America
}
ativo_vals = [2, 6, 19, 24, 31]


for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")

    # Criando folder -----------------------------------------
            
    folder_path = f'base_dados_ativos_intradia/{ticker_clean}'

    # Verifica se o diretório já existe; se não, cria
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Salvando os dados -----------------------------------------

    file_name = f'{folder_path}/dados_intradia.csv'

    if ticker:
        # Importa os dados do Yahoo Finace
        data = yf.download(tickers='AAPL', period='5d', interval='1m')
        print(f'Importando dados de {ticker_clean}')
        data.to_csv(file_name, sep=";", decimal=",", index=True, encoding="utf-8")

    else:
        print("Índice inválido")
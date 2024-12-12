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
    1: "CSCO",       # Ticker para Cisco Systems
    2: "MSFT",       # Ticker para Microsoft
    3: "PHM",        # Ticker para PulteGroup
    4: "MAR",        # Ticker para Marriott International
    5: "YUM",        # Ticker para Yum! Brands
    6: "COST",       # Ticker para Costco
    7: "HSY",        # Ticker para Hershey Company (The)
    8: "K",          # Ticker para Kellanova
    9: "HES",        # Ticker para Hess Corporation
    10: "BSX",       # Ticker para Boston Scientific
    11: "CI",        # Ticker para Cigna
    12: "CVS",       # Ticker para CVS Health
    13: "BA",        # Ticker para Boeing
    14: "GE",        # Ticker para GE Aerospace
    15: "WM",        # Ticker para Waste Management
    16: "ADBE",      # Ticker para Adobe Inc.
    17: "AAPL",      # Ticker para Apple Inc.
    18: "HPQ",       # Ticker para HP Inc.
    19: "VMC",       # Ticker para Vulcan Materials Company
    20: "NEM",       # Ticker para Newmont
    21: "AEP",       # Ticker para American Electric Power
    22: "NEE",       # Ticker para NextEra Energy
    23: "CMI",       # Ticker para Cummins Inc.
    24: "AFL",       # Ticker para Aflac
    25: "JNJ",       # Ticker para Johnson & Johnson
    26: "AIG",       # Ticker para American International Group
    27: "LLY",       # Ticker para Eli Lilly and Company
    28: "NOC",       # Ticker para Northrop Grumman
    29: "AES",       # Ticker para AES Corporation
    30: "BEN",       # Ticker para Franklin Resources
    31: "BAC",       # Ticker para Bank of America
    32: "CL",        # Ticker para Colgate-Palmolive
    33: "COF",       # Ticker para Capital One
    34: "MMC",       # Ticker para Marsh & McLennan
    35: "DHR",       # Ticker para Danaher Corporation
    36: "HAS",       # Ticker para Hasbro
    37: "PFE",       # Ticker para Pfizer
    38: "MMM",       # Ticker para 3M
    39: "ED",        # Ticker para Consolidated Edison
    40: "ORCL",      # Ticker para Oracle Corporation
    41: "PNC",       # Ticker para PNC Financial Services
    42: "MU",        # Ticker para Micron Technology
    43: "MCO",       # Ticker para Moody's Corporation
    44: "FDX",       # Ticker para FedEx
    45: "WY",        # Ticker para Weyerhaeuser
    46: "CINF",      # Ticker para Cincinnati Financial
    47: "AEE",       # Ticker para Ameren
    48: "TJX",       # Ticker para TJX Companies
    49: "SO",        # Ticker para Southern Company
    50: "ITW",       # Ticker para Illinois Tool Works
}
ativo_vals = range(1,51)
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
                
        folder_path = f'base_dados_ativos_simulados/{ticker_clean}'

        # Verifica se o diretório já existe; se não, cria
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Salvando os dados -----------------------------------------

        file_name = f'base_dados_ativos_simulados/{ticker_clean}/{tipo_intervalo}_dados.csv'

        if ticker:
            # Importa os dados do Yahoo Finace
            data = yf.download(ticker, start=start_date, end=end_date)
            data.to_csv(file_name, sep=";", decimal=",", index=True, encoding="utf-8")

        else:
            print("Índice inválido")
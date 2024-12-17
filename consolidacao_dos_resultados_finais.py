# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os

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

# ---------------------------------------------------------------------
#  Faz a consolidação ativo a ativo
# ---------------------------------------------------------------------

ativo_vals = range(1,51)

# Criação do DataFrame para armazenar os resultados
resultados_consolidados = pd.DataFrame(columns=[
    'janela_rsi',
    'ordem',
    'lookback',
    'd_max',
    'num_pontos',
    'break_min',
    'ppt',
    'sl',
    'pt',
    'ativo',
    'cenario',
    'return_ann',
    'sharpe_ratio',
    'max_drawdown',
    'trades',
])


for ativo in ativo_vals: # aqui começa o loop ativo a ativo

    ticker = indices.get(ativo)
    ticker_clean = ticker.replace("^", "")
    
    # Definindo os nomes dos arquivos
    
    folder_path = f'simulações_aplicadas_a_ativos - fases validação e final 4/{ticker_clean}'

    file_name1 = f'{folder_path}/{ticker_clean}_[9, 10]_cenario_final_resultados.csv'
    file_name2 = f'{folder_path}/{ticker_clean}_[9, 10]_cenario_final_resultados_notebook.csv'

    # Tentando abrir o primeiro arquivo, caso falhe, abre o segundo
    try:
        with open(file_name1, 'r') as file:
            resultados_do_ativo_df = pd.read_csv(file_name1, sep=";", decimal=",", index_col=0, encoding="utf-8")
            print(f"Abrindo arquivo: {file_name1}")
    except FileNotFoundError:
        print(f"Arquivo {file_name1} não encontrado. Tentando abrir {file_name2}...")
        try:
            with open(file_name2, 'r') as file:
                resultados_do_ativo_df = pd.read_csv(file_name2, sep=";", decimal=",", index_col=0, encoding="utf-8")
                print(f"Abrindo arquivo: {file_name2}")
        except FileNotFoundError:
            print(f"Ambos os arquivos não foram encontrados.")

    for _, row in resultados_do_ativo_df.iterrows():

        # Criação de uma nova linha com os dados extraídos de cada linha do DataFrame
        nova_linha = {
            'janela_rsi': row['janela_rsi'],
            'ordem': row['ordem'],
            'lookback': row['lookback'],
            'd_max': row['d_max'],
            'num_pontos': row['num_pontos'],
            'break_min': row['break_min'],
            'ppt': row['ppt'],
            'sl': row['sl'],
            'pt': row['pt'],
            'ativo': row['ativo'],
            'cenario': row['cenario'],
            'return_ann': row['return_ann'],
            'sharpe_ratio': row['sharpe_ratio'],
            'max_drawdown': row['max_drawdown'],
            'trades': row['trades'],
        }

        # Adicionando a nova linha ao DataFrame
        resultados_consolidados = pd.concat(
            [resultados_consolidados, pd.DataFrame([nova_linha])],
            ignore_index=True
        )

# Salva o arquivo com os resultados consolidados

folder_path = f'simulações_aplicadas_a_ativos - fases validação e final 4/'
file_name_resultado_cenário = f'{folder_path}/resultados_consolidados_finais.csv'
resultados_consolidados.to_csv(file_name_resultado_cenário, sep=";", decimal=",", index=True, encoding="utf-8")

file_name = f'base_dados_ativos_simulados/resultados.csv'
df_buy_and_hold= pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")

# Configuração do gráfico -----------------------------------out_of_sample_final_1----------------------------------

plt.figure(figsize=(12, 8))

# Resultados para out_of_sample_final_1 (marcados com "squares")
df1 = resultados_consolidados[resultados_consolidados['cenario'] == 'out_of_sample_final_1']
plt.scatter(
    df1['return_ann'], df1['sharpe_ratio'],
    c='blue', marker='s', label='Simulação: out_of_sample_final_1'
)

df2 = df_buy_and_hold[df_buy_and_hold['Cenario'] == 'out_of_sample_final_1']
plt.scatter(
    df2['Retorno_Anual_Medio'], df2['Sharpe_Ratio'],
    color='grey', marker='x', label='Buy and Hold: out_of_sample_final_1'
)

# Adicionando linhas horizontais e verticais
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configuração de títulos e eixos
plt.title('Retorno Anual vs Sharpe Ratio (out_of_sample_final_1)', fontsize=16)
plt.xlabel('Retorno Anual (%)', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# Adiciona a legenda
plt.legend(title='Cenário', fontsize=12, frameon=False, loc='lower right')

# Salvar gráfico como imagem
file_name = f'simulações_aplicadas_a_ativos - fases validação e final 4/dispersao_cenario_out_of_sample_final_1.png'
plt.savefig(file_name, dpi=300)
plt.close()

# Configuração do gráfico --------------------------------------out_of_sample_final_2-------------------------------

plt.figure(figsize=(12, 8))

# Resultados para out_of_sample_final_2 (marcados com "circles")
df3 = resultados_consolidados[resultados_consolidados['cenario'] == 'out_of_sample_final_2']
plt.scatter(
    df3['return_ann'], df3['sharpe_ratio'],
    c='red', marker='o', label='Simulação: out_of_sample_final_2'
)

df4 = df_buy_and_hold[df_buy_and_hold['Cenario'] == 'out_of_sample_final_2']
plt.scatter(
    df4['Retorno_Anual_Medio'], df4['Sharpe_Ratio'],
    color='grey', marker='*', label='Buy and Hold: out_of_sample_final_2'
)

# Adicionando linhas horizontais e verticais
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configuração de títulos e eixos
plt.title('Retorno Anual vs Sharpe Ratio (out_of_sample_final_2)', fontsize=16)
plt.xlabel('Retorno Anual (%)', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# Adiciona a legenda
plt.legend(title='Cenário', fontsize=12, frameon=False, loc='lower right')

# Salvar gráfico como imagem
file_name = f'simulações_aplicadas_a_ativos - fases validação e final 4/dispersao_cenario_out_of_sample_final_2.png'
plt.savefig(file_name, dpi=300)
plt.close()

# Configuração do gráfico ----------------------------------Os dois intervalos juntos -----------------------------------

plt.figure(figsize=(12, 8))

# Cenário 1
plt.scatter(
    df1['return_ann'], df1['sharpe_ratio'],
    c='blue', marker='s', label='Simulação: out_of_sample_final_1'
)
plt.scatter(
    df2['Retorno_Anual_Medio'], df2['Sharpe_Ratio'],
    color='grey', marker='x', label='Buy and Hold: out_of_sample_final_1'
)

# Cenário 2
plt.scatter(
    df3['return_ann'], df3['sharpe_ratio'],
    c='red', marker='o', label='Simulação: out_of_sample_final_2'
)
plt.scatter(
    df4['Retorno_Anual_Medio'], df4['Sharpe_Ratio'],
    color='grey', marker='*', label='Buy and Hold: out_of_sample_final_2'
)

# Adicionando linhas horizontais e verticais
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configuração de títulos e eixos
plt.title('Retorno Anual vs Sharpe Ratio (dois intervalos)', fontsize=16)
plt.xlabel('Retorno Anual (%)', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# Adiciona a legenda consolidada
plt.legend(title='Cenário', fontsize=12, frameon=False, loc='lower right')

# Salvar gráfico consolidado como imagem
file_name = f'simulações_aplicadas_a_ativos - fases validação e final 4/dispersao_cenario_out_of_sample_final_todos.png'
plt.savefig(file_name, dpi=300)
plt.close()

# Configuração do gráfico --------------------A média dos intervalos -------------------------------------------------
plt.figure(figsize=(12, 8))

# Agrupando médias por ativo
media_sim1 = resultados_consolidados.groupby('ativo')[['return_ann', 'sharpe_ratio']].mean().reset_index()
media_bh = df_buy_and_hold.groupby('Ativo')[['Retorno_Anual_Medio', 'Sharpe_Ratio']].mean().reset_index()

# Plotando os valores agrupados
plt.scatter(
    media_sim1['return_ann'], media_sim1['sharpe_ratio'],
    c='blue', marker='s', label='Médias Simulação: out_of_sample_final_1'
)

# Buy and Hold agrupado

plt.scatter(
    media_bh['Retorno_Anual_Medio'], media_bh['Sharpe_Ratio'],
    color='grey', marker='x', label='Buy and Hold: out_of_sample_final_1'
)

# Adicionando linhas horizontais e verticais
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configurando títulos e eixos
plt.title('Médias de Retorno Anual vs Sharpe Ratio por Ativo', fontsize=16)
plt.xlabel('Retorno Anual (%)', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# Adicionando legenda ajustada
plt.legend(title='Cenário', fontsize=10, frameon=False, loc='lower right')

# Salvar gráfico consolidado como imagem
file_name = 'simulações_aplicadas_a_ativos - fases validação e final 4/dispersao_cenario_out_of_sample_final_medias.png'
plt.savefig(file_name, dpi=300)
plt.close()

print(f"Gráfico salvo como {file_name}")

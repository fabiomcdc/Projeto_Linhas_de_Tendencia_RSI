# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
#  Eliminando warnings indesejados 
# ---------------------------------------------------------------------

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------------------------------------------------
# Cria o scattered para o in_sample ----------------------
# ----------------------------------------------------------------------

file_name = f'simulações_aplicadas_a_ativos - fases validação e final 4/resultados_consolidados_validacao.csv'
resultados_consolidados = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")

file_name = f'base_dados_ativos_simulados/resultados.csv'
df_buy_and_hold= pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")

# Definindo as cores com base nas condições
cores = [
    'blue' if (row['sharpe_ratio'] > 0.75 and row['return_ann'] > 10) else
    'gray' if (row['sharpe_ratio'] > 0 and row['return_ann'] > 0) else
    'red'
    for _, row in resultados_consolidados.iterrows()
]

# Configuração do gráfico
plt.figure(figsize=(12, 8))

cenarios = ['in_sample_1_2x', 'in_sample_2_2x', 'in_sample_3_2x', 'out_of_sample_val_1', 'out_of_sample_val_2']
títulos = ['in_sample_1', 'in_sample_2', 'in_sample_3', 'out_of_sample_val_1', 'out_of_sample_val_2']
cenarios_buy_and_hold = ['in_sample_1_1x', 'in_sample_2_1x', 'in_sample_3_1x', 'out_of_sample_val_1', 'out_of_sample_val_2']
marcadores = ['x', 'o', '*', 'd', 's']
cores_legenda = ['black', 'black', 'black']

# Loop para criar gráficos por cenário
for i, cenario in enumerate(cenarios):
    # Filtra apenas os dados do cenário atual
    df_cenario = resultados_consolidados[resultados_consolidados['cenario'] == cenario]

    # Cria uma nova figura para cada cenário
    plt.figure(figsize=(12, 8))
    plt.scatter(
        df_cenario['return_ann'], df_cenario['sharpe_ratio'],
        c=[cores[idx] for idx in df_cenario.index], marker=marcadores[i], label=f'{títulos[i]}'
    )

    # Filtra os dados de buy and hold para o mesmo cenário do loop
    df_buy_and_hold_cenario = df_buy_and_hold[df_buy_and_hold['Cenario'] == cenarios_buy_and_hold[i]]

    # Adiciona os pontos de buy and hold ao mesmo gráfico
    plt.scatter(
        df_buy_and_hold_cenario['Retorno_Anual_Medio'], df_buy_and_hold_cenario['Sharpe_Ratio'],
        c='black', marker='x', label='Buy and Hold'
    )

    # Linhas horizontais e verticais
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
    plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
    plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

    # Configuração de títulos e eixos
    plt.title(f'Dispersão dos Resultados: {títulos[i]}', fontsize=16)
    plt.xlabel('Retorno Anual (%)', fontsize=12)
    plt.ylabel('Sharpe Ratio', fontsize=12)

    # Grade e legenda
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title='Cenário', fontsize=12, frameon=False)

    # Salvar gráfico como imagem
    file_name = f'simulações_aplicadas_a_ativos - fases validação e final 4/dispersao_cenario_{cenario}.png'
    plt.savefig(file_name, dpi=300)
    plt.close()  # Fecha a figura atual para evitar sobreposição



# Cria uma nova figura para o cenario total
plt.figure(figsize=(12, 8))
plt.scatter(
    resultados_consolidados['return_ann'], resultados_consolidados['sharpe_ratio'],
    c=[cores[idx] for idx in resultados_consolidados.index], label='Todos os Cenários'
)

# Adiciona os pontos de buy and hold ao mesmo gráfico
plt.scatter(
    df_buy_and_hold['Retorno_Anual_Medio'], df_buy_and_hold['Sharpe_Ratio'],
    c='black', marker='x', label='Buy and Hold'
)

# Linhas horizontais e verticais
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configuração de títulos e eixos
plt.title(f'Dispersão dos Resultados: {títulos[i]}', fontsize=16)
plt.xlabel('Retorno Anual (%)', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)

# Grade e legenda
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Cenário', fontsize=12, frameon=False)

# Adicionando linhas horizontais e verticais sem incluir na legenda:
# Linhas para Sharpe Ratio e Retorno iguais a zero
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)

# Linhas para Sharpe Ratio = 0.75 e Retorno = 10
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configuração de títulos e eixos
plt.title('Dispersão dos Resultados: Retorno Anual vs Sharpe Ratio', fontsize=16)
plt.xlabel('Retorno Anual (%)', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)

# Adiciona uma grade
plt.grid(True, linestyle='--', alpha=0.5)

# Adiciona a legenda com marcadores em preto
plt.legend(title='Cenário', fontsize=12, frameon=False)

file_name = f'simulações_aplicadas_a_ativos - fases validação e final 4/dispersão_cenario_todos_cenarios.png'
plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI
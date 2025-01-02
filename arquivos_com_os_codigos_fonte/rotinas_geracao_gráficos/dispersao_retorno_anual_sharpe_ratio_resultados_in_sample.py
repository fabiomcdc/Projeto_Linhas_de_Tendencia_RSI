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



#---------------------------------------------------------------------
# Setando localidade
#---------------------------------------------------------------------

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

folder_path = f'simulacoes_realizadas/simulacoes_in_sample'
file_name_resultado_cenário = f'{folder_path}/consolidação_todos_in_sample.csv'
resultados_consolidados = pd.read_csv(file_name_resultado_cenário, sep=";", decimal=",", index_col=0, encoding="utf-8")

file_name = f'bases_de_dados/base_dados_ativos_simulados/resultados.csv'
df_buy_and_hold= pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")



# Configuração do gráfico -----------------------------------in_sample_1_1x----------------------------------

plt.figure(figsize=(12, 8))

# Resultados para in_sample_1_1x (marcados com "squares")
df1 = resultados_consolidados[resultados_consolidados['cenario'] == 'in_sample_1_1x']
plt.scatter(
    df1['return_ann'], df1['sharpe_ratio'],
    c='blue', marker='s', label='Simulação: in_sample_1_1x'
)

df2 = df_buy_and_hold[df_buy_and_hold['Cenario'] == 'in_sample_1_1x']
plt.scatter(
    df2['Retorno_Anual_Medio'], df2['Sharpe_Ratio'],
    color='black', marker='x', label='Buy and Hold: in_sample_1_1x'
)

# Adicionando linhas horizontais e verticais
plt.axhline(y=0, color='grey', linestyle='--', linewidth=1)
plt.axvline(x=0, color='grey', linestyle='--', linewidth=1)
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configuração de títulos e eixos
plt.title('Retorno Anual vs Sharpe Ratio (in_sample_1_1x)', fontsize=18)
plt.xlabel('Retorno Anual (%)', fontsize=14)
plt.ylabel('Sharpe Ratio', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

# Ajustando a escala do eixo x
plt.xlim(-30, 200)
plt.xticks(ticks=[0, 50, 100, 150, 200])

# Ajustando a escala do eixo y
plt.ylim(-0.7, 2.1)
plt.yticks(ticks=[-0.5, 0, 0.5, 1.0, 1.5, 2.0])

# Adiciona a legenda
plt.legend(title='', fontsize=16, frameon=False, loc='lower right')

plt.subplots_adjust(
    left=0.07,  # Margem esquerda
    right=0.97,  # Margem direta
    top=0.94,  # Margem superior
    bottom=0.08 # Margem inferior
    )  # Espaçamento vertical entre os gráficos

# Salvar gráfico como imagem
file_name = f'graficos_da_dissertacao/dispersao_retorno_anual_sharpe_ratio_simulacao_in_sample/dispersao_cenario_in_sample_1_1x.png'
plt.savefig(file_name, dpi=300)
plt.close()





# Configuração do gráfico --------------------------------------in_sample_2_1x-------------------------------

plt.figure(figsize=(12, 8))

# Resultados para in_sample_2_1x (marcados com "circles")
df3 = resultados_consolidados[resultados_consolidados['cenario'] == 'in_sample_2_1x']
plt.scatter(
    df3['return_ann'], df3['sharpe_ratio'],
    c='red', marker='o', label='Simulação: in_sample_2_1x'
)

df4 = df_buy_and_hold[df_buy_and_hold['Cenario'] == 'in_sample_2_1x']
plt.scatter(
    df4['Retorno_Anual_Medio'], df4['Sharpe_Ratio'],
    color='black', marker='*', label='Buy and Hold: in_sample_2_1x'
)

# Adicionando linhas horizontais e verticais
plt.axhline(y=0, color='grey', linestyle='--', linewidth=1)
plt.axvline(x=0, color='grey', linestyle='--', linewidth=1)
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configuração de títulos e eixos
plt.title('Retorno Anual vs Sharpe Ratio (in_sample_2_1x)', fontsize=18)
plt.xlabel('Retorno Anual (%)', fontsize=14)
plt.ylabel('Sharpe Ratio', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

# Ajustando a escala do eixo x
plt.xlim(-30, 200)
plt.xticks(ticks=[0, 50, 100, 150, 200])

# Ajustando a escala do eixo y
plt.ylim(-0.7, 2.1)
plt.yticks(ticks=[-0.5, 0, 0.5, 1.0, 1.5, 2.0])

# Adiciona a legenda
plt.legend(title='', fontsize=16, frameon=False, loc='lower right')

plt.subplots_adjust(
    left=0.07,  # Margem esquerda
    right=0.97,  # Margem direta
    top=0.94,  # Margem superior
    bottom=0.08 # Margem inferior
    )  # Espaçamento vertical entre os gráficos

# Salvar gráfico como imagem
file_name = f'graficos_da_dissertacao/dispersao_retorno_anual_sharpe_ratio_simulacao_in_sample/dispersao_cenario_in_sample_2_1x.png'
plt.savefig(file_name, dpi=300)
plt.close()




# Configuração do gráfico --------------------------------------in_sample_3_1x-------------------------------

plt.figure(figsize=(12, 8))

# Resultados para in_sample_3_1x (marcados com "circles")
df5 = resultados_consolidados[resultados_consolidados['cenario'] == 'in_sample_3_1x']
plt.scatter(
    df5['return_ann'], df5['sharpe_ratio'],
    c='green', marker='h', label='Simulação: in_sample_3_1x'
)

df6 = df_buy_and_hold[df_buy_and_hold['Cenario'] == 'in_sample_3_1x']
plt.scatter(
    df6['Retorno_Anual_Medio'], df6['Sharpe_Ratio'],
    color='black', marker='v', label='Buy and Hold: in_sample_3_1x'
)

# Adicionando linhas horizontais e verticais
plt.axhline(y=0, color='grey', linestyle='--', linewidth=1)
plt.axvline(x=0, color='grey', linestyle='--', linewidth=1)
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configuração de títulos e eixos
plt.title('Retorno Anual vs Sharpe Ratio (in_sample_3_1x)', fontsize=18)
plt.xlabel('Retorno Anual (%)', fontsize=14)
plt.ylabel('Sharpe Ratio', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

# Ajustando a escala do eixo x
plt.xlim(-30, 200)
plt.xticks(ticks=[0, 50, 100, 150, 200])

# Ajustando a escala do eixo y
plt.ylim(-0.7, 2.1)
plt.yticks(ticks=[-0.5, 0, 0.5, 1.0, 1.5, 2.0])

# Adiciona a legenda
plt.legend(title='', fontsize=16, frameon=False, loc='lower right')

plt.subplots_adjust(
    left=0.07,  # Margem esquerda
    right=0.97,  # Margem direta
    top=0.94,  # Margem superior
    bottom=0.08 # Margem inferior
    )  # Espaçamento vertical entre os gráficos

# Salvar gráfico como imagem
file_name = f'graficos_da_dissertacao/dispersao_retorno_anual_sharpe_ratio_simulacao_in_sample/dispersao_cenario_in_sample_3_1x.png'
plt.savefig(file_name, dpi=300)
plt.close()


# Configuração do gráfico ----------------------------------Os três intervalos juntos -----------------------------------

plt.figure(figsize=(12, 8))

# Cenário 1
plt.scatter(
    df1['return_ann'], df1['sharpe_ratio'],
    c='blue', marker='s', label='Simulação: in_sample_1_1x'
)


# Cenário 2
plt.scatter(
    df3['return_ann'], df3['sharpe_ratio'],
    c='red', marker='o', label='Simulação: in_sample_2_1x'
)

plt.scatter(
    df5['return_ann'], df5['sharpe_ratio'],
    c='green', marker='h', label='Simulação: in_sample_3_1x'
)

# Cenários Buy and Hold

plt.scatter(
    df2['Retorno_Anual_Medio'], df2['Sharpe_Ratio'],
    color='black', marker='x', label='Buy and Hold: in_sample_1_1x'
)

plt.scatter(
    df4['Retorno_Anual_Medio'], df4['Sharpe_Ratio'],
    color='black', marker='*', label='Buy and Hold: in_sample_2_1x'
)

plt.scatter(
    df6['Retorno_Anual_Medio'], df6['Sharpe_Ratio'],
    color='black', marker='v', label='Buy and Hold: in_sample_3_1x'
)


# Adicionando linhas horizontais e verticais
plt.axhline(y=0, color='grey', linestyle='--', linewidth=1)
plt.axvline(x=0, color='grey', linestyle='--', linewidth=1)
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configuração de títulos e eixos
plt.title('Retorno Anual vs Sharpe Ratio (os três intervalos)', fontsize=18)
plt.xlabel('Retorno Anual (%)', fontsize=14)
plt.ylabel('Sharpe Ratio', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

# Ajustando a escala do eixo x
plt.xlim(-30, 200)
plt.xticks(ticks=[0, 50, 100, 150, 200])

# Ajustando a escala do eixo y
plt.ylim(-0.7, 2.1)
plt.yticks(ticks=[-0.5, 0, 0.5, 1.0, 1.5, 2.0])

# Adiciona a legenda consolidada
plt.legend(title='', fontsize=16, frameon=False, loc='lower right')

plt.subplots_adjust(
    left=0.07,  # Margem esquerda
    right=0.97,  # Margem direta
    top=0.94,  # Margem superior
    bottom=0.08 # Margem inferior
    )  # Espaçamento vertical entre os gráficos

# Salvar gráfico consolidado como imagem
file_name = f'graficos_da_dissertacao/dispersao_retorno_anual_sharpe_ratio_simulacao_in_sample/dispersao_cenario_in_sample_todos.png'
plt.savefig(file_name, dpi=300)
plt.close()

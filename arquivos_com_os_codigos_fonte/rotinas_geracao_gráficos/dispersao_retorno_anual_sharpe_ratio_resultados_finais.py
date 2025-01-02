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

folder_path = f'simulacoes_realizadas/simulacoes_out_of_sample_final'
file_name_resultado_cenário = f'{folder_path}/resultados_consolidados_finais.csv'
resultados_consolidados = pd.read_csv(file_name_resultado_cenário, sep=";", decimal=",", index_col=0, encoding="utf-8")

file_name = f'bases_de_dados/base_dados_ativos_simulados/resultados.csv'
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
plt.title('Retorno Anual vs Sharpe Ratio (out_of_sample_final_1)', fontsize=18)
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
file_name = f'graficos_da_dissertacao/dispersao_retorno_anual_sharpe_ratio_simulacao_final/dispersao_cenario_out_of_sample_final_1.png'
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
plt.title('Retorno Anual vs Sharpe Ratio (out_of_sample_final_2)', fontsize=18)
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
file_name = f'graficos_da_dissertacao/dispersao_retorno_anual_sharpe_ratio_simulacao_final/dispersao_cenario_out_of_sample_final_2.png'
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
plt.title('Retorno Anual vs Sharpe Ratio (dois intervalos)', fontsize=18)
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
file_name = f'graficos_da_dissertacao/dispersao_retorno_anual_sharpe_ratio_simulacao_final/dispersao_cenario_out_of_sample_final_todos.png'
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
    c='blue', marker='s', label='Médias Simulação: out_of_sample_final_1 e 2'
)

# Buy and Hold agrupado

plt.scatter(
    media_bh['Retorno_Anual_Medio'], media_bh['Sharpe_Ratio'],
    color='grey', marker='x', label='Médias Buy and Hold: out_of_sample_final_1 e 2'
)

# Adicionando linhas horizontais e verticais
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
plt.axhline(y=0.75, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=10, color='blue', linestyle='--', linewidth=1)

# Configurando títulos e eixos
plt.title('Médias de Retorno Anual vs Sharpe Ratio por Ativo', fontsize=18)
plt.xlabel('Retorno Anual (%)', fontsize=14)
plt.ylabel('Sharpe Ratio', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

# Ajustando a escala do eixo x
plt.xlim(-30, 200)
plt.xticks(ticks=[0, 50, 100, 150, 200])

# Ajustando a escala do eixo y
plt.ylim(-0.7, 2.1)
plt.yticks(ticks=[-0.5, 0, 0.5, 1.0, 1.5, 2.0])

# Adicionando legenda ajustada
plt.legend(title='', fontsize=16, frameon=False, loc='lower right')

plt.subplots_adjust(
    left=0.07,  # Margem esquerda
    right=0.97,  # Margem direta
    top=0.94,  # Margem superior
    bottom=0.08 # Margem inferior
    )  # Espaçamento vertical entre os gráficos

# Salvar gráfico consolidado como imagem
file_name = 'graficos_da_dissertacao/dispersao_retorno_anual_sharpe_ratio_simulacao_final/dispersao_cenario_out_of_sample_final_medias.png'
plt.savefig(file_name, dpi=300)
plt.close()

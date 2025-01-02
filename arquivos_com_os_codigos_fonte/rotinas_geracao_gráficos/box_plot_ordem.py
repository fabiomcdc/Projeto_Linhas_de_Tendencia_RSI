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


# ---------------------------------------------------------------------
#  Carrega arquivo com todas as simulações in_sample
# ---------------------------------------------------------------------


#  ---------------------------------------------------------
    
folder_path = f'simulacoes_realizadas/simulacoes_in_sample'
file_name = f'{folder_path}/consolidação_todos_in_sample.csv'

print("Carregando  ,", file_name)

resultados_todos_in_sample = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# Box plot com ordem ---------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Cria o box plot com o retorno anual por ordem ----------------------
# -------------------------------------------------------------------------

plt.figure(figsize=(10, 6))

resultados_todos_in_sample.boxplot(column='return_ann', by='ordem', grid=False, showfliers=True)

# Configurar título e rótulos
plt.title('Box Plot de Retorno Anual por ordem')
plt.suptitle('')  # Remove o título padrão gerado pelo pandas
plt.xlabel('ordem')
plt.ylabel('Retorno Anual %')

# Calcular e adicionar o texto "Média" e o valor
ordem_values = resultados_todos_in_sample['ordem'].unique()
ylim = plt.ylim()  # Obtém os limites do eixo Y
offset = (ylim[1] - ylim[0]) * 0.03  # Define um deslocamento proporcional para posicionamento

for i, value in enumerate(ordem_values):
    mean_value = resultados_todos_in_sample[resultados_todos_in_sample['ordem'] == value]['return_ann'].mean()
    
    # Adicionar o texto "Média" uma linha acima
    plt.text(i + 1, mean_value + offset, 'Média:', ha='center', va='bottom', color='black', fontsize=9)
    
    # Adicionar o valor da média na posição correta
    plt.text(i + 1, mean_value, f'{mean_value:.2f}', ha='center', va='bottom', color='black', fontsize=9)

plt.subplots_adjust(
    left=0.116,  # Margem esquerda
    right=0.97,  # Margem direta
    top=0.94,  # Margem superior
    bottom=0.1 # Margem inferior
    )  # Espaçamento vertical entre os gráficos

folder_path = f'graficos_da_dissertacao/box_plot_ordem'
file_name = f'{folder_path}/retorno_anual_por_ordem.png'
plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI


# ----------------------------------------------------------------------------
# Cria o box plot com o número de trades por ordem ----------------------
# ----------------------------------------------------------------------------

resultados_todos_in_sample.boxplot(column='trades', by='ordem', grid=False, showfliers=True)

# Configurar título e rótulos
plt.title('Box Plot de Número de Trades por ordem')
plt.suptitle('')  # Remove o título padrão gerado pelo pandas
plt.xlabel('ordem')
plt.ylabel('Número de trades')

# Calcular e adicionar o texto "Média" e o valor
ordem_values = resultados_todos_in_sample['ordem'].unique()
ylim = plt.ylim()  # Obtém os limites do eixo Y
offset = (ylim[1] - ylim[0]) * 0.03  # Define um deslocamento proporcional para posicionamento

for i, value in enumerate(ordem_values):
    mean_value = resultados_todos_in_sample[resultados_todos_in_sample['ordem'] == value]['trades'].mean()
    
    # Adicionar o texto "Média" uma linha acima
    plt.text(i + 1, mean_value + offset, 'Média:', ha='center', va='bottom', color='black', fontsize=9)
    
    # Adicionar o valor da média na posição correta
    plt.text(i + 1, mean_value, f'{mean_value:.2f}', ha='center', va='bottom', color='black', fontsize=9)

plt.subplots_adjust(
    left=0.113,  # Margem esquerda
    right=0.97,  # Margem direta
    top=0.94,  # Margem superior
    bottom=0.1 # Margem inferior
    )  # Espaçamento vertical entre os gráficos

file_name = f'{folder_path}/num_trades_por_ordem.png'
plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# ------------------------------------------------------------------------
# Cria o box plot com o sharpe_ratio por ordem ----------------------
# ------------------------------------------------------------------------

resultados_todos_in_sample.boxplot(column='sharpe_ratio', by='ordem', grid=False, showfliers=True)

# Configurar título e rótulos
plt.title('Box Plot de Sharpe Ratio por ordem')
plt.suptitle('')  # Remove o título padrão gerado pelo pandas
plt.xlabel('ordem')
plt.ylabel('Sharpe Ratio')

# Calcular e adicionar o texto "Média" e o valor
ordem_values = resultados_todos_in_sample['ordem'].unique()
ylim = plt.ylim()  # Obtém os limites do eixo Y
offset = (ylim[1] - ylim[0]) * 0.03  # Define um deslocamento proporcional para posicionamento

for i, value in enumerate(ordem_values):
    mean_value = resultados_todos_in_sample[resultados_todos_in_sample['ordem'] == value]['sharpe_ratio'].mean()
    
    # Adicionar o texto "Média" uma linha acima
    plt.text(i + 1, mean_value + offset, 'Média:', ha='center', va='bottom', color='black', fontsize=9)
    
    # Adicionar o valor da média na posição correta
    plt.text(i + 1, mean_value, f'{mean_value:.2f}', ha='center', va='bottom', color='black', fontsize=9)


plt.subplots_adjust(
    left=0.105,  # Margem esquerda
    right=0.97,  # Margem direta
    top=0.94,  # Margem superior
    bottom=0.1 # Margem inferior
    )  # Espaçamento vertical entre os gráficos

file_name = f'{folder_path}/sharpe_ratio_por_ordem.png'
plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI



# ----------------------------------------------------------------------
# Cria o box plot com max_drawdown por ordem ----------------------
# ----------------------------------------------------------------------

resultados_todos_in_sample.boxplot(column='max_drawdown', by='ordem', grid=False, showfliers=True)

# Configurar título e rótulos
plt.title('Box Plot do Drawdown % máximo por ordem')
plt.suptitle('')  # Remove o título padrão gerado pelo pandas
plt.xlabel('ordem')
plt.ylabel('Percentual de Drawdown Máximo')

plt.subplots_adjust(
    left=0.13,  # Margem esquerda
    right=0.97,  # Margem direta
    top=0.94,  # Margem superior
    bottom=0.1 # Margem inferior
    )  # Espaçamento vertical entre os gráficos

# Calcular e adicionar o texto "Média" e o valor
ordem_values = resultados_todos_in_sample['ordem'].unique()
ylim = plt.ylim()  # Obtém os limites do eixo Y
offset = (ylim[1] - ylim[0]) * 0.03  # Define um deslocamento proporcional para posicionamento

for i, value in enumerate(ordem_values):
    mean_value = resultados_todos_in_sample[resultados_todos_in_sample['ordem'] == value]['max_drawdown'].mean()
    
    # Adicionar o texto "Média" uma linha acima
    plt.text(i + 1, mean_value + offset, 'Média:', ha='center', va='bottom', color='black', fontsize=9)
    
    # Adicionar o valor da média na posição correta
    plt.text(i + 1, mean_value, f'{mean_value:.2f}', ha='center', va='bottom', color='black', fontsize=9)

file_name = f'{folder_path}/max_drawdown_por_ordem.png'
plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI
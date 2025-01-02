# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import numpy as np
import pandas as pd
from scipy.stats import ttest_rel, shapiro, wilcoxon


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
retornos_simulacao = pd.read_csv(file_name_resultado_cenário, sep=";", decimal=",", index_col=0, encoding="utf-8")

file_name = f'bases_de_dados/base_dados_ativos_simulados/resultados.csv'
retornos_buy_and_hold= pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")

# Redefinindo o índice para que 'Ativo' seja uma coluna
retornos_buy_and_hold.reset_index(inplace=True)

# Renomeando colunas para garantir compatibilidade no merge
retornos_buy_and_hold.rename(columns={'Ativo': 'ativo', 'Cenario': 'cenario'}, inplace=True)

# Fazendo o merge com base no par (ativo, cenario)
df_merged = pd.merge(
    retornos_simulacao[['ativo', 'cenario', 'return_ann']],
    retornos_buy_and_hold[['ativo', 'cenario', 'Retorno_Anual_Medio']],
    on=['ativo', 'cenario']
)

# Calculando as diferenças emparelhadas
df_merged['diferenca'] = df_merged['return_ann'] - df_merged['Retorno_Anual_Medio']

stat, p_value = wilcoxon(df_merged['diferenca'])

# Exibindo os resultados
print("Teste de Wilcoxon para Amostras Pareadas:")
print(f"Estatística: {stat}, p-valor: {p_value}")

# Interpretação
if p_value < 0.05:
    print("Hipótese rejeitada: A estratégia simulada é estatisticamente superior ao Buy and Hold (mediana das diferenças é positiva).")
else:
    print("Não foi possível rejeitar a hipótese nula: Não há evidência suficiente de superioridade da estratégia simulada.")



# Realizando o teste de Shapiro-Wilk
stat, p_value = shapiro(df_merged['diferenca'])

# Exibindo os resultados
print("Teste de Shapiro-Wilk:")
print(f"Estatística W: {stat}, p-valor: {p_value}")

# Interpretando o resultado
if p_value < 0.05:
    print("Os dados não seguem uma distribuição normal (rejeitamos H0).")
else:
    print("Os dados seguem uma distribuição normal (não rejeitamos H0).")



# Realizando o teste t de amostras pareadas
resultado_pareado = ttest_rel(df_merged['return_ann'], df_merged['Retorno_Anual_Medio'])

# Obtendo a estatística t e o p-valor bilateral
estatistica_t = resultado_pareado.statistic
p_valor_bilateral = resultado_pareado.pvalue

# Ajustando para teste unidirecional (one-tailed)
if estatistica_t > 0:
    p_valor_unilateral = p_valor_bilateral / 2
else:
    p_valor_unilateral = 1  # Se t < 0, não há evidência para rejeitar H0 em um teste unidirecional

# Exibindo os resultados
print("Teste t de amostras pareadas:")
print(f"Estatística t: {estatistica_t}, p-valor bilateral: {p_valor_bilateral}, p-valor unilateral: {p_valor_unilateral}")

# Interpretação
if p_valor_unilateral < 0.05:
    print("Hipótese rejeitada: A estratégia simulada é estatisticamente superior à estratégia Buy and Hold.")
else:
    print("Não foi possível rejeitar a hipótese nula: Não há evidência suficiente de que a estratégia simulada seja superior.")


import matplotlib.pyplot as plt

# Boxplot das diferenças
plt.boxplot(df_merged['diferenca'], vert=False)
plt.title("Boxplot das Diferenças Emparelhadas")
plt.xlabel("Diferenças")
plt.show()
# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import FormatStrFormatter


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


# Caminhos e arquivo de entrada
folder_path = 'simulacoes_realizadas/simulacoes_in_sample'
file_name_melhor_resultado_cenario = f'{folder_path}/melhores_resultados.csv'
melhores_resultados_por_ativo_in_sample_1 = pd.read_csv(file_name_melhor_resultado_cenario, sep=";", decimal=",", encoding="utf-8")

# Caminho para salvar os gráficos
folder_path_graficos = 'graficos_da_dissertacao/frequencia_de_ocorrencia_parametros_in_sample'
os.makedirs(folder_path_graficos, exist_ok=True)  # Garantir que o diretório exista

# Lista de parâmetros a serem filtrados
parametros = ['janela_rsi', 'ordem', 'lookback', 'num_pontos', 'break_min']

# Dicionário de valores esperados para cada parâmetro
valores_esperados = {
    'ordem': [1, 2, 3, 4],
    'janela_rsi': [14, 21, 28, 35, 42, 49, 56, 63],
    'lookback': [50, 100],
    'break_min': [3, 4],
    'num_pontos': [2, 3],
}

# Gerar gráficos de barras para frequência dos parâmetros
for param in parametros:
    # Filtrar o DataFrame para o parâmetro atual
    df_param = melhores_resultados_por_ativo_in_sample_1[melhores_resultados_por_ativo_in_sample_1['variavel'] == param]

    # Calcular a distribuição de frequência
    freq = df_param['melhor_valor'].value_counts().sort_index()

    # Obter os valores esperados para o parâmetro atual usando o dicionário
    if param in valores_esperados:
        freq = freq.reindex(valores_esperados[param], fill_value=0)

    # Plotar a distribuição do parâmetro
    plt.figure(figsize=(8, 5))
    ax = freq.plot(kind='bar', color='grey', edgecolor='black')

    # Ajustar o limite superior do eixo Y
    max_freq = freq.max()  # Frequência máxima
    ax.set_ylim(0, max_freq * 1.2)  # Adiciona 20% de espaço acima da barra mais alta

    # Fixar os labels do eixo X na mesma altura
    ax.set_xticks(range(len(freq)))
    ax.set_xticklabels(freq.index, rotation=0, ha='center', va='top')  # Centraliza e ajusta verticalmente

    # Adicionar valores acima das barras
    for bar in ax.patches:
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # Posição X
            bar.get_height() + 0.1,  # Posição Y (um pouco acima da barra)
            f'{int(bar.get_height())}',  # Valor da frequência
            ha='center', va='bottom', fontsize=10  # Centralizar e ajustar fonte
        )

    # Configurar título e rótulos
    plt.title(f'Distribuição de {param}')
    plt.xlabel(param)
    plt.ylabel('Frequência')

    plt.subplots_adjust(
    left=0.09,  # Margem esquerda
    right=0.97,  # Margem direta
    top=0.93,  # Margem superior
    bottom=0.12 # Margem inferior
    )  # Espaçamento vertical entre os gráficos

    # Salvar o gráfico com o nome baseado no parâmetro
    file_name = f'{folder_path_graficos}/frequencia_{param}.png'
    plt.savefig(file_name, dpi=300)  # Salva com resolução de 300 DPI
    
    plt.close()  # Fechar o gráfico para liberar memória
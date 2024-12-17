# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
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


folder_path = f'simulações_aplicadas_a_ativos_in_sample_resultados'
file_name = f'{folder_path}/resultados_in_sample_final.csv'
print("Carregando  ,", file_name)

resultados_consolidados = pd.read_csv(file_name, sep=";", decimal=",", encoding="utf-8")

file_name_melhor_resultado_cenário = f'simulações_aplicadas_a_ativos_in_sample_resultados/media_pontos_ponderados.csv'
media_pontos_ponderados=pd.read_csv(file_name_melhor_resultado_cenário, sep=";", decimal=",", encoding="utf-8")

file_name_melhor_resultado_cenário = f'simulações_aplicadas_a_ativos_in_sample_resultados/melhores_resultados_consolidados.csv'
melhores_resultados_por_ativo_in_sample_1=pd.read_csv(file_name_melhor_resultado_cenário, sep=";", decimal=",", encoding="utf-8")




parametros = ['janela_rsi', 'ordem', 'lookback', 'num_pontos', 'break_min', 'ppt']

# Gerar gráficos de barras para frequência dos parâmetros
for param in parametros:
    plt.figure(figsize=(8, 5))
    melhores_resultados_por_ativo_in_sample_1[param].value_counts().sort_index().plot(kind='bar')
    plt.title(f'Distribuição de {param}')
    plt.xlabel(param)
    plt.ylabel('Frequência')
    
    # # Formatar o eixo y com uma casa decimal
    # plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    
    # Salvar o gráfico com o nome baseado no parâmetro
    file_name = f'{folder_path}/frequencia_{param}.png'
    plt.savefig(file_name, dpi=300)  # Salva com resolução de 300 DPI
    
    plt.close()  # Fechar o gráfico para liberar memória















# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------
# # Box plot com  janela_rsi ---------------------------------------------------
# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------


# # -------------------------------------------------------------------------
# # Cria o box plot com o retorno anual por janela_rsi ----------------------
# # -------------------------------------------------------------------------

# plt.figure(figsize=(10, 6))

# resultados_consolidados.boxplot(column='return_ann', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Retorno Anual por janela_rsi')
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi', fontsize=12)
# plt.ylabel('Retorno Anual %', fontsize = 12)



# # # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/retorno_anual_por_rsi.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI





# # ----------------------------------------------------------------------------
# # Cria o box plot com o número de trades por janela_rsi ----------------------
# # ----------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='trades', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Número de Trades por janela_rsi', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi', fontsize=12)
# plt.xlabel('Número de trades', fontsize=12)

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/num_trades_por_rsi.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ------------------------------------------------------------------------
# # Cria o box plot com o sharpe_ratio por janela_rsi ----------------------
# # ------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='sharpe_ratio', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Sharpe Ratio por janela_rsi', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi', fontsize=12)
# plt.ylabel('Sharpe Ratio', fontsize=12)

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/sharpe_ratio_por_rsi.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por janela_rsi ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por janela_rsi', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi', fontsize=12)
# plt.ylabel('Percentual de Drawdown Máximo', fontsize=12)

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_rsi.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por janela_rsi ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='janela_rsi', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por janela_rsi', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('janela_rsi', fontsize=12)
# plt.ylabel('Percentual de Drawdown Máximo', fontsize=12)

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_rsi.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI





# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------
# # Box plot com lookback ---------------------------------------------------
# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------



# # -------------------------------------------------------------------------
# # Cria o box plot com o retorno anual por lookback ----------------------
# # -------------------------------------------------------------------------

# plt.figure(figsize=(10, 6))

# resultados_consolidados.boxplot(column='return_ann', by='lookback', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Retorno Anual por lookback', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('lookback', fontsize=12)
# plt.ylabel('Retorno Anual %', fontsize=12)

# # # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/retorno_anual_por_lookback.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI


# # ----------------------------------------------------------------------------
# # Cria o box plot com o número de trades por lookback ----------------------
# # ----------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='trades', by='lookback', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Número de Trades por lookback', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('lookback', fontsize=12)
# plt.xlabel('Número de trades', fontsize=12)

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/num_trades_por_lookback.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ------------------------------------------------------------------------
# # Cria o box plot com o sharpe_ratio por lookback ----------------------
# # ------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='sharpe_ratio', by='lookback', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Sharpe Ratio por lookback', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('lookback', fontsize=12)
# plt.ylabel('Sharpe Ratio', fontsize=12)

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/sharpe_ratio_por_lookback.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por lookback ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='lookback', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por lookback', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('lookback', fontsize=12)
# plt.ylabel('Percentual de Drawdown Máximo', fontsize=12)

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_lookback.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por lookback ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='lookback', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por lookback', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('lookback', fontsize=12)
# plt.ylabel('Percentual de Drawdown Máximo', fontsize=12)

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_lookback.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI





# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------
# # Box plot com  break_min ---------------------------------------------------
# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------



# # -------------------------------------------------------------------------
# # Cria o box plot com o retorno anual por break_min ----------------------
# # -------------------------------------------------------------------------

# plt.figure(figsize=(10, 6))

# resultados_consolidados.boxplot(column='return_ann', by='break_min', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Retorno Anual por break_min', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('break_min', fontsize = 12)
# plt.ylabel('Retorno Anual %', fontsize = 12)

# # # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/retorno_anual_por_break_min.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI


# # ----------------------------------------------------------------------------
# # Cria o box plot com o número de trades por break_min ----------------------
# # ----------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='trades', by='break_min', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Número de Trades por break_min', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('break_min', fontsize = 12)
# plt.xlabel('Número de trades', fontsize=12)

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/num_trades_por_break_min.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ------------------------------------------------------------------------
# # Cria o box plot com o sharpe_ratio por break_min ----------------------
# # ------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='sharpe_ratio', by='break_min', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Sharpe Ratio por break_min', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('break_min', fontsize = 12)
# plt.ylabel('Sharpe Ratio', fontsize = 12)

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/sharpe_ratio_por_break_min.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por break_min ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='break_min', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por break_min', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('break_min', fontsize = 12)
# plt.ylabel('Percentual de Drawdown Máximo', fontsize = 12)

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_break_min.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por break_min ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='break_min', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por break_min', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('break_min', fontsize = 12)
# plt.ylabel('Percentual de Drawdown Máximo', fontsize = 12)

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_break_min.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI






# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------
# # Box plot com  ordem ---------------------------------------------------
# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------



# # -------------------------------------------------------------------------
# # Cria o box plot com o retorno anual por ordem ----------------------
# # -------------------------------------------------------------------------

# plt.figure(figsize=(10, 6))

# resultados_consolidados.boxplot(column='return_ann', by='ordem', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Retorno Anual por ordem', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('ordem', fontsize = 12)
# plt.ylabel('Retorno Anual %', fontsize = 12)

# # # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/retorno_anual_por_ordem.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI


# # ----------------------------------------------------------------------------
# # Cria o box plot com o número de trades por ordem ----------------------
# # ----------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='trades', by='ordem', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Número de Trades por ordem', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('ordem', fontsize = 12)
# plt.xlabel('Número de trades', fontsize=12)

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/num_trades_por_ordem.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ------------------------------------------------------------------------
# # Cria o box plot com o sharpe_ratio por ordem ----------------------
# # ------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='sharpe_ratio', by='ordem', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Sharpe Ratio por ordem', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('ordem', fontsize = 12)
# plt.ylabel('Sharpe Ratio', fontsize = 12)

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/sharpe_ratio_por_ordem.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por ordem ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='ordem', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por ordem', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('ordem', fontsize = 12)
# plt.ylabel('Percentual de Drawdown Máximo', fontsize = 12)

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_ordem.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por ordem ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='ordem', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por ordem', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('ordem', fontsize = 12)
# plt.ylabel('Percentual de Drawdown Máximo', fontsize = 12)

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_ordem.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI






# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------
# # Box plot com  num_pontos ---------------------------------------------------
# # ----------------------------------------------------------------------------
# # ----------------------------------------------------------------------------



# # -------------------------------------------------------------------------
# # Cria o box plot com o retorno anual por num_pontos ----------------------
# # -------------------------------------------------------------------------

# plt.figure(figsize=(10, 6))

# resultados_consolidados.boxplot(column='return_ann', by='num_pontos', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Retorno Anual por num_pontos', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('num_pontos', fontsize = 12)
# plt.ylabel('Retorno Anual %', fontsize = 12)

# # # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/retorno_anual_por_num_pontos.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI


# # ----------------------------------------------------------------------------
# # Cria o box plot com o número de trades por num_pontos ----------------------
# # ----------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='trades', by='num_pontos', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Número de Trades por num_pontos', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('num_pontos', fontsize = 12)
# plt.xlabel('Número de trades', fontsize=12)

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/num_trades_por_num_pontos.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ------------------------------------------------------------------------
# # Cria o box plot com o sharpe_ratio por num_pontos ----------------------
# # ------------------------------------------------------------------------

# resultados_consolidados.boxplot(column='sharpe_ratio', by='num_pontos', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot de Sharpe Ratio por num_pontos', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('num_pontos', fontsize = 12)
# plt.ylabel('Sharpe Ratio', fontsize = 12)

# # Exibir o gráfico
# # plt.show()

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/sharpe_ratio_por_num_pontos.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por num_pontos ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='num_pontos', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por num_pontos', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('num_pontos', fontsize = 12)
# plt.ylabel('Percentual de Drawdown Máximo', fontsize = 12)

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_num_pontos.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI




# # ----------------------------------------------------------------------
# # Cria o box plot com max_drawdown por num_pontos ----------------------
# # ----------------------------------------------------------------------

# resultados_consolidados.boxplot(column='max_drawdown', by='num_pontos', grid=False, showfliers=True)

# # Configurar título e rótulos
# plt.title('Box Plot do Drawdown % máximo por num_pontos', fontsize=14)
# plt.suptitle('')  # Remove o título padrão gerado pelo pandas
# plt.xlabel('num_pontos', fontsize = 12)
# plt.ylabel('Percentual de Drawdown Máximo', fontsize = 12)

# plt.subplots_adjust(
#     left=0.12,  # Margem esquerda
#     right=0.97,  # Margem direta
#     top=0.94,  # Margem superior
#     bottom=0.1 # Margem inferior
#     )  # Espaçamento vertical entre os gráficos

# # Exibir o gráfico
# # plt.show()

# file_name = f'simulações_aplicadas_a_ativos_in_sample_resultados/max_drawdown_por_num_pontos.png'
# plt.savefig(file_name, dpi=300)  # Salva como PNG com resolução de 300 DPI






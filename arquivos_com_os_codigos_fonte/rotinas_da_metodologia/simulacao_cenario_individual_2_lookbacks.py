# ---------------------------------------------------------------------
#  Importando bibliotecas
# ---------------------------------------------------------------------

import pandas as pd
import yfinance as yf
import os
import matplotlib.pyplot as plt
from backtesting import Backtest, Strategy

# ---------------------------------------------------------------------
#  Importando rotinas
# ---------------------------------------------------------------------

from arquivos_com_os_codigos_fonte.rotinas_da_metodologia.gerador_de_sinais_para_um_cenario import simulacao
from arquivos_com_os_codigos_fonte.rotinas_da_metodologia.classe_estrategia import EstrategiaAdaptada

# ------------------------------------------------------------------------------------
# Criando rotina de consolida eventos de break para um determinado ponto
# ------------------------------------------------------------------------------------


def consolidar_eventos(grupo):
    contagem_evento_1 = (grupo['evento'] == 1).sum()
    contagem_evento_2 = (grupo['evento'] == 2).sum()
    if contagem_evento_1 > contagem_evento_2:
        return 1
    elif contagem_evento_1 < contagem_evento_2:
        return 2
    else:
        return 0

# ----------------------------------------------------------------------------------------------------------------
# Rotina que processa uma simulação e devolve um resultado
# ----------------------------------------------------------------------------------------------------------------

def processa_simulacao_dois_lookbacks(ticker,
                       tipo_intervalo,
                       start_date,
                       end_date,
                       break_min_vals,
                       janela_rsi_vals,
                       ordem_vals,
                       lookback_vals,
                       num_pontos_vals,
                       ppt,
                       d_max,
                       sl_vals,
                       pt_vals,
                       aplicar_log,
                       imprime_grafico,
                       salva_dados,
                       folder_raiz):
    
    ticker_clean = ticker.replace("^", "")
    folder_path = f'{folder_raiz}/{ticker_clean}'
    file_name_tipo_intervalo = f'{tipo_intervalo}'

    intervalos_valendo = pd.DataFrame(columns=['data_ini_periodo', 'data_fim_periodo'])
    intervalos_valendo = intervalos_valendo._append({
        'data_ini_periodo': pd.Timestamp(start_date),
        'data_fim_periodo': pd.Timestamp(end_date)
    }, ignore_index=True)

    start_date_gráfico = f"{pd.Timestamp(start_date).year if pd.Timestamp(start_date).month >= 7 else pd.Timestamp(start_date).year - 1}-01-01"

    # Especifica os nomes de todos os arquivos de auditoria que serão salvos

    file_name_trades = f'{folder_path}/{ticker_clean}_{file_name_tipo_intervalo}_trades.csv'
    file_name_equity_curve = f'{folder_path}/{ticker_clean}_{file_name_tipo_intervalo}_equity_curve.csv'
    file_name_backtesting = f'{folder_path}/{ticker_clean}_{file_name_tipo_intervalo}_gráfico_backtesting_html'

    # Cria o DataFrame para armazenar os resultados que serão retornados

    resultados = pd.DataFrame(columns=[
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
        'start_date',
        'end_date',
        'final_balance',
        'return_acum',
        'return_ann',
        'sharpe_ratio',
        'sortino_ratio',
        'volatility',
        'max_drawdown',
        'trades',
        'win_rate',
        'profit_factor',
        'avg_trade_return',
        ])

    # -------------------------------------------------------------------------------------------------------
    # Se os dados tiverem sido salvos em bases_de_dados/base_dados_ativos_simulados/{ticker_clean}
    # comente o trecho abaixo e use o código de carregar os dados
    # -------------------------------------------------------------------------------------------------------


    # if ticker:
    #     # Importa os dados do Yahoo Finace
    #     data = yf.download(ticker, start=start_date_gráfico, end=end_date)
        
    # else:
    #     print("Índice inválido")

    # # Converte colunas numéricas (exceto 'Date', que é uma string)
    # colunas_numericas = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    # # Converte as colunas para tipo numérico (ignorar erros caso já esteja no formato correto)
    # data[colunas_numericas] = data[colunas_numericas].apply(pd.to_numeric, errors='coerce')



    # -------------------------------------------------------------------------------------------------------
    # Se os dados NÃO tiverem sido salvos em bases_de_dados/base_dados_ativos_simulados/{ticker_clean}
    # comente o trecho abaixo e baixe diretamente do yf
    # -------------------------------------------------------------------------------------------------------

    if ticker:
        
        file_name = f'bases_de_dados/base_dados_ativos_simulados/{ticker_clean}/{tipo_intervalo}_dados.csv'
        print('Importando base de --------------------------',file_name)
        data = pd.read_csv(file_name, sep=";", decimal=",", encoding="utf-8")
    else:
        print("Índice inválido")

    # Converte colunas numéricas (exceto 'Date', que é uma string)
    colunas_numericas = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    # Converte as colunas para tipo numérico (ignorar erros caso já esteja no formato correto)
    data[colunas_numericas] = data[colunas_numericas].apply(pd.to_numeric, errors='coerce')
    data = pd.read_csv(file_name, sep=";", decimal=",", index_col=0, encoding="utf-8")
    data.index = pd.to_datetime(data.index, errors='coerce')





    # -------------------------------------------------------------------------------------------------------
    # Loops para simular todos os cenários
    # -------------------------------------------------------------------------------------------------------

    contador = 1

    for num_pontos in num_pontos_vals:
        for break_min in break_min_vals:
            for janela_rsi in janela_rsi_vals:
                for ordem in ordem_vals:
                    if len(lookback_vals) == 2:
                        print(f'Simulação {contador} para: Ativo={ticker_clean}, num_pontos={num_pontos}, janela_rsi={janela_rsi}, ordem={ordem}, lookback = {lookback_vals}, d_max={d_max}, '
                                f'break_min={break_min}, aplicar_log={aplicar_log}')
                        contador = contador + 1                       
                        # Chama a função de simulação para gerar os sinais

                        breaks_gerados_1 = simulacao(janela_rsi,
                                                ordem,
                                                lookback_vals[0],
                                                d_max,
                                                num_pontos,
                                                break_min,
                                                ppt,
                                                data,
                                                aplicar_log,
                                                ticker_clean,
                                                imprime_grafico,
                                                salva_dados)
                        
                        breaks_gerados_2 = simulacao(janela_rsi,
                                                ordem,
                                                lookback_vals[1],
                                                d_max,
                                                num_pontos,
                                                break_min,
                                                ppt,
                                                data,
                                                aplicar_log,
                                                ticker_clean,
                                                imprime_grafico,
                                                salva_dados)
                        
                                                # Consolidando os dois dataframes
                        # Combine os dois dataframes adicionando as linhas
                        breaks_gerados_consolidado = pd.concat([breaks_gerados_1, breaks_gerados_2], ignore_index=True)


                        # Ordene o dataframe consolidado por 'x_rompimento', 'fim_janela' e 'ponto'
                        breaks_gerados_consolidado = breaks_gerados_consolidado.sort_values(by=['x_rompimento', 'fim_janela', 'ponto'])

                        # Função para consolidar os eventos agrupados por 'x_rompimento'


                        # Consolidar o dataframe agrupando por 'x_rompimento'
                        breaks_gerados = (
                            breaks_gerados_consolidado.groupby('x_rompimento')
                            .apply(lambda grupo: pd.Series({
                                'evento': consolidar_eventos(grupo),
                                'reta': grupo['reta'].iloc[0],  # Mantendo o primeiro valor (ou escolha outro critério)
                                'y_rompimento': grupo['y_rompimento'].iloc[0],  # Mantendo o primeiro valor
                                'inicio_janela': grupo['inicio_janela'].iloc[0],  # Mantendo o primeiro valor
                                'fim_janela': grupo['fim_janela'].iloc[0]  # Mantendo o primeiro valor
                            }))
                            .reset_index()
                        )

                        # Transfere os sinais para a base com os dados

                        data['Evento'] = 0 # Zera os valor de Evento em data para colocar os Eventos de break

                        for _, row in breaks_gerados.iterrows():
                            x_rompimento = int(row['x_rompimento'])  # Certifique-se de que ponto é um inteiro
                            evento = row['evento']
                            if 0 <= x_rompimento-1 < len(data):  # Verifique se está dentro dos limites
                                data.iloc[x_rompimento-1, data.columns.get_loc('Evento')] = evento

                    
                    # Cria o DataFrame para backtesting com índice datetime

                    dados_backtesting = pd.DataFrame({
                        'Open': data['Open'],    # Preço de abertura
                        'High': data['High'],    # Preço mais alto
                        'Low': data['Low'],      # Preço mais baixo
                        'Close': data['Close'],  # Preço de fechamento
                        'Volume': data['Volume'], # Volume negociado
                        'Evento': data['Evento']  # Sinais de compra e venda
                    }, index=data.index)  # Define o índice como a coluna 'Date'

                    # Executa o backtesting

                    bt = Backtest(dados_backtesting, EstrategiaAdaptada, cash=10_000_000, commission=.002)
                    for sl_val in sl_vals:
                        for pt_val in pt_vals:
                            print(f"Rodando o backtest para: sl={sl_val}, pt={pt_val}")
                            resultado_bt = bt.run(
                                pt=pt_val, 
                                sl=sl_val, 
                                intervalos_valendo=intervalos_valendo
                            )

                            nova_linha = {
                                'janela_rsi': janela_rsi, 
                                'ordem': ordem, 
                                'lookback': f"lookback duplo [{lookback_vals[0]}, {lookback_vals[1]}]",
                                'd_max': d_max,
                                'num_pontos': num_pontos,
                                'break_min': break_min,
                                'ppt': ppt,
                                'sl': sl_val,
                                'pt': pt_val,
                                'ativo': ticker,
                                'start_date': start_date,
                                'end_date': end_date,
                                'final_balance': resultado_bt['Equity Final [$]'],
                                'return_acum': resultado_bt['Return [%]'],
                                'return_ann': resultado_bt['Return (Ann.) [%]'],
                                'sharpe_ratio': resultado_bt['Sharpe Ratio'],
                                'sortino_ratio': resultado_bt['Sortino Ratio'],
                                'volatility': resultado_bt['Volatility (Ann.) [%]'],
                                'max_drawdown': resultado_bt['Max. Drawdown [%]'], 
                                'trades': resultado_bt['# Trades'],  
                                'win_rate': resultado_bt['Win Rate [%]'],
                                'profit_factor': resultado_bt['Profit Factor'],
                                'avg_trade_return': resultado_bt['Avg. Trade [%]'],
                            }

                            resultados = pd.concat([resultados, pd.DataFrame([nova_linha])], ignore_index=True)                        
                            
                            if imprime_grafico:
                                
                                # # Obtem os trades executados trades = stats._trades

                                trades = resultado_bt._trades
                                trades.to_csv(file_name_trades, sep=";", decimal=",", index=True, encoding="utf-8")

                                equity_values = resultado_bt._equity_curve
                                equity_values.to_csv(file_name_equity_curve, sep=";", decimal=",", index=True, encoding="utf-8")

                                bt.plot(open_browser=True, filename=file_name_backtesting)

  
    # Retorna os resultados
    return resultados
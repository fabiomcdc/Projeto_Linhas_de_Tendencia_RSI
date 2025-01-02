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

# ------------------------------------------------------------------------------------
# Criando a classe de estratégia a ser usada pela biblioteca Backtesting do Python
# ------------------------------------------------------------------------------------

class EstrategiaAdaptada(Strategy):
    # Adicione os parâmetros como variáveis de classe
    pt = 0.0  # Profit target padrão, depois será sobrescrita
    sl = 0.02  # Stop loss padrão, depois será sobrescrita
    intervalos_valendo = None  # DataFrame com intervalos de datas permitidos

    def init(self):
        # Inicializando as variáveis de estado
        self.pos_ant = 0  # 0 = sem posição, -1 = vendido, 1 = comprado
        self.ini_posicao_ant = None  # Índice inicial da posição anterior
        self.valor_posicao_ant = None  # Valor inicial da posição anterior

        self.datas_validas = self._gerar_datas_validas()  # Lista de datas válidas para negociação


    def _gerar_datas_validas(self):
        # Gera um conjunto de datas válidas baseado no DataFrame intervalos_valendo.
        datas_validas = set()

        # Garante que as colunas do DataFrame estão no formato datetime
        self.intervalos_valendo['data_ini_periodo'] = pd.to_datetime(self.intervalos_valendo['data_ini_periodo'])
        self.intervalos_valendo['data_fim_periodo'] = pd.to_datetime(self.intervalos_valendo['data_fim_periodo'])

        # Percorre cada linha do DataFrame separadamente
        for i in range(len(self.intervalos_valendo)):
            data_ini = self.intervalos_valendo.iloc[i]['data_ini_periodo']
            data_fim = self.intervalos_valendo.iloc[i]['data_fim_periodo']

            # Gera o intervalo de datas para a linha atual
            intervalo_atual = pd.date_range(start=data_ini, end=data_fim)

            # Adiciona as datas ao conjunto de datas válidas
            datas_validas.update(intervalo_atual)
        
        return datas_validas


    def next(self):
        # Preço atual e índice
        valor = self.data.Close[-1]  # Preço de fechamento da barra sendo inspecionada
        ind = len(self.data) - 1  # Índice atual no DataFrame
        
        # Data atual
        data_atual = self.data.df.index[ind]

        # Verifica se a data atual não é válida
        if data_atual not in self.datas_validas:
            if self.pos_ant != 0:  # Se houver posição aberta
                self.position.close()  # Fecha a posição existente
                self.pos_ant = 0  # Atualiza estado para sem posição
            return  # Finaliza o processamento para a data atual

        # Evento da estratégia
        evento = self.data.df.loc[self.data.df.index[ind], 'Evento']

        # Lógica de abertura de uma posição a partir de uma posição neutra
        if self.pos_ant == 0:  # Sem posição
            if evento == 1:  # Sinal de compra
                self.buy()  # Abrir posição de compra
                self.pos_ant = 1  # Muda variável de estado para comprado
                self.ini_posicao_ant = ind  # Marca a barra em que a posição foi comprada
                self.valor_posicao_ant = valor  # Assume que posição adquirida foi o preço de fechamento da barra sendo inspecionada
            elif evento == 2:  # Sinal de venda
                self.sell()  # Abrir posição de venda
                self.pos_ant = -1  # Muda variável de estado para vendido
                self.ini_posicao_ant = ind  # Marca a barra em que a posição foi vendida
                self.valor_posicao_ant = valor  # Assume que posição vendida foi o preço de fechamento da barra sendo inspecionada

        # Lógica de decisão caso a posição anterior fosse vendida
        elif self.pos_ant == -1:  # Posição vendida
            if -(valor / self.valor_posicao_ant - 1) > self.pt or \
               -(valor / self.valor_posicao_ant - 1) < -self.sl or evento == 1:  # Testa stop loss ou profit taking ou sinal de compra
                self.position.close()  # Fecha a posição
                self.pos_ant = 0  # Muda variável de estado para neutro

        # Lógica de decisão caso a posição anterior fosse comprada
        elif self.pos_ant == 1:  # Posição comprada
            if (valor - self.valor_posicao_ant) / self.valor_posicao_ant > self.pt or \
               (valor - self.valor_posicao_ant) / self.valor_posicao_ant < -self.sl or evento == 2:
                self.position.close()  # Fecha a posição
                self.pos_ant = 0  # Muda variável de estado para neutro
def cruzou_para_baixo(ind_pontos, slope_reta_suporte, intercept_reta_suporte, break_min):
    cruzou = False
    for x, y in ind_pontos:
        y_reta = slope_reta_suporte * x + intercept_reta_suporte
        if abs(y - y_reta) > break_min:
            cruzou = True
            break
    return cruzou


# DataFrame para armazenar os resultados
breaks = pd.DataFrame(columns=['ponto', 'evento', 'reta'])

# Processamento
for i in range(4, len(data_RSI)):
    # Criando a lista de pontos para a linha atual
    pontos = [(j, data_RSI.iloc[j]['RSI']) for j in range(i-4, i+1)]

    for idx, linha in eliminado_trendlines_suporte.iterrows():
        # Extraindo os valores da reta e a fim_janela
        slope = linha['support_slope']
        intercept = linha['support_intercept']
        fim_janela = linha['fim_janela']

        # Verificando se i é maior do que fim_janela + ordem
        if i > fim_janela + ordem:
            # Verificando cruzamento
            if cruzou_para_baixo(pontos, slope, intercept, break_min):
                # Adicionando ao DataFrame 'breaks'
                breaks = breaks.append({'ponto': i, 'evento': 'bsd', 'reta': idx}, ignore_index=True)

# Exibir os resultados
print(breaks)

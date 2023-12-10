import pandas as pd
import numpy as np

def check_trend_line(support: bool, pivot: int, slope: float, y: np.array):
    # compute sum of differences between line and prices, 
    # return negative val if invalid 
    
    # Find the intercept of the line going through pivot point with given slope
    intercept = -slope * pivot + y.iloc[pivot]
    line_vals = slope * np.arange(len(y)) + intercept
     
    diffs = line_vals - y
    
    # Check to see if the line is valid, return -1 if it is not valid.
    if support and diffs.max() > 1e-5:
        return -1.0
    elif not support and diffs.min() < -1e-5:
        return -1.0

    # Squared sum of diffs between data and line 
    err = (diffs ** 2.0).sum()
    return err


def optimize_slope(support: bool, pivot:int , init_slope: float, y: np.array):
    
    # Amount to change slope by. Multiplyed by opt_step
    slope_unit = (y.max() - y.min()) / len(y) 
    
    # Optmization variables
    opt_step = 1.0
    min_step = 0.0001
    curr_step = opt_step # current step
    
    # Initiate at the slope of the line of best fit
    best_slope = init_slope
    best_err = check_trend_line(support, pivot, init_slope, y)
    assert(best_err >= 0.0) # Shouldn't ever fail with initial slope

    get_derivative = True
    derivative = None
    while curr_step > min_step:

        if get_derivative:
            # Numerical differentiation, increase slope by very small amount
            # to see if error increases/decreases. 
            # Gives us the direction to change slope.
            slope_change = best_slope + slope_unit * min_step
            test_err = check_trend_line(support, pivot, slope_change, y)
            derivative = test_err - best_err;
            
            # If increasing by a small amount fails, 
            # try decreasing by a small amount
            if test_err < 0.0:
                slope_change = best_slope - slope_unit * min_step
                test_err = check_trend_line(support, pivot, slope_change, y)
                derivative = best_err - test_err

            if test_err < 0.0: # Derivative failed, give up
                raise Exception("Derivative failed. Check your data. ")

            get_derivative = False

        if derivative > 0.0: # Increasing slope increased error
            test_slope = best_slope - slope_unit * curr_step
        else: # Increasing slope decreased error
            test_slope = best_slope + slope_unit * curr_step
        

        test_err = check_trend_line(support, pivot, test_slope, y)
        if test_err < 0 or test_err >= best_err: 
            # slope failed/didn't reduce error
            curr_step *= 0.5 # Reduce step size
        else: # test slope reduced error
            best_err = test_err 
            best_slope = test_slope
            get_derivative = True # Recompute derivative
    
    # Optimize done, return best slope and intercept
    return (best_slope)

def fit_trendlines_single(data: np.array):
    # Trendline de melhor fit (por least squared) 
    # coefs[0] = slope,  coefs[1] = intercept
    x = np.arange(len(data))
    coefs = np.polyfit(x, data, 1)
    
    # Pontos do eixo y correspondentes a trendline fittada
    line_points = coefs[0] * x + coefs[1]

    # acha os índices do pontos chaves de máximo e de mínimo
    upper_pivot = (data - line_points).argmax() 
    lower_pivot = (data - line_points).argmin() 

    # Optimando a inclinação para as linhas de tendência
    support_slope = optimize_slope(True, lower_pivot, coefs[0], data)
    resist_slope = optimize_slope(False, upper_pivot, coefs[0], data)

    return (lower_pivot, support_slope, upper_pivot, resist_slope) 

def mapear_retas_com_bottoms(bottoms, retas, dist_min):
    mapeamento = pd.DataFrame(index=bottoms['bottom_idx'], columns=retas['indice'])

    # Preencher o DataFrame mapeamento
    for bottom in bottoms.itertuples():
        for reta in retas.itertuples():
            valor_na_reta = bottom.bottom_idx * reta.support_slope + reta.support_intercept
            distancia = bottom.bottom_price - valor_na_reta

            if abs(distancia) < dist_min:
                mapeamento.at[bottom.bottom_idx, reta.indice] = 0
            elif distancia < 0:
                mapeamento.at[bottom.bottom_idx, reta.indice] = -1
            else:
                mapeamento.at[bottom.bottom_idx, reta.indice] = 1

    # Avaliar cada reta
    for coluna in mapeamento.columns:
        coluna_valores = mapeamento[coluna]
        zeros_consecutivos = 0
        x_min = None
        x_max = None
        for i, valor in enumerate(coluna_valores):
            if valor == 0:
                if x_min is None:
                    x_min = mapeamento.index[i]
                x_max = mapeamento.index[i]
                zeros_consecutivos += 1
            elif valor == -1:
                x_min = None
                x_max = None
                zeros_consecutivos = 0
            if zeros_consecutivos >= 3:
                retas.loc[retas['indice'] == coluna, 'mapeado'] = 1
                break
            else:
                retas.loc[retas['indice'] == coluna, 'mapeado'] = 0

        retas.loc[retas['indice'] == coluna, 'x_min'] = x_min
        retas.loc[retas['indice'] == coluna, 'x_max'] = x_max

    retas.to_csv('dados_csv_produzidos/retas.csv', index=True)
    return retas

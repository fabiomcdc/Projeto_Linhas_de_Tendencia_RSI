import pandas as pd
import numpy as np
import os
import random


def criar_intervalos(data_ini, data_fim, seed=None):

    variacao_da_media_min = -0.04
    variacao_da_media_max = 0.04

    # Gera os dias úteis
    dias_uteis = pd.bdate_range(start=data_ini, end=data_fim)
    num_dias = len(dias_uteis)

    # Calculando valor_min e valor_max
    valor_base = num_dias // 9  # Trunca para inteiro
    valor_min = int(valor_base + (variacao_da_media_min * num_dias))
    valor_max = int(valor_base + (variacao_da_media_max * num_dias))

    # Repetir até que o nono intervalo esteja no intervalo desejado
    while True:
        intervalos = []
        dias_restantes = dias_uteis.copy()

        # sorteia 8 datas para gerar 9 intervalos aleatórioa
        for _ in range(8):
            # Calcula o tamanho do intervalo com a fórmula especificada
            tamanho_intervalo = int(
                valor_min + np.random.rand() * (valor_max - valor_min)
            )

            # Armazena o menor intervalo para garantir que não exceda os dias restantes
            tamanho_intervalo = min(tamanho_intervalo, len(dias_restantes))

            # Cria o intervalo
            data_ini_intervalo = dias_restantes[0]
            data_fim_intervalo = dias_restantes[tamanho_intervalo - 1]

            # Adiciona ao resultado
            intervalos.append(
                {
                    "data_ini_intervalo": data_ini_intervalo,
                    "data_fim_intervalo": data_fim_intervalo,
                    "tamanho": tamanho_intervalo,
                }
            )

            # Remove os dias usados do restante
            dias_restantes = dias_restantes[tamanho_intervalo:]

        # Adicionando o intervalo final com o que sobrou
        tamanho_ultimo_intervalo = len(dias_restantes)
        if (
            tamanho_ultimo_intervalo >= valor_min
            and tamanho_ultimo_intervalo <= valor_max
        ):
            # Se o tamanho do último intervalo está dentro do intervalo,
            # adiciona e sairdo loop
            intervalos.append(
                {
                    "data_ini_intervalo": dias_restantes[0],
                    "data_fim_intervalo": dias_restantes[-1],
                    "tamanho": tamanho_ultimo_intervalo,
                }
            )
            break  # Condição satisfeita

    # Converte para DataFrame
    intervalos_df = pd.DataFrame(intervalos)

    # Inicializa todos os intervalos como "Out_of_Sample_Validacao"
    intervalos_df["tipo_intervalo"] = "Out_of_Sample_Validacao"

    # Passo 2 - garante que o primeiro intervalo seja sempre "In_Sample"
    # e que o último intervalo seja sempre "Out_Of_Sample_Final"
    intervalos_df.loc[0, "tipo_intervalo"] = "In_Sample"
    intervalos_df.loc[len(intervalos_df) - 1, "tipo_intervalo"] = "Out_Of_Sample_Final"

    # Passo3 - sortea 4 intervalos adicionais para "In_Sample"
    in_sample_indices = np.random.choice(
        intervalos_df.index[1:8], size=4, replace=False
    )
    intervalos_df.loc[in_sample_indices, "tipo_intervalo"] = "In_Sample"

    # Passo 4 - sortea um dos intervalos restantes do tipo
    # "Out_of_Sample_Validacao" para ser "Out_Of_Sample_Final"
    out_of_sample_validacao_indices = intervalos_df[
        (intervalos_df["tipo_intervalo"] == "Out_of_Sample_Validacao")
    ].index
    if len(out_of_sample_validacao_indices) > 0:
        final_index = np.random.choice(out_of_sample_validacao_indices, size=1)[0]
        intervalos_df.loc[final_index, "tipo_intervalo"] = "Out_Of_Sample_Final"

    # Calcula a duração em dias úteis
    intervalos_df["duracao"] = intervalos_df.apply(
        lambda row: len(
            pd.bdate_range(
                start=row["data_ini_intervalo"], end=row["data_fim_intervalo"]
            )
        ),
        axis=1,
    )

    # Filtra apenas os intervalos "In_Sample"
    in_sample_df = intervalos_df[intervalos_df["tipo_intervalo"] == "In_Sample"]

    # Identifica mudanças consecutivas no tipo_intervalo
    intervalos_df["grupo"] = (
        intervalos_df["tipo_intervalo"] != intervalos_df["tipo_intervalo"].shift()
    ).cumsum()

    # Passo 5 - Consolida os intervalos por grupo
    intervalos_df_consolidado = (
        intervalos_df.groupby("grupo")
        .agg(
            {
                "data_ini_intervalo": "first",
                "data_fim_intervalo": "last",
                "tipo_intervalo": "first",
                "duracao": "sum",
            }
        )
        .reset_index(drop=True)
    )

    # Calcula estatísticas dos intervalos obtidos para validação

    in_sample_df = intervalos_df_consolidado[
        intervalos_df_consolidado["tipo_intervalo"] == "In_Sample"
    ]
    media_dias_in_sample = in_sample_df["duracao"].sum() / len(dias_uteis)

    out_of_sample_final_df = intervalos_df_consolidado[
        intervalos_df_consolidado["tipo_intervalo"] == "Out_Of_Sample_Final"
    ]
    media_dias_out_of_sample_final = out_of_sample_final_df["duracao"].sum() / len(
        dias_uteis
    )

    num_in_sample = len(
        intervalos_df_consolidado[
            intervalos_df_consolidado["tipo_intervalo"] == "In_Sample"
        ]
    )
    num_out_of_sample_validacao = len(
        intervalos_df_consolidado[
            intervalos_df_consolidado["tipo_intervalo"] == "Out_of_Sample_Validacao"
        ]
    )
    num_out_of_sample_final = len(
        intervalos_df_consolidado[
            intervalos_df_consolidado["tipo_intervalo"] == "Out_Of_Sample_Final"
        ]
    )

    return (
        intervalos_df_consolidado,
        media_dias_in_sample,
        media_dias_out_of_sample_final,
        num_in_sample,
        num_out_of_sample_validacao,
        num_out_of_sample_final,
    )


# Função para iterar a semente até atingir o critério

def encontrar_intervalos(data_ini, data_fim, min_media=0.55, max_media=0.62):
    contador = 1
    while True:
        print(contador)
        contador = contador + 1
        seed = random.randint(1, 10000)  # Geran uma semente aleatória
        (
            intervalos,
            media_dias_in_sample,
            media_dias_out_of_sample_final,
            num_in_sample,
            num_out_of_sample_validacao,
            num_out_of_sample_final,
        ) = criar_intervalos(data_ini, data_fim, seed=seed)
        if (
            media_dias_in_sample > 0.55
            and media_dias_out_of_sample_final > 0.17
            and num_in_sample == 3
            and num_out_of_sample_validacao == 2
            and num_out_of_sample_final == 2
        ):

            print(f"Semente encontrada: {seed}")
            return (
                intervalos,
                media_dias_in_sample,
                media_dias_out_of_sample_final,
                seed,
                num_in_sample,
                num_out_of_sample_validacao,
                num_out_of_sample_final,
            )


# Executa usando os dados desde 01/01/2000 até 01/11/2024

data_ini = "2000-01-01"
data_fim = "2024-11-01"
(
    intervalos,
    media_dias_in_sample,
    media_dias_out_of_sample_final,
    seed,
    num_in_sample,
    num_out_of_sample_validacao,
    num_out_of_sample_final,
) = encontrar_intervalos(data_ini, data_fim)

# Salva em CSV

file_path = os.path.join("dados_csv_produzidos", "datas_sorteadas.csv")
os.makedirs(os.path.dirname(file_path), exist_ok=True)
intervalos.to_csv(file_path, index=True)

print(intervalos)
print(f"Média: {media_dias_in_sample:.4f}")
print(f"Semente utilizada: {seed}")
print(f"Intervalos salvos em: {file_path}")

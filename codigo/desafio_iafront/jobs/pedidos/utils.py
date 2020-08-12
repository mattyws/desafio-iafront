import os

import pandas as pd
import multiprocessing as mp
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.data.saving import save_partitioned

from desafio_iafront.jobs.pedidos.contants import KEPT_COLUNS, COLUMN_RENAMES, SAVING_PARTITIONS


def _prepare(pedidos_joined: pd.DataFrame) -> pd.DataFrame:
    # Remove colunas resultantes do merge
    result_dataset = drop_merged_columns(pedidos_joined)
    # Remove colunas que não serão usadas
    result_dataset = result_dataset[KEPT_COLUNS]
    # Renomeia colunas
    result_dataset = result_dataset.rename(columns=COLUMN_RENAMES)

    return result_dataset


def drop_merged_columns(data_frame: pd.DataFrame) -> pd.DataFrame:
    result_dataset = data_frame.copy(deep=True)
    for column in data_frame.columns:
        if column.endswith("_off"):
            result_dataset = data_frame.drop(column, axis=1)
    return result_dataset


def save_prepared(saida: str, visita_com_produto_e_conversao_df: pd.DataFrame):
    prepared = _prepare(visita_com_produto_e_conversao_df)
    save_partitioned(prepared, saida, SAVING_PARTITIONS)


def merge_visita_produto(data_str: str, hour: int, pedidos_df: pd.DataFrame, produtos_df: pd.DataFrame, visitas_df: pd.DataFrame) -> pd.DataFrame:
    visita_com_produto_df = visitas_df.merge(produtos_df, how="inner", on="product_id", suffixes=("", "_off"))
    visita_com_produto_e_conversao_df = visita_com_produto_df.merge(pedidos_df, how="left",
                                                                    on="visit_id", suffixes=("", "_off"))
    visita_com_produto_e_conversao_df["data"] = data_str
    visita_com_produto_e_conversao_df["hora"] = hour
    return visita_com_produto_e_conversao_df


def create_pedidos_df(date_partition: str, hour_snnipet: str, pedidos: pd.DataFrame) -> pd.DataFrame:
    pedidos_partition = os.path.join(pedidos, date_partition, hour_snnipet)
    pedidos_df = read_partitioned_json(pedidos_partition)
    pedidos_df["visit_id"] = pedidos_df["visit_id"].astype(str)
    return pedidos_df


def create_visitas_df(date_partition: str, hour_snnipet: str, visitas: pd.DataFrame) -> pd.DataFrame:
    visitas_partition = os.path.join(visitas, date_partition, hour_snnipet)
    visitas_df = read_partitioned_json(visitas_partition)
    visitas_df["product_id"] = visitas_df["product_id"].astype(str)
    visitas_df["visit_id"] = visitas_df["visit_id"].astype(str)
    return visitas_df

def process_partition(data: str, hour: int, pedidos: str, produtos_df: pd.DataFrame, saida: str, visitas: str) -> pd.DataFrame:
    hour_snnipet = f"hora={hour}"

    data_str = data.strftime('%Y-%m-%d')
    date_partition = f"data={data_str}"

    visitas_df = create_visitas_df(date_partition, hour_snnipet, visitas)

    pedidos_df = create_pedidos_df(date_partition, hour_snnipet, pedidos)

    visita_com_produto_e_conversao_df = merge_visita_produto(data_str, hour, pedidos_df, produtos_df,
                                                             visitas_df)

    save_prepared(saida, visita_com_produto_e_conversao_df)

def process_data_with_multiprocessing(date_partitions: [], pedidos: str, produtos_df: pd.DataFrame,
                                      saida: str, visitas: str, manager_queue:mp.Queue):
    for data in date_partitions:
        hour_partitions = list(range(0, 23))
        for hour in hour_partitions:
            date_partition = process_partition(data, hour, pedidos, produtos_df, saida, visitas)
            manager_queue.put(str(data)+str(hour))
            # print(f"Concluído para {date_partition} {hour}h")
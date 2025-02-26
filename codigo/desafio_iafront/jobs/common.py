from functools import partial

import pandas as pd
from datetime import datetime
from typing import Sequence

from desafio_iafront.jobs.contants import columns_to_scale
from sklearn.base import TransformerMixin

from desafio_iafront.data.dataframe_utils import read_partitioned_json
import os


def get_feature_index(feature:str):
    return columns_to_scale.index(feature)


def prepare_dataframe(departamentos_lista: Sequence[str], dataset_path, data_inicial: datetime,
                      data_final: datetime):
    def filter_function(row):
        return filter_departamento(row, departamentos_lista) and filter_date(row, data_inicial, data_final)

    if departamentos_lista is None:
        filter_func = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    else:
        filter_func = filter_function
    visitas = read_partitioned_json(dataset_path, filter_func)
    visitas_com_coordenadas = _extracting_coordinates(visitas)
    visitas_com_conversao = convert(visitas_com_coordenadas)
    departamentos = pd.get_dummies(visitas_com_conversao["departamento"])
    result = visitas_com_conversao.join(departamentos).drop('departamento', axis=1)
    return result


def filter_departamento(row, departamentos_lista: Sequence[str]):
    return row["departamento"] in departamentos_lista


def filter_date(row, data_inicial: datetime, data_final: datetime):
    data = datetime.strptime(row["data"], "%Y-%m-%d")
    return data_inicial <= data < data_final


def _extracting_coordinates(dataframe: pd.DataFrame) -> pd.DataFrame:
    expanded_cols = pd.DataFrame(dataframe['coordenadas'].values.tolist(), columns=['latitude', 'longitude'])

    return dataframe.join(expanded_cols).drop('coordenadas', axis=1)


def transform(dataframe: pd.DataFrame, fields: Sequence[str], scaler: TransformerMixin) -> pd.DataFrame:
    fields_to_normalize = dataframe.filter(fields).to_numpy()
    feature_scaled = scaler.fit_transform(fields_to_normalize)
    dataframe['features'] = list(feature_scaled)
    return dataframe


def convert(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['convertido'] = [_apply_conversion(item) for item in dataframe['id_pedido']]
    return dataframe.drop('id_pedido', axis=1)


def _apply_conversion(product_id):
    if product_id is None:
        return 0
    else:
        return 1

def combine_series_with_sum(first:pd.Series, second:pd.Series):
    return first.combine(second, (lambda x1, x2: x1+x2), fill_value=0)


def extract_path_partitions_and_values(path:str):
    partitions = os.listdir(path)
    values = []
    feature = None
    for partition in partitions:
        partition = partition.split('=')
        if feature is not None and partition[0] != feature:
            raise ValueError("Partições com formatação incorreta.")
        feature = partition[0]
        values.append(partition[1])
    return feature, values
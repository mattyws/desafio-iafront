from collections import Sequence

import pandas
from datetime import datetime

columns_to_aggregate = ['data', 'hora', 'minuto']

def aggregate_conversao(dataset: pandas.DataFrame, columns_to_group:[]):
    clusters = dataset['cluster_label'].unique().tolist()
    aggregated_conversao = pandas.DataFrame([])
    for cluster in clusters:
        dataset_groupby = dataset[dataset['cluster_label'] == cluster].groupby(by=columns_to_group)
        for group in dataset_groupby.groups:
            date_group_df: pandas.DataFrame = dataset_groupby.get_group(group)
            group_conversao_count = date_group_df['convertido'].value_counts()
            if 1 in group_conversao_count.keys():
                group_conversao_count['convertido'] = group_conversao_count[1]
                group_conversao_count = group_conversao_count.drop(1)
            else:
                group_conversao_count['convertido'] = 0

            if 0 in group_conversao_count.keys():
                group_conversao_count['nao_convertido'] = group_conversao_count[0]
                group_conversao_count = group_conversao_count.drop(0)
            else:
                group_conversao_count['nao_convertido'] = 0

            if isinstance(group, list) or isinstance(group, tuple):
                for index, column in enumerate(columns_to_group):
                    group_conversao_count[column] = group[index]
            else:
                group_conversao_count[columns_to_group[0]] = group
            group_conversao_count['cluster_label'] = cluster
            aggregated_conversao = aggregated_conversao.append(group_conversao_count, ignore_index=True)
    if 'convertido' in aggregated_conversao.columns:
        aggregated_conversao.loc[:, 'convertido'] = aggregated_conversao['convertido'].astype(int)
    if 'nao_convertido' in aggregated_conversao.columns:
        aggregated_conversao.loc[:, 'nao_convertido'] = aggregated_conversao['nao_convertido'].astype(int)
    if 'minuto' in aggregated_conversao.columns:
        aggregated_conversao.loc[:, 'minuto'] = aggregated_conversao['minuto'].astype(int)
    return aggregated_conversao


def add_minutes_to_dataset(dataset:pandas.DataFrame):
    dataset.loc[:, 'datahora'] = pandas.to_datetime(dataset['datahora'], format="%Y-%m-%d %H:%M")
    dataset['minuto'] = dataset['datahora'].apply(lambda x: x.minute)
    return dataset

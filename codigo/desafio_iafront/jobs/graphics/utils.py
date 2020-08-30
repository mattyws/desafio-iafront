from collections import Sequence

import numpy
import pandas as pd
from bokeh.models import HoverTool
from bokeh.models.ranges import FactorRange
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure
from bokeh.plotting.figure import Figure
from desafio_iafront.jobs.common import columns_to_scale
from sklearn.decomposition import PCA
from bokeh.plotting import output_file, show

COLORS = ["green", "blue", "red", "orange", "purple"]

def plot(dataframe: pd.DataFrame, x_axis, y_axis, cluster_label, title=""):
    clusters = [label for label in dataframe[cluster_label]]

    colors = [set_color(_) for _ in clusters]

    p = figure(title=title)

    p.scatter(dataframe[x_axis].tolist(), dataframe[y_axis].tolist(), fill_color=colors)

    return p

def plot_scatter(x_values: pd.Series, y_values: pd.Series, x_axis:str, y_axis:str, color="green",
                 title="", p:Figure=None):
    if p is None:
        p = figure(title=title, x_axis_label=x_axis.capitalize(), y_axis_label=y_axis.capitalize())
    p.scatter(x_values.values.tolist(), y_values.values.tolist(), color=color)
    return p

def plot_histogram(values: pd.Series, feature:str, color="green", title="", p:Figure=None):
    hist, edges = numpy.histogram(values)
    hist_df = pd.DataFrame({feature: hist,
                            "left": edges[:-1],
                            "right": edges[1:]})
    hist_df["interval"] = ["%d to %d" % (left, right) for left,
                                                          right in zip(hist_df["left"], hist_df["right"])]
    data_src = ColumnDataSource(hist_df)

    if p is None:
        p = figure(title=title, x_axis_label=feature.capitalize(), y_axis_label="Count")
    p.quad(bottom = 0, top = feature, left = "left",
                right = "right", source = data_src, fill_color = color,
                line_color = "black", fill_alpha = 0.7)
    return p

def plot_vbar(categories:[], counts:[], title="", p:Figure=None, plot_width:int=750):
    source = ColumnDataSource(data=dict(x=categories, counts=counts))
    if p is None:
        p = figure(x_range=FactorRange(*categories), plot_height=250, title=title,
               tools="pan,wheel_zoom,box_zoom,reset, save", plot_width=plot_width)
    p.vbar(x='x', top='counts', width=0.9, source=source)
    p.add_tools(HoverTool(tooltips=[("CATEGORY", "@x"), ("TOTAL", "@counts")]))
    return p

def plot_vbar_stacked(categories:[], data:dict, stacks_labels:[], title="", p:Figure=None, plot_width:int=750,
                      hover_tool_tooltips=None):
    # source = ColumnDataSource(data=dict(x=categories, counts=counts))
    colors = [set_color(_) for _, value in enumerate(stacks_labels)]
    if p is None:
        p = figure(x_range=FactorRange(*categories), plot_height=250, title=title, tooltips="$name @$name",
               tools="pan,wheel_zoom,box_zoom,reset, save", plot_width=plot_width)
    p.vbar_stack(stacks_labels, x='categories', width=0.9, color=colors, source=data, legend_label=stacks_labels)
    if hover_tool_tooltips is not None:
        p.add_tools(HoverTool(tooltips=hover_tool_tooltips))
    return p

def plot_cluster_temporal_conversao(dataframe:pd.DataFrame, title=""):
    clusters = dataframe['cluster_label'].unique().tolist()
    colors = [set_color(_) for _ in clusters]

    p = figure(title=title, x_axis_type="datetime")
    for index, cluster in enumerate(clusters):
        cluster_df = dataframe[dataframe['cluster_label'] == cluster]
        taxa_conversao = cluster_df['convertido'] / (cluster_df['convertido'] + cluster_df['nao_convertido'])
        plot_line(cluster_df['label'], taxa_conversao, p, legend="Cluster:{}".format(cluster), color=colors[index])
    return p


def plot_line(x_values:pd.Series, y_values:pd.Series, p:Figure, legend="", color="green"):
    p.line(x_values, y_values, legend_label=legend, color=color)
    # return p


def _unique(original):
    return list(set(original))


def set_color(color):
    index = int(color) % len(COLORS)

    return COLORS[index]

def transform_pca_2d(vector:numpy.array):
    pca = PCA(n_components=2)
    pca.fit(vector)
    new_space = pca.transform(vector)
    return new_space



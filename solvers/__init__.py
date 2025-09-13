from .graph_gen import gen_graph
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from flet.matplotlib_chart import MatplotlibChart

matplotlib.use("svg")

def draw_graph(graph: nx.DiGraph) -> MatplotlibChart:
    fig, ax = plt.subplots()
    nx.draw(graph, with_labels=True, ax=ax)
    return MatplotlibChart(fig, expand=True)

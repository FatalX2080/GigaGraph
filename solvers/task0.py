import graphviz as gv
from .graph_gen import gen_graph
import flet as ft
import base64

FILE_PATH = 'render/rendered_graph'

def draw_by_issue(var: int, img_obg:ft.Image) -> None:
    """
    :param var: issue_in_magazine
    :return:
    """
    v, e = gen_graph(var)

    dot = gv.Digraph(
        comment='Haar graph', format='svg', graph_attr={'rankdir': 'LR'},
        node_attr={'shape': 'circle', 'width': '0.5', "fixedsize": "true"}
    )

    for vertex in v: dot.node(str(vertex))
    for iex, edge in enumerate(e):  dot.edge(str(edge[0]), str(edge[1]), f"u{iex + 1}")

    png_bytes = dot.pipe(format='svg')
    img_base64 = base64.b64encode(png_bytes).decode('utf-8')
    img_obg.src_base64 = img_base64

    img_obg.update()
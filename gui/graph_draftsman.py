from typing import Sequence
from typing import Sequence
from graphviz import Digraph
from config import graph_attr, node_attr, edge_attr
from base64 import b64encode


class Draftsman:
    def __init__(self, vertex: Sequence, edges: Sequence[list | tuple], file_type: str = "png"):
        self.v = vertex
        self.e = edges
        self.dot = Digraph(graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr)
        self.file_type = file_type

    def display_graph(self, name: str, v_colors: Sequence = None, render_md: bool = False) -> bytes:
        self.dot.name = name

        if not v_colors:
            for v in self.v:
                self.dot.node(str(v), str(v))
        else:
            for iex, v in enumerate(self.v):
                self.dot.node(str(v), str(v), fillcolor=v_colors[iex])

        for iex, e in enumerate(self.e):
            self.dot.edge(str(e[0]), str(e[1]), label=f"u{iex}")

        if not render_md:
            graph = self.dot.pipe(format=self.file_type)
            return graph
        else:
            pass

    def to_flet_format(self, graph: bytes) -> str:
        return b64encode(graph).decode('utf-8')

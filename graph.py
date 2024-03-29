"""
===============================
Style Match
===============================
...
"""

from __future__ import annotations
import uuid
import csv
from typing import Any


class WeightedVertex:
    """A weighted vertex."""
    item_id: str
    item_name: str
    item_description: str
    price: float
    urls: list[str]
    neighbours: dict[WeightedVertex, float]

    def __init__(self, item_id: str, item_name: str, item_description: str, price: float, urls: list[str]) -> None:
        """Initialize a new vertex with the given item."""
        self.item_id = item_id
        self.item_name = item_name
        self.item_description = item_description
        self.price = price
        self.urls = urls
        self.neighbours = {}

    def get_ordered_neighbours(self) -> list[WeightedVertex]:
        """Returns a list of the neighbours ordered by decreasing weights"""

        n = dict(sorted(self.neighbours.items(), key=lambda i: -i[1]))
        return list(n.keys())


class WeightedGraph:
    """A weighted graph."""

    vertices: dict[str, WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, item_id: str, item_name: str, item_description: str, price: float, urls: list[str]) -> None:
        """
        Add a vertex with the given parameters to this graph.
        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if item_id not in self.vertices:
            self.vertices[item_id] = WeightedVertex(item_id, item_name, item_description, price, urls)

    def add_edge(self, item_id1: Any, item_id2: Any, weight: float = 1) -> None:
        """Add an edge between the two vertices with the given item_ids in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """

        # check if both vertices exist
        if item_id1 in self.vertices and item_id2 in self.vertices:
            v1 = self.vertices[item_id1]
            v2 = self.vertices[item_id2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            raise ValueError

    def get_neighbours(self, item_id) -> list[WeightedVertex]:
        """Returns the neighbours of the vertex with the given id ordered by decreasing weight."""
        return self.vertices[item_id].get_ordered_neighbours()


def load_clothing_items(clothing_items_file: str) -> WeightedGraph:
    """Create a weighted graph containing each clothing item from the file as vertices."""

    g = WeightedGraph()

    with open(clothing_items_file) as file:
        reader = csv.reader(file)
        for line in reader:

            # skip headers
            if line[0] == "brand":
                continue

            # create vertex for each clothing item
            urls = str_to_list(line[7])
            g.add_vertex(line[2], line[3], line[4], float(line[5]), urls)

    return g


def create_edges(g: WeightedGraph) -> None:
    """Creates edges between vertices in the given graph based on the similarity score between item descriptions."""
    vertex_names = list(g.vertices.keys())

    for i in range(len(vertex_names)):
        for j in range(i + 1, len(vertex_names)):
            create_edge(g, vertex_names[i], vertex_names[j])


def create_edge(g: WeightedGraph, id1: str, id2: str) -> None:
    """Check the similarity of the vertices with the given ids
    and add an edge if the score passes a certain threshold.

    No edge is added if the ids are identical."""

    if id1 == id2:
        return

    threshold = 0.5     # TODO: temp

    v1 = g.vertices[id1]
    v2 = g.vertices[id2]

    # get similarity score between two vertices
    score = get_similarity_score(v1.item_description, v2.item_description)

    # if score is above a certain threshold, add edge with score as the weight
    if score > threshold:
        g.add_edge(v1.item_id, v2.item_id, score)


def get_similarity_score(text1: str, text2: str) -> float:
    """Return the similarity score between the two given texts."""

    # TODO: placeholder
    return 1


def str_to_list(text: str) -> list[str]:
    """Takes in a string representation of a list of strings and converts them into a list of strings."""

    lst = text[1:-1].split(",")         # remove brackets and split by comma
    for i in range(len(lst)):
        lst[i] = lst[i][1:-1]           # remove quotations

    return lst


def create_clothing_item(g: WeightedGraph, item_description: str) -> str:
    """Add new vertex with given parameters to the weighted graph and calculate its neighbours
    and return its item_id"""

    item_id = str(uuid.uuid4())         # generate random id
    g.add_vertex(item_id, "", item_description, 0, [])      #TODO: missing info?

    for other_id in g.vertices:
        create_edge(g, item_id, other_id)

    return item_id


if __name__ == '__main__':

    # create the graph using a dataset
    graph = load_clothing_items("data/store_zara_small_women.csv")
    create_edges(graph)

    # add a new clothing item to the graph
    item_description = "This is a black dress."
    new_id = create_clothing_item(graph, item_description)

    # get list of similar clothing items ordered by decreasing similarity
    similar_items = graph.get_neighbours(new_id)
    print([i.item_name for i in similar_items])

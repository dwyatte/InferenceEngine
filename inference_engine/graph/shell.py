import pprint
import json
from ego import egonet
from networkx import Graph, write_gexf, spring_layout, to_edgelist


class GraphShell(object):

    """
    Query shell over graph engine
    """

    def __init__(self, engine, query_output=None):
        """

        Parameters
        ----------
        engine: GraphEngine object
        query_output: Whether to write query output to file or just print

        Returns
        -------

        """
        self.query_output = query_output
        self.engine = engine

    def query_topk_nodes_degree(self, k):
        """
        return top-k nodes in terms of degree
        Parameters
        ----------
        k

        Returns
        -------

        """
        degree = self.engine.degree()
        return sorted(zip(degree.values(), degree.keys()))[-k:]

    def _query_node_subgraph(self, node):
        """
        get the subgraph of a node (broken in networkx, we will do it manually)
        Parameters
        ----------
        node

        Returns
        -------
        ebunch
        """
        neighbors = self.engine.neighbors(node)
        return [(node, n, self.engine.get_edge_data(node, n)['weight']) for n in neighbors]

    def _query_node_egonet(self, node):
        """
        get the egnoet of a node
        Parameters
        ----------
        node

        Returns
        -------
        ebunch
        """
        ego = egonet(self.engine, node)
        # return the edge bunch
        return [(e[0], e[1], e[2]['weight']) for e in to_edgelist(ego)]

    def query_node(self, node):
        """
        either print or write to file the subgraph/egonet of a node
        Parameters
        ----------
        node

        Returns
        -------

        """
        # ebunch = self._query_node_subnet(node)
        ebunch = self._query_node_egonet(node)
        if self.query_output:
            pprint.pprint(ebunch)
            # return self.write_gexf(ebunch, self.query_output)  # doesn't seem to work with SigmaJS
            self._write_json(ebunch, self.query_output)
        else:
            pprint.pprint(ebunch)

    @staticmethod
    def _write_json(ebunch, path):
        """

        Parameters
        ----------
        ebunch
        path

        Returns
        -------

        """
        G = Graph()
        G.add_weighted_edges_from(ebunch)
        pos = spring_layout(G)

        nodes = [{"id": str(k),
                  "label": str(k),
                  "size": "100",
                  "x": pos[k][0],
                  "y": pos[k][1]}
                 for k in pos]

        edges = [{"id": '%s-%s' % (e[0], e[1]),
                  "source": e[0],
                  "target": e[1]}
                 for e in ebunch]

        with open(path, 'w') as f:
            json.dump({"nodes": nodes, "edges": edges}, f)

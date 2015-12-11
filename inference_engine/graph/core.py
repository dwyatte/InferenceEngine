
import itertools
from networkx.classes import Graph


class GraphCore(Graph):

    """
    Core graph shell
    """

    def __init__(self, node_separator='='):
        """

        Parameters
        ----------
        node_separator

        Returns
        -------

        """
        self.node_separator = node_separator
        super(GraphCore, self).__init__()

    def _edge_bunch_from_json_records(self, records):
        """
        * merges key1, sep, val1 for each key/val in records
        * then creates edge list
        Parameters
        ----------
        records [{key1: val1, key2: val2}, {key1: val1, key2: val2}, ...]

        Returns ebunch [(source1, target1, weight1), (source2, target2, weight2), ...]
        -------

        """
        # format node name
        nodes = [map(lambda x: '%s%s%s' % (x[0], self.node_separator, x[1]), zip(d.keys(), d.values())) for d in records]
        # take combinations
        edgelist = [list(itertools.combinations(n, 2)) for n in nodes]
        # add weight
        edgelist = [[edge + (1.0,) for edge in combination] for combination in edgelist]
        # flatten and return
        return itertools.chain(*edgelist)

    def insert(self, records):
        """
        insert records into graph

        Parameters
        ----------
        records [{key1: val1, key2: val2}, {key1: val1, key2: val2}, ...]

        Returns
        -------

        """
        ebunch = self._edge_bunch_from_json_records(records)
        # update weight if already in graph
        ebunch = [(x[0], x[1], x[2]+self.get_edge_data(x[0], x[1])['weight'])
                     if self.get_edge_data(x[0], x[1]) else (x[0], x[1], x[2]) for x in ebunch]
        self.add_weighted_edges_from(ebunch)
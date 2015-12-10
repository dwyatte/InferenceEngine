import itertools
from networkx.classes import Graph


class GraphEngine(Graph):

    def __init__(self, separator='='):
        self.separator = separator
        super(GraphEngine, self).__init__()

    def _edge_list_from_json_records(self, records):
        """
        * merges key1, sep, val1 for each key/val in records
        * then creates edge list
        :param records: [{key1: val1, key2: val2}, {key1: val1, key2: val2}, ...]
        :return:
        """
        # format node name
        nodes = [map(lambda x: '%s%s%s' % (x[0], self.separator, x[1]), zip(d.keys(), d.values())) for d in records]
        # take combinations
        edgelist = [list(itertools.combinations(n, 2)) for n in nodes]
        # add weight
        edgelist = [[edge + (1.0,) for edge in combination] for combination in edgelist]
        # flatten and return
        return itertools.chain(*edgelist)

    def insert(self, records):
        edge_list = self._edge_list_from_json_records(records)
        edge_list = [(x[0], x[1], x[2]+self.get_edge_data(x[0], x[1])['weight'])
                     if self.get_edge_data(x[0], x[1]) else (x[0], x[1], x[2]) for x in edge_list]
        self.add_weighted_edges_from(edge_list)
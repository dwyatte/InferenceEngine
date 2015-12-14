import sys
import time
import itertools
from threading import Thread
from networkx import Graph


class GraphEngine(Graph, Thread):
    """
    Performs threaded insertion of json stream into graph
    """

    def __init__(self, input_stream, record_filter=None, node_separator='=', max_nodes=sys.maxint, max_edges=sys.maxint):
        """

        Parameters
        ----------
        input_stream: iterator with a next(), should contain list of dicts (records)
        record_filter: only use these keys from input_stream
        node_separator: separtor between node key and value
        max_nodes: stop inserting from stream after max_nodes in graph
        max_edges: stop inserting from stream after max_edges in graph

        Returns
        -------

        """
        # constructor fields
        self.input_stream = input_stream
        self.record_filter = record_filter
        self.node_separator = node_separator
        self.max_nodes = max_nodes
        self.max_edges = max_edges

        # stats
        self.records_per_second = -1
        self.records_processed = 0

        # I don't think this is how to handle multiple-inheritance super init, but it seems to work
        Graph.__init__(self)
        Thread.__init__(self)
        self.start()

    def stats(self):
        return 'GraphEngine: %d records processed, %d nodes, %d edges (%f records/second)' % \
               (self.records_processed, self.number_of_nodes(), self.number_of_edges(), self.records_per_second)

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
        records: [{key1: val1, key2: val2}, {key1: val1, key2: val2}, ...]

        Returns
        -------

        """
        ebunch = self._edge_bunch_from_json_records(records)
        # update weight if already in graph
        ebunch = [(x[0], x[1], x[2]+self.get_edge_data(x[0], x[1])['weight'])
                  if self.get_edge_data(x[0], x[1]) else (x[0], x[1], x[2]) for x in ebunch]
        self.add_weighted_edges_from(ebunch)

    def run(self):
        """

        Returns
        -------

        """
        for records in self.input_stream:
            start_time = time.time()

            # filter, remove empties, and insert
            if self.record_filter:
                records = [dict([(k, record[k]) for k in self.record_filter if k in record]) for record in records]
            records = [record for record in records if len(record) > 1]
            self.insert(records)

            # stats
            elapsed_time = time.time() - start_time
            self.records_per_second = len(records)/elapsed_time
            self.records_processed += len(records)

            # stop insertion if we hit max graph size
            if self.number_of_nodes() > self.max_nodes or self.number_of_edges() > self.max_edges:
                break

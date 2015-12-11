import sys
import time
import pprint
import json
from networkx import Graph, write_gexf, spring_layout
from threading import Thread
from inference_engine.graph.core import GraphCore


class GraphEngine(GraphCore, Thread):
    """
    Threaded version of graph core
    """

    def __init__(self, input_stream, record_filter=None, max_nodes=sys.maxint, max_edges=sys.maxint, query_output=None,
                 verbose=False):
        """

        Parameters
        ----------
        input_stream
        record_filter
        max_nodes
        max_edges
        verbose

        Returns
        -------

        """
        # constructor fields
        self.input_stream = input_stream
        self.record_filter = record_filter
        self.max_nodes = max_nodes
        self.max_edges = max_edges
        self.query_output = query_output
        self.verbose = verbose

        # stats
        self.records_per_second  = -1
        self.records_processed = 0

        # I don't think this is how to handle multiple-inheritance super init, but it seems to work
        Thread.__init__(self)
        GraphCore.__init__(self)

    def stats(self):
        return 'GraphEngine: %d records processed, %d nodes, %d edges (%f records/second)' % \
               (self.records_processed, self.number_of_nodes(), self.number_of_edges(), self.records_per_second)

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

            if self.verbose:
                print self.stats()

            # stop insertion if we hit max graph size
            if self.number_of_nodes() > self.max_nodes or self.number_of_edges() > self.max_edges:
                break

    def query_topk_nodes_degree(self, k):
        """
        return
        Parameters
        ----------
        k

        Returns
        -------

        """
        degree = self.degree()
        return sorted(zip(degree.values(), degree.keys()))[-k:]

    def query_node(self, node):
        """

        Returns
        -------

        """
        neighbors = self.neighbors(node)
        ebunch = [(node, n, self.get_edge_data(node, n)['weight']) for n in neighbors]

        if self.query_output:
            pprint.pprint(ebunch)
            # return self.write_gexf(ebunch, self.query_output)  # doesn't seem to work with SigmaJS
            self._write_json(ebunch, self.query_output)
        else:
            pprint.pprint(ebunch)

    def _write_json(self, ebunch, path):

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




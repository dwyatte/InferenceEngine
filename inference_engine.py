import time
from inference_engine.elastic import ElasticStream
from inference_engine.graph import GraphEngine

ES_HOST = '10.1.20.125'
ES_PORT = '9200'
ES_INDEX = 'logsar-internaldeploymenttestrestore-*'
RECORD_FILTER = ['login', 'originIp', 'originName', 'impactedIp', 'impactedName']
QUERY_OUTPUT = 'output.json'
MAX_NODES = 1e5
MAX_EDGES = 1e6

if __name__ == '__main__':

    es = ElasticStream(ES_HOST, ES_PORT, ES_INDEX,
                       '{"query": {"match_all": {}}}',
                       scroll_keep_alive='1m', scroll_size=100)

    ge = GraphEngine(es, record_filter=RECORD_FILTER, query_output=QUERY_OUTPUT,
                     max_nodes=MAX_NODES, max_edges=MAX_EDGES, verbose=False)
    ge.start()
    time.sleep(1)

    print
    print 'GraphEngine (ge) started.\n' \
          'Nodes with highest degree: %s\n' \
          'Query with ge.query_node([node])\n' % ge.query_topk_nodes_degree(3)
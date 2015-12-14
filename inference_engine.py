import time
from inference_engine.elastic import ElasticStream
from inference_engine.graph import GraphShell, GraphEngine

ES_HOST = '10.1.20.125'
ES_PORT = '9200'
ES_INDEX = 'logsar-internaldeploymenttestrestore-*'
ES_QUERY = '{"query": {"match_all": {}}}'
RECORD_FILTER = ['login', 'originIp', 'originName', 'impactedIp', 'impactedName']
QUERY_OUTPUT = 'app/data/data.json'
MAX_NODES = 1e5
MAX_EDGES = 1e6

if __name__ == '__main__':
    stream = ElasticStream(ES_HOST, ES_PORT, ES_INDEX, ES_QUERY, scroll_keep_alive='1m', scroll_size=100)
    engine = GraphEngine(stream, record_filter=RECORD_FILTER, max_nodes=MAX_NODES, max_edges=MAX_EDGES)
    shell = GraphShell(engine, query_output=QUERY_OUTPUT)

    time.sleep(1)

    print
    print engine.stats()
    print 'GraphShell started.'
    print 'Nodes with highest degree: %s' % shell.query_topk_nodes_degree(3)
    print 'Query with shell.query_node([node])'

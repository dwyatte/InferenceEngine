import json
import time
import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt

from inference_engine.elastic_stream import ElasticStream
from inference_engine.graph_engine import GraphEngine

ES_HOST = '10.1.20.125'
ES_PORT = '9200'
ES_INDEX = 'logsar-internaldeploymenttestrestore-*'
RECORD_FILTER = ['login', 'originIp', 'originName', 'impactedIp', 'impactedName']

if __name__ == '__main__':

    with open('queries/match_all.json') as f:
        data = json.dumps(json.load(f))

    es = ElasticStream(ES_HOST, ES_PORT, ES_INDEX, data)
    ge = GraphEngine()

    for records in es:
        start_time = time.time()
        # filter and remove empties
        records = [dict([(k, record[k]) for k in RECORD_FILTER if k in record]) for record in records]
        records = [record for record in records if len(record) > 1]
        ge.insert(records)
        elapsed_time = time.time() - start_time
        print 'GraphEngine: %d nodes, %d edges, (insert time: %f seconds)' % \
              (ge.number_of_nodes(), ge.number_of_edges(), elapsed_time)

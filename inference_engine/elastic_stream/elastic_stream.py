import requests


class ElasticStream(object):
    """
    Class to handle elasticsearch stream
    """

    def __init__(self, host, port, index, data, scroll_keep_alive='1m', scroll_size='5'):
        """
        Initialize the context by performing the search once and storing context as fields such as the scroll_id,
        number of hits, and the mappings so that the keys are consistent across scrolls
        :param host: Elasticsearch host on which to execute query (e.g., 10.1.10.208)
        :param port: Elasticsearch port
        :param index: 'Elasticsearch index to query (*-wildcards allowed)'
        :param data: JSON string data specifying Elasticsearch DSL query
        :param scroll_keep_alive: How long to keep the scroll context alive
        :param scroll_size: Size of scroll (multiplied by # shards)
        :return:
        """
        self.host = host
        self.port = port
        self.index = index
        self.scroll_keep_alive = scroll_keep_alive
        self.scroll_size = str(scroll_size)

        # the scroll id saves our context and will get updated with each scroll
        url = 'http://%s:%s/%s/_search?scroll=%s&size=%s&search_type=scan' % \
              (host, port, index, scroll_keep_alive, scroll_size)
        print 'Creating stream from %s -d %s' % (url, data)
        response = requests.get(url, data=data).json()
        self.scroll_id = response['_scroll_id']
        self.hits_total = response['hits']['total']
        self.hits_scrolled = 0

    def __iter__(self):
        return self

    def next(self):
        """
        Scroll through one self.scroll_size set of results and save the new scroll_id context
        """
        url = 'http://%s:%s/_search/scroll?scroll=%s&scroll_id=%s' % \
              (self.host, self.port, self.scroll_keep_alive, self.scroll_id)
        response = requests.get(url).json()

        # update scroll id and return hits
        self.scroll_id = response['_scroll_id']
        self.hits_scrolled += len(response['hits']['hits'])
        return [x['_source'] for x in response['hits']['hits']]
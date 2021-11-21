import json
from elasticsearch import Elasticsearch
import jsonpickle
class A(object):
    def __init__(self, name):
        self.name=name
def index_links(links, url):
    data=jsonpickle.encode(A(links))
    es = Elasticsearch('http://127.0.0.1:9200') 
    es.index(index="crawled_links", doc_type="links",id=url, body=data)

def index_data(data):
        es = Elasticsearch('http://127.0.0.1:9200') 
        es.index(index="data", doc_type="page_content", body=json.dumps(data)) 

#base_url='https://www.python.org/download/releases/3.0/'

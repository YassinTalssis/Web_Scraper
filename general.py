import os
import json
from elasticsearch import Elasticsearch
import jsonpickle
import requests
from bs4 import BeautifulSoup
class A(object):
    def __init__(self, name):
        self.name=name
#flash  website you crow is a separate project(folder)
def create_project_dir(directory):
   if not os.path.exists(directory):#creating a directory if not exists
        print("creatin directory "+directory)
        os.makedirs(directory)

#creating queue and crawled files (if not ctreated)
def creating_data_files(project_name, base_url):
    queue = project_name +'/queue.txt'
    crawled = project_name +'/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue,base_url)
    if not os.path.isfile(crawled):
        write_file(crawled,'')


#write write_file fonction
def write_file(path, data):
    f=open(path,'w')
    f.write(data)
    f.close()

#add data onto an existing file
def append_to_file(path,data):
    with open(path,'a') as file:
        file.write(data +'\n')

#delecte the content of a file
def delecte_file_contents(path):
    with open(path,'w'):
        pass


#writing in  files is very slowling, so we can use variables
#read a file tile and conert each line to set item
def file_to_set(file_name):
    results = set()
    with open(file_name,'rt') as f:
        for line in f:
            results.add(line.replace('\n',''))
    return results
#iterate throught a set, each item will be a new line in the fille
def set_to_file(links,file):
    delecte_file_contents(file)
    for link in sorted(links):
        append_to_file(file,link)

def index_links(links, url):
    data=jsonpickle.encode(A(links))
    es = Elasticsearch('http://127.0.0.1:9200') 
    es.index(index="crawled_links", doc_type="links",id=url, body=data)

#this fonction store ours data in elastic search
def index_data(data):
        es = Elasticsearch('http://127.0.0.1:9200') 
        es.index(index="data", doc_type="page_content", body=json.dumps(data))
#dowload html of a page 
def download_page(url):
    headers ={
            'User-Agent':'FPT Searching bot version 0.1'
            }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception("not ok status code {}".format(r.status_code))
    return r.text

#parse html given by dowload_page
def parse_text(html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs
    
"""create_project_dir('thenewboston')
creating_data_files('thenewboston','https://thenewboston.com/')
set_to_file('www.fcfd.com','queue.txt')"""
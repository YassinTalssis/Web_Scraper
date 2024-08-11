from general import *
from urllib.parse import urljoin
import re
#ty
class spider:
    # here, i defined the static variables (shared between all the spiders)
    project_name = ''
    base_url = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()


    def __init__(self, project_name, base_url):
        spider.project_name = project_name
        spider.base_url = base_url
        spider.queue_file = project_name + '/queue.txt'
        spider.crawled_file = project_name + '/crawled.txt'
        self.boot()
        self.craw_page('First spider ', spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(spider.project_name)
        creating_data_files(spider.project_name, spider.base_url)
        spider.queue = file_to_set(spider.queue_file)
        spider.crawled = file_to_set(spider.crawled_file)

    @staticmethod
    def craw_page(thread_name, page_url):
        if page_url not in spider.crawled:
            print(thread_name + 'now crawling ' + page_url)
            print('queue :' + str(len(spider.queue)) + '| crawled :' + str(len(spider.crawled)))
            spider.add_links_to_queue(spider.gatter_data(page_url))
            spider.queue.remove(page_url)  # remove page from waiting list
            spider.crawled.add(page_url)  # add page to crawled list
            spider.update_files()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in spider.queue:
                continue
            if url in spider.crawled:
                continue
            if spider.domain_name not in url:
                continue
            spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(spider.queue, spider.queue_file)
        set_to_file(spider.crawled, spider.crawled_file)
    def gatter_data(start_url):
                try:
                        soup = parse_text(download_page(start_url))
                        headers = ''
                        #find all tags start with h and have a dih=gital after it and end in the end
                        for header  in soup.find_all(re.compile('^h[1-6]$')):
                                headers = headers+' '+header.text.strip()
                        pa= ''
                        for p in soup.find_all('p'):
                            pa= pa+' '+p.text.strip()
                        result = {
                                'id':start_url,
                                'title':soup.find('title').text,
                                'headers':headers,
                                'content':pa
                        }
                        all_links = soup.find_all('a')
                        for link in all_links:
                                a=0
                                url = link.get('href')
                                if 'http://' in url :
                                    for e in url:
                                        if e=='/':
                                            a=a+1
                                    if a<=4:
                                        if url not in (spider.queue and spider.crawled):
                                            spider.queue.add(url)
                                else:
                                    url = urljoin(start_url, url)
                                    for e in url:
                                        if e=='/':
                                            a=a+1
                                    if url not in (spider.queue and spider.crawled) and a<4:
                                            spider.queue.add(url)    
                except:
                    result=None
                if result is not None:
                   index_data(result)
                return spider.queue

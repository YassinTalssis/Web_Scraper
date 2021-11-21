import threading
from queue import Queue
from spider import spider
from domain import *
from general import *

PROJECT_NAME = 'Links'
HOME_PAGE = 'https://www.javatpoint.com/'
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 2
queue = Queue()
spider(PROJECT_NAME, HOME_PAGE)

# create worker threads (will die when the main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# the next job in the queue
def work():
    while True:
        url = queue.get()
        spider.craw_page(threading.current_thread().name, url)
        queue.task_done()

# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

#  check if they are items in the queue , if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + 'links in the queue')
        create_jobs()

def main():
    create_workers()
    crawl()
    
if __name__=='__main__':
    main()

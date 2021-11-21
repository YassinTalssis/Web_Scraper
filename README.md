# Web_Scraper
This is a simple web scraper that travel around the WWW, extract all text from html pages and stock them in elasticsearch.
The principe is simple:
1- i give it a start url. 
2-download this page and extract all text && links. 
3-Add links to queue file and start url to crawled file.
4-index data in elasticsearch.
5- start url = first url in queue.
To add some performance i already used multithreading...

from urllib.parse import urlparse,urljoin


# get domain name like exemple.com
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''

# get sub domain name like name.exemple.com
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''

#print(urljoin('https://java.developpez.com/cours/','/ftp/python/3.0/Python-3.0.tgz'))


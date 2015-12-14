__author__ = 'Dev'

from urlparse import urlparse, urlunparse,urljoin
import re
from urllib import unquote

_collapse = re.compile('([^/]+/\.\./?|/\./|//|/\.$|/\.\.$)')

def Canonicalize(url,parent_domain):
    (scheme, netloc, path, parameters, query, fragment) =  urlparse(url)
    scheme = "http"
    parent =  urlparse(parent_domain)
    if not netloc and not path:
        return ""
    if not netloc and path.startswith("."):
        new_url = urljoin(parent_domain, path)
        (scheme, netloc, path, parameters, query, fragment) =  urlparse(new_url)
    elif not netloc and path:
        netloc = parent.netloc
    netloc = netloc.lower().split(":")[0]
    last_path = path
    while 1:
        path = _collapse.sub('/', path, 1)
        if last_path == path:
            break
        last_path = path
    path = unquote(path)
    return urlunparse((scheme,netloc,path,"","",""))


def base_url(url):
    extract = urlparse(url)
    return extract.scheme+'://'+extract.netloc+'/'

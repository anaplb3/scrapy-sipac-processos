import urllib.parse as urlparse
import os

url = urlparse.urlparse(os.environ['DATABASE_URL'])

POSTGRES_CFG = {
    'host': url.hostname,
    'port': url.port,
    'dbname': url.path[1:],
    'user': url.username,
    'pwd': url.password
}

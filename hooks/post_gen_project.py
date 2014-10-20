import shutil
import json
try:
    # For Python 3.0 and later
    from urllib.request import Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import Request

# config = json.loads(open('./config/config.json', 'r').read())

config = {
    "repo_name": 'test'
}

print(open('./config/config.json', 'r').read())

print('Create project on Jenkins', config['repo_name'])
# req = Request('http://ci.anvil8.com/createItem?name={{', data, headers)

shutil.rmtree('./config')
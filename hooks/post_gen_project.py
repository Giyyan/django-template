import shutil
try:
    # For Python 3.0 and later
    from urllib.request import Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import Request

print('Create project on Jenkins {{cookicutter.repo_name}}')
# req = Request('http://ci.anvil8.com/createItem?name={{', data, headers)

shutil.rmtree('./config')
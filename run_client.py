import sys
from client.client import Client

cli = None

if len(sys.argv) > 1:
    if sys.argv[1] == 'local':
        cli = Client(local=True)
else:
    cli = Client()

import sys
from gradio_client import Client
c = Client(sys.argv[1])
c.view_api()

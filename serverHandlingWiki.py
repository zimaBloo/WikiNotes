#Necessary imports
import xml.etree.ElementTree as ET

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

import requests
import time

#Threading
from socketserver import ThreadingMixIn
import threading



#Wikipedia query requirement
#Looked up how this could be done in the web, and found a REST API that Wikipedia provides on this forum: https://stackoverflow.com/questions/8555320/is-there-a-wikipedia-api-just-for-retrieve-the-content-summary
def restApiWiki(topic):
    time.sleep(1) #needed to not overload wikipedia API with requests

    
    makingUrl = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"

    response = requests.get(makingUrl)


    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No summary available") + f"\n\nLink to read more: {data.get('content_urls', {}).get('desktop', {}).get('page', '')}" #Got help from Copilot for this
    
    return "No Wikipedia information found."


class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass




def launchWikiServer():
    server = ThreadedXMLRPCServer(("127.0.0.1", 8001), requestHandler=SimpleXMLRPCRequestHandler, allow_none=True)

    server.register_function(restApiWiki, "restApiWiki")


    print("Wikipedia Server started on 127.0.0.1:8001")

    server.serve_forever()

    

if __name__ == "__main__":
    launchWikiServer()
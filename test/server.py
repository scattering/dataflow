import sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,root)

import re
import BaseHTTPServer
import SimpleHTTPServer
    
server_class=BaseHTTPServer.HTTPServer
handler_class=SimpleHTTPServer.SimpleHTTPRequestHandler
WWW = os.path.abspath(os.path.join(root,'www'))

handler_class.extensions_map['.json'] = 'application/json'

def run(host='',port=8000,path=WWW):
    os.chdir(path)
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
